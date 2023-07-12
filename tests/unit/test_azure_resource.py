import unittest
from unittest.mock import patch, PropertyMock
from mlops.azureml.azure_resource import AzureWorkspaceClass

class MockProfile:
    def load_cached_subscriptions(self):
        return [{'id': 'fake_id_1'}, {'id': 'fake_id_2'}]

class MockResourceGroup:
    def __init__(self, id):
        self.id = id
        pass

    @property
    def name(self):
        return f'fake_resource_group_from_{self.id}'

def side_effect_get_resource_group_names(id):
    return [MockResourceGroup(id)]

class MockWorkspace:
    def __init__(self, id, resource_group):
        self.id = id
        self.resource_group = resource_group
        pass

class Test_AzureVariables(unittest.TestCase):

    def setUp(self) -> None:
        self.class_test = AzureWorkspaceClass()

    def test_declare_class(self):
        self.assertIsInstance(self.class_test, AzureWorkspaceClass)

    def test_check_if_running_on_vm(self):
        self.assertFalse(self.class_test._check_if_running_on_vm())

    @patch.object(AzureWorkspaceClass, '_get_ml_client_workspace_iterable', return_value=[MockWorkspace])
    @patch.object(AzureWorkspaceClass, '_get_resource_group_names', side_effect=side_effect_get_resource_group_names)
    @patch.object(AzureWorkspaceClass, 'profile', new_callable=PropertyMock, return_value=MockProfile())
    def test_generate_resources_dict(self,
                                     mock_profile,
                                     mock_get_resource_group_names,
                                     mock_get_ml_client_workspace_iterable):
        self.class_test._generate_ids()

        self.assertEqual(self.class_test.resources_dict, {
            'fake_id_1': {'name': [], 'workspaces': []},
            'fake_id_2': {'name': [], 'workspaces': []},
        })

        with self.assertRaises(TypeError):
            # this meant to fail
            self.class_test.resources_dict = 1  # type: ignore
        with self.assertRaises(TypeError):
            # this meant to fail that's why the type: ignore
            self.class_test.resources_dict = {'fake_id_1': 1} # type: ignore

        self.class_test._generate_resource_group_names()

        self.assertEqual(self.class_test.resources_dict, {'fake_id_1': {'name': ['fake_resource_group_from_fake_id_1'], 'workspaces': []},
                                                          'fake_id_2': {'name': ['fake_resource_group_from_fake_id_2'], 'workspaces': []}})

        self.class_test._get_woskspace_name_dict()

        self.assertEqual(self.class_test.resources_dict, {'fake_id_1': {'name': ['fake_resource_group_from_fake_id_1'], 'workspaces': [MockWorkspace]},
                                                          'fake_id_2': {'name': ['fake_resource_group_from_fake_id_2'], 'workspaces': [MockWorkspace]}})


if __name__ == '__main__':
    unittest.main()