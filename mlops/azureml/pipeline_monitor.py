"""Bibliotecas utilizadas."""
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.pipeline.core.run import PipelineRun
import pandas as pd
from typing import Generator


config_workspace = {
                    "subscription_id": "7deebbf6-cf9c-45b4-a02b-789e95a561b1",
                    "resource_group": "rg-ipp-datascience-dev",
                    "workspace_name": "aml-ipp-datascience-dev"
                }


class Pipeline_monitor:
    """Classe utilizada para monitorar os status dos pipelines e dos steps."""

    def __init__(self: "Pipeline_monitor", config_workspace: dict) -> None:
        """__init__.

        args:
            config_workspace: Dict contendo as chaves de acesso do workspace
        """
        self.credential = config_workspace

    def create_workspace(self: "Pipeline_monitor") -> None:
        """Cria o workspace utilizado para a execução do código."""
        self.ws = Workspace(subscription_id=self.credential['subscription_id'],
                            resource_group=self.credential['resource_group'],
                            workspace_name=self.credential['workspace_name'])

    def get_experiment_list(self: "Pipeline_monitor") -> list:
        """Extrai os experimentos do workspace.

        Returns:
            Retorna uma lista contendo os experimentos disponíveis no workspace
        """
        experiments = Experiment.list(self.ws)

        return experiments

    def get_pipeline_list_generator(self: "Pipeline_monitor",
                                    experiments: list,
                                    position: int = 12) -> Generator:
        """Cria um gerador que contém os pipelines.

        Args:
            experiments: Lista contendo experimentos disponíveis no workspace
            position: Posição na lista, inteiro utilizado para varrer a lista

        Returns:
            Retorna uma generator contendo os pipelines de um dado experimento
        """
        name_pipeline = experiments[position].name
        experiment = Experiment(workspace=self.ws, name=name_pipeline)
        pipeline_list = PipelineRun.list(experiment)

        return pipeline_list

    def get_last_pipeline(self: "Pipeline_monitor",
                          pipeline_list: Generator) -> PipelineRun:
        """Responsável por retornar a ocorrência mais recente no generator.

        Args:
            pipeline_list: generator contendo os pipelines de um experimento
        Returns:
            Retorna um azureml.pipeline.core.run.PipelineRun com dados
            do mais recente pipeline do experimento escolhido
        """
        last_pipeline = pipeline_list.__next__()

        return last_pipeline

    def get_pipeline_details(self: "Pipeline_monitor",
                             last_pipeline: PipelineRun) -> dict:
        """Responsável por extrair os detalhes do pipeline.

        Args:
            last_pipeline: um azureml.pipeline.core.run.PipelineRun com dados
            do mais recente pipeline do experimento escolhido
        Returns:
            Retorna um dict contendo as informações escohidas
        """
        if last_pipeline != 0:
            pipe = last_pipeline.get_details()
            pipe_details = {
                'display_name': last_pipeline.display_name,
                'experiment_name': last_pipeline.experiment.name,
                'runId': pipe.get('runId'),
                'status': pipe.get('status'),
                'startTimeUtc': pipe.get('startTimeUtc'),
                'endTimeUtc': pipe.get('endTimeUtc'),
                'git_branch': pipe.get(
                    'properties', {}).get('azureml.git.branch'),
                'url': last_pipeline.get_portal_url()
            }
        return pipe_details

    def get_steps(self: "Pipeline_monitor",
                  last_pipeline: PipelineRun) -> list:
        """Responsável por extrair os steps.

        :param last_pipeline:
        :type last_pipeline: dict
        """
        try:
            steps = list(last_pipeline.get_steps())
        except steps .DoesNotExist:
            steps = []

        return steps

    def get_steps_details(self: "Pipeline_monitor",
                          steps: list,
                          position: int = 0) -> dict:
        """Responsável por extrair os detalhes do step.

        Args:
            steps: child run de um pipeline
            position: variável utilizada para iterar o a lista de steps
        Returns:
            dicionário contendo os detalhes de cada step
        """
        if len(steps) > 0:
            step = steps[position].get_details()
            step_details = {
                'display_name': steps[position].display_name,
                'experiment_name': steps[position].experiment.name,
                'runId': step.get('runId'),
                'status': step.get('status'),
                'startTimeUtc': step.get('startTimeUtc'),
                'endTimeUtc': step.get('endTimeUtc'),
                'url': steps[position].get_portal_url(),
                'user_logs/std_log.txt': step.get(
                    'logFiles', {}).get('user_logs/std_log.txt')
            }

        return step_details


def create_dataframe() -> pd.DataFrame:
    """Executa a classe Pipeline_monitor.

    Returns:
        Dois dataframes contendo os detahes do pipeline e detalhes dos steps
    """
    # Executa a função
    gs = Pipeline_monitor(config_workspace)

    # Cria Workspace
    gs.create_workspace()

    # Cria lista experimentos
    experiment_list = gs.get_experiment_list()
    pipelines_details = pd.DataFrame()
    steps_details = pd.DataFrame()

    for i in range(len(experiment_list)):
        try:
            # Cria gerador com os pipelines
            pipeline_list = gs.get_pipeline_list_generator(experiment_list,
                                                           position=i)

            # Obtém o último pipeline
            last_pipe = gs.get_last_pipeline(pipeline_list)

            # Obtem detalhes dos pipelines
            pipeline_details = gs.get_pipeline_details(last_pipe)
            pipeline_details_row = pd.DataFrame(pipeline_details,
                                                index=[0])
            pipelines_details = pd.concat([pipelines_details,
                                           pipeline_details_row])

            # Cria gerador com os steps
            steps = gs.get_steps(last_pipe)

            # Obtem detalhes dos steps
            for j in range(len(steps)):
                step_details = gs.get_steps_details(steps, position=j)
                step_details_row = pd.DataFrame(step_details, index=[0])
                steps_details = pd.concat([steps_details, step_details_row])
        except Exception:
            continue

    return pipelines_details, steps_details


#dataframe = create_dataframe()

#dataframe[1].experiment_name.nunique()
