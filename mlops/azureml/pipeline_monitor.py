"""Bibliotecas utilizadas."""
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.pipeline.core.run import PipelineRun
import pandas as pd
from typing import Generator
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


config_workspace = {
                    "subscription_id": "<escreva seu subscription_id>",
                    "resource_group": "<escreva o resource_group>",
                    "workspace_name": "<escreva o workspace_name>"
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
                                    experimento: list) -> Generator:
        """Cria um gerador que contém os pipelines.

        Args:
            experiments: Lista contendo experimentos disponíveis no workspace
            position: Posição na lista, inteiro utilizado para varrer a lista

        Returns:
            Retorna uma generator contendo os pipelines de um dado experimento
        """
        name_pipeline = experimento.name
        experiment = Experiment(workspace=self.ws, name=name_pipeline)
        pipeline_list_generator = PipelineRun.list(experiment)

        return pipeline_list_generator

    def get_last_pipeline(self: "Pipeline_monitor",
                          pipeline_list_generator: Generator) -> PipelineRun:
        """Responsável por retornar a ocorrência mais recente no generator.

        Args:
            pipeline_list: generator contendo os pipelines de um experimento
        Returns:
            Retorna um azureml.pipeline.core.run.PipelineRun com dados
            do mais recente pipeline do experimento escolhido
        """
        try:
            last_pipeline = [pipeline_list_generator.__next__()]
        except StopIteration:
            last_pipeline = []

        return last_pipeline

    def get_all_pipeline(self: "Pipeline_monitor",
                         pipeline_list_generator: Generator) -> PipelineRun:
        """Gera uma lista contendo todos os pipelines de um experiment."""
        pipeline_list = (list(pipeline_list_generator))

        return pipeline_list

    def mesure_delta_time(self: "Pipeline_monitor",
                          start: str,
                          end: str) -> timedelta:
        """Retorna o tempo de execução do pipeline."""
        format = "%Y-%m-%dT%H:%M:%S.%fZ"
        try:
            dt1 = datetime.strptime(start, format)
            dt2 = datetime.strptime(end, format)
            difference = dt2 - dt1
            return difference.total_seconds()/60
        except TypeError:
            return 0

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
                'experiment_name': last_pipeline.experiment.name,
                'display_name': last_pipeline.display_name,
                'runId': pipe.get('runId'),
                'status': pipe.get('status'),
                'TimeRunning_min': self.mesure_delta_time(
                    pipe.get('startTimeUtc'), pipe.get('endTimeUtc')),
                'startTimeUtc': pipe.get('startTimeUtc'),
                'endTimeUtc': pipe.get('endTimeUtc'),
                'dt_created_run': datetime.strptime(
                    pipe.get('startTimeUtc'), "%Y-%m-%dT%H:%M:%S.%fZ").date(),
                'url_run': last_pipeline.get_portal_url()
            }

        return pipe_details

    def iterate_pipelines(self: "Pipeline_monitor",
                          pipeline_list: list) -> pd.DataFrame:
        """Itera os pipelines de uma lista."""
        pipelines_details = pd.DataFrame()
        if len(pipeline_list) > 0:
            for pipeline in pipeline_list:
                pipeline_details = self.get_pipeline_details(pipeline)
                pipeline_details_row = pd.DataFrame(pipeline_details,
                                                    index=[0])
                pipelines_details = pd.concat([pipelines_details,
                                               pipeline_details_row])

        pipelines_details = pipelines_details.reset_index(drop=True)

        return pipelines_details

    def get_steps(self: "Pipeline_monitor",
                  last_pipeline: PipelineRun) -> list:
        """Responsável por extrair os steps.

        :param last_pipeline:
        :type last_pipeline: dict
        """
        step_list = []
        for step in last_pipeline:
            try:
                step_list += list(step.get_steps())
            except IndexError:
                pass
            except AttributeError:
                pass

        return step_list

    def get_steps_details(self: "Pipeline_monitor",
                          step: list) -> dict:
        """Responsável por extrair os detalhes do step.

        Args:
            steps: child run de um pipeline
            position: variável utilizada para iterar o a lista de steps
        Returns:
            dicionário contendo os detalhes de cada step
        """
        try:
            step_dict = step.get_details()
            step_details = {
                'experiment_name': step.experiment.name,
                'step_name': step_dict.get(
                    'properties', {}).get('azureml.moduleName'),
                'display_name': step.display_name,
                'runId_step': step_dict.get('runId'),
                'status': step_dict.get('status'),
                'TimeRunning_min': self.mesure_delta_time(
                    step_dict.get('startTimeUtc'),
                    step_dict.get('endTimeUtc')),
                'startTimeUtc': step_dict.get('startTimeUtc'),
                'endTimeUtc': step_dict.get('endTimeUtc'),
                'dt_created_run': datetime.strptime(
                    step_dict.get('startTimeUtc'),
                    "%Y-%m-%dT%H:%M:%S.%fZ").date(),
                'url_run': step.get_portal_url(),
                'user_logs/std_log.txt': step_dict.get(
                    'logFiles', {}).get('user_logs/std_log.txt')
            }

        except AttributeError:
            step_details = {}

        return step_details

    def iterate_steps(self: "Pipeline_monitor",
                      step_list: list) -> pd.DataFrame:
        """Itera os steps de uma lista."""
        steps_details = pd.DataFrame()
        if len(step_list) > 0:
            for step in range(len(step_list)):
                step_details = self.get_steps_details(step_list[step])
                step_details_row = pd.DataFrame(step_details, index=[0])
                steps_details = pd.concat([steps_details, step_details_row])

        steps_details = steps_details.reset_index(drop=True)

        return steps_details

    def year_month_func(self: "Pipeline_monitor", data: datetime) -> tuple:
        """Retorna uma tupla com o ano e mês."""
        return (data.year, data.month)

    def period_filter(self: "Pipeline_monitor",
                            df: pd.DataFrame,
                            tipo: str) -> pd.DataFrame:
        """Filtra o dataframe de acordo com o período pré-selecionado."""
        today = datetime.now().date()
        last_30d = today - relativedelta(days=30)
        if tipo == 'last':
            return df

        elif tipo == 'day':
            return df[df['dt_created_run'] == today]

        elif tipo == 'last_30d':
            return df[df['dt_created_run'] >= last_30d]

        elif tipo == 'month':
            df['year_month'] = df['dt_created_run'].apply(self.year_month_func)
            return df[df['year_month'] == (today.year, today.month)]

    def experiments_filter(self: "Pipeline_monitor",
                           experimentos: list[str]) -> list:
        """Filtra os experimentos de acordo com a lista passada de input."""
        experiments_ws = self.get_experiment_list()
        if len(experimentos) == 0:
            # Coleta os experimentos disponiveis no workspace
            filtered_experiments = experiments_ws
        else:
            experiments_workspace_names = [[i, i.name] for i in experiments_ws]
            filter_experiments = [i for i in experiments_workspace_names
                                  if i[1] in experimentos]
            filtered_experiments = [i[0] for i in filter_experiments]

        return filtered_experiments

    def run(self: "Pipeline_monitor",
            tipo: str,
            experimentos: list[str] = []) -> pd.DataFrame:
        """Executa a classe Pipeline_monitor.

        Returns:
            Dois dataframes contendo os detahes dos pipeline e steps
        """
        # Executa a função
        gs = Pipeline_monitor(config_workspace)

        # Cria Workspace
        gs.create_workspace()

        # Filtra os experimentos passados como argumento, caso padrão:todos
        final_experiment_list = gs.experiments_filter(experimentos)

        # Itera os experimentos
        output_pipeline = pd.DataFrame()
        output_step = pd.DataFrame()

        for exp in final_experiment_list:
            # Cria gerador com os pipelines
            pipeline_list_generator = gs.get_pipeline_list_generator(exp)

            # Determina o tipo de rodagem
            if tipo == 'last':  # 17m50
                pipeline_list = gs.get_last_pipeline(pipeline_list_generator)
                pipeline_details = gs.iterate_pipelines(pipeline_list)
                step_lists = gs.get_steps(pipeline_list)
                step_details = gs.iterate_steps(step_lists)

                output_pipeline = pd.concat(
                    [output_pipeline, gs.period_filter(pipeline_details,
                                                       tipo)])
                output_step = pd.concat([output_step, gs.period_filter(
                    step_details, tipo)])

            elif tipo == 'day':
                pipeline_list = gs.get_all_pipeline(pipeline_list_generator)
                pipeline_details = gs.iterate_pipelines(pipeline_list)

                output_pipeline = pd.concat([output_pipeline,
                                             gs.period_filter(
                                                pipeline_details, tipo)])

            elif tipo == 'last_30d':
                pipeline_list = gs.get_all_pipeline(pipeline_list_generator)
                pipeline_details = gs.iterate_pipelines(pipeline_list)

                output_pipeline = pd.concat([output_pipeline,
                                             gs.period_filter(
                                                pipeline_details, tipo)])

            elif tipo == 'month':
                pipeline_list = gs.get_all_pipeline(pipeline_list_generator)
                pipeline_details = gs.iterate_pipelines(pipeline_list)

                output_pipeline = pd.concat([output_pipeline,
                                             self.period_filter(
                                                pipeline_details, tipo)])

        return output_pipeline, output_step
