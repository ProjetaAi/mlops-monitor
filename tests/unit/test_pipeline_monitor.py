import unittest
from unittest.mock import patch, PropertyMock
from mlops_monitor.mlops.azureml.azure_resource import AzureWorkspaceClass



class MockProfile:
    def load_cached_subscriptions(self):
        return [{'id': 'fake_id_1'}, {'id': 'fake_id_2'}]

class TestAzureVariables(unittest.TestCase):

    def setUp(self) -> None:
        self.class_test = AzureWorkspaceClass()

    def test_declare_class(self):
        self.assertIsInstance(self.class_test, AzureWorkspaceClass)

    def test_check_if_running_on_vm(self):
        self.assertFalse(self.class_test._check_if_running_on_vm())

    @patch.object(AzureWorkspaceClass, 'profile', new_callable=PropertyMock)
    def test_generate_resources_dict(self, mock_profile):
        mock_profile.return_value = MockProfile()

        self.class_test = AzureWorkspaceClass()

        resources_dict = self.class_test._generate_ids()

        self.assertEqual(resources_dict, {
            'fake_id_1': {'name': [], 'workspaces': []},
            'fake_id_2': {'name': [], 'workspaces': []},
        })
        print(self.class_test.resources_dict)
