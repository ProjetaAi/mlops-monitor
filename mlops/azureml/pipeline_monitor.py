"""Bibliotecas utilizadas."""
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.pipeline.core.run import PipelineRun
from typing import Iterable
from mlops_monitor_2.mlops_monitor.mlops.azureml.azure_resource import AzureWorkspaceClass
from itertools import chain, takewhile
from datetime import datetime, timedelta

class PipelineMonitor:

    azure_resource_obj = AzureWorkspaceClass()

    def __init__(self) -> None:
        pass

    def init_azure_resource(self):
        self.azure_resource_obj.initialize()
        return self

    def chained_get(self, d: dict, *args) -> dict:

        """
        gets the chained value from a dictionary
        if fails returns an empty dict
        """

        if len(args) == 1:
            return d.get(args[0])
        else:
            return self.chained_get(d.get(args[0], {}), *args[1:])

    def recursive_dict(self, d: dict, until_k: str) -> Iterable[dict]:

        """
        gets a specific key from
        recursivelly walking though a
        dictionary
        if multiple are found, it'll return
        all found matches
        """

        for k, v in d.items():
            if k == until_k:
                yield from v
            elif isinstance(v, dict):
                yield from self.recursive_dict(v, until_k)

    def _get_workspaces(self) -> Iterable[Workspace]:

        """
        recursively gets the workspaces from the
        dictionary of resources. It's only
        necessary the workspaces objects to
        extract the experiments and runs
        """

        return self.recursive_dict(self.azure_resource_obj.resources_dict, 'workspaces')

    def _get_experiments_map(self) -> Iterable[list[Experiment]]:

        """
        gets the experiments from the workspaces
        """

        return map(lambda workspace: Experiment.list(workspace), self._get_workspaces())

    def _get_specific_experiment(self,
                                 name: str) -> Iterable[Experiment]:

        """
        filters the experiments by name
        """

        return filter(lambda experiment: experiment.name == name,
                      chain.from_iterable(self._get_experiments_map()))

    def _filter_by_days(self, runs: Iterable[PipelineRun], days: int) -> Iterable[PipelineRun]:
        today = datetime.now().date()
        cutoff = (today - timedelta(days=days)).strftime('%Y-%m-%d')
        return takewhile(lambda run: run.get_details()['startTimeUtc'] > cutoff, runs)

    def _get_runs(self, experiment: Experiment) -> Iterable[PipelineRun]:
        return experiment.get_runs()

    def _get_pipe(self, name: str, days: int) -> Iterable[PipelineRun]:
        return self._filter_by_days(self._get_runs(list(self._get_specific_experiment(name=name))[0]), days)

