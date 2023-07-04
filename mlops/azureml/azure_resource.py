from functools import partial
from azureml.core import Run
from typing import Callable, Generator, TypedDict, Iterable
from azureml.core import Workspace, Experiment
from azure.ai.ml import MLClient
from azure.identity import AzureCliCredential
from azure.cli.core._profile import Profile
from azure.mgmt.resource import ResourceManagementClient
from azureml.core.authentication import InteractiveLoginAuthentication
from azure.mgmt.resource.resources.v2022_09_01.models import ResourceGroup

from itertools import repeat, chain

class ResourceDict(TypedDict):
    name: list[str]
    workspaces: list[tuple[str, Workspace]]

class AzureBaseClass:

    """
    general class for getting azure
    resources
    """

    _resource_dict: dict[str, ResourceDict] = {}

    @property
    def resources_dict(self) -> dict[str, ResourceDict]:
        return self._resource_dict

    @resources_dict.setter
    def resources_dict(self, value: dict[str, dict[str, list[str]]]):

        """
        this dictionary will get updated with all
        the ids, workspaces and names of the resources
        """

        # confirm if value is a dict in the format of ResourceDict
        if not isinstance(value, dict):
            raise TypeError(f'Expected dict, got {type(value)}')
        if not all(isinstance(v, dict) for v in value.values()):
            raise TypeError(f'Expected dict, got {type(value)}')
        self._resource_dict = self.deep_update(self._resource_dict, value)

    def deep_update(self, source: dict, updates: dict) -> dict:
        for key, value in updates.items():
            if isinstance(value, dict):
                source[key] = self.deep_update(source.get(key, {}), value)
            else:
                source[key] = value
        return source

    def _loop_resources_dict(self, function: Callable):

        """
        in the first iteration the resources_dict
        will be empty, so it will be filled
        with the first function call
        """

        if self.resources_dict == {}:
            self.resources_dict = function()
        else:
            for k, v in self.resources_dict.items():
                self.resources_dict = function(k, v)
        return self


    def _generate_dict_from_iterable(self, iterable: Iterable[dict]) -> dict:

        """
        generate a dictionary from an iterable of dictionaries
        """

        return {k: v for i in iterable for k, v in i.items()}

    def _azure_local_authentication(self):

        """
        azure interactive login authentication
        if its running locally it will ask
        for authentication
        theres no way to return anything to
        if user is not logged in but its
        possible to always run this function
        and it will check if the user is logged in
        """

        InteractiveLoginAuthentication()

        return

    def _check_if_isinstance_experiment(self, run_context: dict) -> bool:
        """
        check if the current run is a local or running in a azure vm
        """
        return isinstance(run_context.__dict__.get('_experiment', None), Experiment)

    def _check_if_running_on_vm(self):
        """
        checks if running on vm
        if true = running on an azure cluster
        if false = not running on azure cluster
        """
        return self._check_if_isinstance_experiment(Run.get_context())

class AzureIDClass(AzureBaseClass):

    """
    generate ids for the resources
    """

    _profile = None

    def initialize(self):
        self._generate_ids()

    @property
    def profile(self) -> Profile:
        """
        this makes sure that the profile is
        initialized only once
        """
        if self._profile is None:
            self._profile = Profile()
        return self._profile

    def _map_generate_resources(self) -> Iterable[dict[str, dict]]:

        """
        generates the map for the resources dict
        and repeat the dict for each subscription
        """

        return map(lambda cached_subscriptions, default_dict_name: {cached_subscriptions['id']: default_dict_name},
                   self.profile.load_cached_subscriptions(),
                   repeat({'name': [], 'workspaces': []}))


    def _generate_ids_dict(self):

        """
        this dictionary is used to store the
        id, resource_group_name and workspace name
        """

        return self._generate_dict_from_iterable(self._map_generate_resources())

    def _generate_ids(self):

        """
        generate ids for the resources
        """

        return self._loop_resources_dict(self._generate_ids_dict)

