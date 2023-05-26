"""Arquivo de testes unitários."""
from mlops.azureml.pipeline_monitor import Pipeline_monitor


class get_details_simulation:
    """Classe utilizada para simular métodos utilizados no código real."""

    def __init__(self: "get_details_simulation") -> None:
        """."""
        self.display_name = 'sleepy_cord_4m5fdazqk'
        self.name = 'model_detection'
        self.experiment = self.experimento()

    class experimento:
        """Faz o self.experimento.name funcionar."""

        def __init__(self: "get_details_simulation") -> None:
            """."""
            self.name = 'model_detection'

    def get_details(self: "get_details_simulation") -> dict:
        """Testa o método get_details para o pipeline e para o steps."""
        output = {'display_name': 'sleepy_cord_4m5fdazqk',
                  'experiment_name': 'model_detection',
                  'runId': '7b073518-t3st-id11-9bdf-2e7805cc62fc',
                  'status': 'Completed',
                  'startTimeUtc': '2023-05-23T10:03:37.292747Z',
                  'endTimeUtc': '2023-05-23T10:05:16.930999Z',
                  'url': 'https://ml.azure.com/runs/',
                  'logFiles': {
                      'user_logs/std_log.txt':
                      'https://<storage_account_name>.blob.core'}}

        return output

    def get_portal_url(self: "get_details_simulation") -> str:
        """Testa o método get_portal_url para preencher o details."""
        output = 'https://<storage_account_name>.blob.core'

        return output

    def get_steps(self: "get_details_simulation") -> list:
        """Testa o método get_steps presente na função original."""
        lista = [1, 2, 3, 4]

        return lista


class first_n:
    """Função utilizada para simular um generator."""

    def __init__(self: "first_n", n: int) -> None:
        """."""
        self.n = n
        self.num = 0

    def __iter__(self: "first_n") -> "first_n":
        """."""
        return self

    def __next__(self: "first_n") -> int:
        """Quando executada, retornará o próximo valor da lista."""
        return self.next()

    def next(self: "first_n") -> None:
        """Responsável por iterar a lista e retornar erro."""
        if self.num < self.n:
            cur, self.num = self.num, self.num+1
            return cur
        raise StopIteration()


config_workspace = {
                    "subscription_id": "<escreva seu subscription_id>",
                    "resource_group": "<escreva o resource_group>",
                    "workspace_name": "<escreva o workspace_name>"
                }

gs = Pipeline_monitor(config_workspace=config_workspace)


def test_get_last_pipeline(workspace: object = gs) -> bool:
    """Testa o métpdp get_last_pipeline()."""
    test_argument = first_n(5)
    actual = workspace.get_last_pipeline(test_argument)
    expected = 0

    assert actual == expected


def test_get_pipelines_details(workspace: object = gs) -> bool:
    """Testa o método get_pipeline_details()."""
    test_argument = get_details_simulation()
    actual = workspace.get_pipeline_details(test_argument)
    expected = {'display_name': 'sleepy_cord_4m5fdazqk',
                'experiment_name': 'model_detection',
                'runId': '7b073518-t3st-id11-9bdf-2e7805cc62fc',
                'status': 'Completed',
                'startTimeUtc': '2023-05-23T10:03:37.292747Z',
                'endTimeUtc': '2023-05-23T10:05:16.930999Z',
                'git_branch': None,
                'url': 'https://<storage_account_name>.blob.core'}

    assert actual == expected


def test_get_steps(workspace: object = gs) -> bool:
    """Testa o método get_steps()."""
    test_argument = get_details_simulation()
    actual = workspace.get_steps(test_argument)
    expected = [1, 2, 3, 4]

    assert actual == expected


def test_get_steps_details(workspace: object = gs) -> bool:
    """Testa o método get_steps_details()."""
    test_argument = [get_details_simulation()]
    actual = workspace.get_steps_details(test_argument)
    expected = {'display_name': 'sleepy_cord_4m5fdazqk',
                'experiment_name': 'model_detection',
                'runId': '7b073518-t3st-id11-9bdf-2e7805cc62fc',
                'status': 'Completed',
                'startTimeUtc': '2023-05-23T10:03:37.292747Z',
                'endTimeUtc': '2023-05-23T10:05:16.930999Z',
                'url': 'https://<storage_account_name>.blob.core',
                'user_logs/std_log.txt':
                    'https://<storage_account_name>.blob.core'}

    assert actual == expected
