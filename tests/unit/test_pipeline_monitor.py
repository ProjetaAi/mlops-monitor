"""Arquivo de testes unitários."""
from mlops.azureml.pipeline_monitor import Pipeline_monitor
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta


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
        output = {
                  'experiment_name': 'model_detection',
                  'properties': {'azureml.moduleName': 'nome'},
                  'display_name': 'sleepy_cord_4m5fdazqk',
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


class a:
    """Classe simulada."""

    def __init__(self: "get_details_simulation") -> None:
        """Simula atributo name."""
        self.name = 'a'


class b:
    """Classe simulada."""

    def __init__(self: "get_details_simulation") -> None:
        """Simula atributo name."""
        self.name = 'b'


class c:
    """Classe simulada."""

    def __init__(self: "get_details_simulation") -> None:
        """Simula atributo name."""
        self.name = 'c'


config_workspace = {
                    "subscription_id": "<escreva seu subscription_id>",
                    "resource_group": "<escreva o resource_group>",
                    "workspace_name": "<escreva o workspace_name>"
                }

gs = Pipeline_monitor(config_workspace=config_workspace)


def test_get_last_pipeline(workspace: object = gs) -> bool:
    """Testa o método get_last_pipeline()."""
    test_argument = first_n(5)
    actual = workspace.get_last_pipeline(test_argument)
    expected = [0]

    assert actual == expected


def test_get_pipelines_details(workspace: object = gs) -> bool:
    """Testa o método get_pipeline_details()."""
    test_argument = get_details_simulation()
    actual = workspace.get_pipeline_details(test_argument)
    expected = {'experiment_name': 'model_detection',
                'display_name': 'sleepy_cord_4m5fdazqk',
                'runId_pipeline': '7b073518-t3st-id11-9bdf-2e7805cc62fc',
                'status': 'Completed',
                'TimeRunning_min': 1.6606375333333332,
                'startTimeUtc': '2023-05-23T10:03:37.292747Z',
                'endTimeUtc': '2023-05-23T10:05:16.930999Z',
                'dt_created_run': datetime.strptime(
                    '2023-05-23T10:03:37.292747Z',
                    "%Y-%m-%dT%H:%M:%S.%fZ").date(),
                'url_run': 'https://<storage_account_name>.blob.core'}

    assert actual == expected


def test_get_steps(workspace: object = gs) -> bool:
    """Testa o método get_steps()."""
    test_argument = [get_details_simulation()]
    actual = workspace.get_steps(test_argument)
    expected = [1, 2, 3, 4]

    assert actual == expected


def test_get_steps_details(workspace: object = gs) -> bool:
    """Testa o método get_steps_details()."""
    test_argument = get_details_simulation()
    actual = workspace.get_steps_details(test_argument)
    expected = {'experiment_name': 'model_detection',
                'step_name': 'nome',
                'display_name': 'sleepy_cord_4m5fdazqk',
                'runId_step': '7b073518-t3st-id11-9bdf-2e7805cc62fc',
                'status': 'Completed',
                'TimeRunning_min': 1.6606375333333332,
                'startTimeUtc': '2023-05-23T10:03:37.292747Z',
                'endTimeUtc': '2023-05-23T10:05:16.930999Z',
                'dt_created_run': datetime.strptime(
                    '2023-05-23T10:03:37.292747Z',
                    "%Y-%m-%dT%H:%M:%S.%fZ").date(),
                'url_run': 'https://<storage_account_name>.blob.core',
                'user_logs/std_log.txt':
                    'https://<storage_account_name>.blob.core'}

    assert actual == expected


def test_get_all_pipeline(workspace: object = gs) -> bool:
    """Testa o método get_all_pipeline()."""
    test_argument = first_n(5)
    actual = workspace.get_all_pipeline(test_argument)
    expected = [0, 1, 2, 3, 4]

    assert actual == expected


def test_mesure_delta_time(workspace: object = gs) -> bool:
    """Testa o método mesure_delta_time()."""
    test_argument_1 = "2020-03-04T20:15:10.345678Z"
    test_argument_2 = "2020-03-04T21:45:10.346754Z"
    actual = workspace.mesure_delta_time(test_argument_1, test_argument_2)
    expected = 90.00001793333333

    assert actual == expected


def test_year_month_func(workspace: object = gs) -> bool:
    """Testa o método year_month_func()."""
    format = "%Y-%m-%dT%H:%M:%S.%fZ"
    test_argument = datetime.strptime("2020-03-04T20:15:10.345678Z", format)
    actual = workspace.year_month_func(test_argument)
    expected = (2020, 3)

    assert actual == expected


def test_period_filter(workspace: object = gs) -> bool:
    """Testa o método period_filter()."""
    date_1 = datetime.now().date() - relativedelta(months=1)
    date_2 = datetime.now().date()
    date_3 = datetime.now().date()

    test_argument_1 = pd.DataFrame({'dt_created_run': [date_1, date_2, date_3],
                                    'id': ['teste1', 'teste2', 'teste3']})
    test_argument_2 = 'month'
    actual = workspace.period_filter(
        test_argument_1, test_argument_2).to_dict()
    expected = test_argument_1.drop(0).to_dict()

    assert actual == expected


def test_experiments_filter(workspace: object = gs) -> bool:
    """Testa o método experiments_filter()."""
    exp_a, exp_b, exp_c = a(), b(), c()
    test_argument_1 = ['a', 'c']
    test_argument_2 = [exp_a, exp_b, exp_c]
    actual = workspace.experiments_filter(test_argument_1, test_argument_2)
    expected = [exp_a, exp_c]

    assert actual == expected