class AzureResourceGroupClass(AzureIDClass):

    def initialize(self) -> None:
        super().initialize()
        self._generate_resource_group_names()

    def _resource_groups(self,
                         id: str) -> ResourceManagementClient:
        """ generate resource groups """
        return ResourceManagementClient(AzureCliCredential(), id)

    def _list_resource_groups(self,
                              resource: ResourceManagementClient) -> Iterable[ResourceGroup]:

        """
        generates resource groups list
        """

        return resource.resource_groups.list()

    def _get_resource_group_names(self, id: str) -> Iterable[ResourceGroup]:

        """
        wrapper for _resource_groups and
        _list_resource_groups
        """

        return self._list_resource_groups(self._resource_groups(id))

    def _map_resource_group_names(self, id: str) -> Generator[str, None, None]:
        return map(lambda resource_group: resource_group.name, self._get_resource_group_names(id))

    def _generate_resource_group_names_dict(self,
                                            id: str,
                                            resourcedict: ResourceDict) -> dict[str, ResourceDict]:

        """

        """

        return {id: {'name': list(self._map_resource_group_names(id)),
                     'workspaces': []}}

    def _generate_resource_group_names(self):
        """
        run the _generate_resource_group_names_dict to get the resource groups
        and save to the resources_dict
        """
        return self._loop_resources_dict(self._generate_resource_group_names_dict)

class AzureWorkspaceClass(AzureResourceGroupClass):

    """
    generate the workspaces names
    """

    def initialize(self):
        super().initialize()
        self._get_woskspace_name_dict()
        return self

    def _get_name_from_workspace(self, workspace: Iterable[Workspace]) -> str:
        return map(lambda workspace: workspace.name, workspace)

    def _wrapper_create_workspace_object(self,
                                        id: str,
                                        resource_group_name: str,
                                        workspace: Iterable[Workspace]) -> Workspace:

        return  map(partial(self._get_workplace_object, id, resource_group_name),
                                           self._get_name_from_workspace(workspace))

    def _get_workplace_object(self, id: str,
                              resource_group_name: str,
                              workspace_name: str):

        """
        while MLClient returns a workspace object
        it can not be initialized with the classes
        that are used to find the experiments, because
        the mlclient lacks the credentials method in it
        (service_context)
        """

        return Workspace(subscription_id=id,
                         resource_group=resource_group_name,
                         workspace_name=workspace_name)


    def _get_ml_client_workspace_iterable(self,
                                      id: str,
                                      resource_group_name: str) -> Iterable[Workspace]:

        """
        generates the iterable to get
        the workspaces names from the ml_client
        """

        ml_client = MLClient(credential=AzureCliCredential(),
                        subscription_id=id,
                        resource_group_name=resource_group_name)

        return self._wrapper_create_workspace_object(id,
                                                     resource_group_name,
                                                     ml_client.workspaces.list())


    def _get_ml_client_workspace(self,
                                 id: str,
                                 resource_group_name: str):
        """
        returns the workspace object from the iterable
        """
        return self._get_ml_client_workspace_iterable(id, resource_group_name)

    def _get_ml_client_workspace_map(self,
                                     id: str,
                                     list_resource_group_name: list[str]) -> Iterable[Workspace]:

        """
        generates the iterable to get
        the workspaces names from the ml_client
        """

        return list(chain.from_iterable(
            map(self._get_ml_client_workspace_iterable, repeat(id), list_resource_group_name)))

    def _generate_ml_client_workspace_dict(self,
                                           id: str,
                                           resourcedict: ResourceDict) -> ResourceDict:

        """
        generates the ml_client workspace list
        """

        return {id:
            {'workspaces':self._get_ml_client_workspace_map(id, resourcedict['name'])}}

    def _get_woskspace_name_dict(self):

        """
        generates the workspace names
        """

        return self._loop_resources_dict(self._generate_ml_client_workspace_dict)