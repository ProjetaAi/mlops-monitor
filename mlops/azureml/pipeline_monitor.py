"""Bibliotecas utilizadas."""
from azureml.core import Run, Workspace, Experiment
from azureml.pipeline.core.run import PipelineRun
from typing import Generator, Iterable, Iterator
from mlops_monitor.mlops_monitor.mlops.azureml.azure_resource import AzureWorkspaceClass
from itertools import chain, takewhile
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # start timer
        result = func(*args, **kwargs)    # execute the function
        end_time = time.perf_counter()    # stop timer
        run_time = end_time - start_time  # calculate run time
        print(f"Function {func.__name__!r} executed in {run_time:.4f} seconds")
        return result
    return wrapper


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

    def recursive_dict(self,
                       d: dict,
                       until_k: str) -> Iterable[dict]:

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

    def get_cutoff(self, days: int) -> str:
        today = datetime.now().date()
        cutoff = (today - timedelta(days=days)).strftime('%Y-%m-%d')
        return cutoff

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

    def _filter_by_days(self, runs: Iterable[Run], days: int) -> Iterable[Run]:
        cutoff = self.get_cutoff(days)
        return takewhile(lambda run: run.get_details()['startTimeUtc'] > cutoff, runs)

    def _wrapper_experiments_runs(self) -> Iterator[Iterable[Run]]:
        return map(lambda experiment: self._get_runs(experiment),
                   chain.from_iterable(self._get_experiments_map()))

    def _get_runs(self, experiment: Experiment) -> Iterable[Run]:
        return experiment.get_runs()

    def _get_runs_from_filter(self, experiment: Generator[Experiment, None, None]) -> Iterable[Run]:
        return next(experiment).get_runs()

    def _get_steps(self, run: Iterable[Run]) -> Iterable[dict]:
        return map(lambda run: run.get_details(), run)

    def get_pipe(self, name: str, days: int) -> Iterable[Run]:
        return self._filter_by_days(self._get_runs_from_filter(self._get_specific_experiment(name)),
                                    days)

class PipelineFormatter(PipelineMonitor):

    def __init__(self) -> None:
        pass

    def _filter_run_details(self, d: dict):

        """
        function that gets specific details from the run
        """

        keys = {'pipe_id': 'runId',
                'pipe_status': 'status',
                'pipe_start': 'startTimeUtc',
                'pipe_end': 'endTimeUtc',
                'pipe_logs': 'logFiles',
                'pipe_submitted_by': 'submittedBy'}

        return {name: d.get(orig_name) for name, orig_name in keys.items()}

    @timer_decorator
    def _run_azure_generators(self, runs: Iterable[PipelineRun]) -> list[dict]:
        return list(map(lambda run: self._filter_run_details(run.get_details()), runs))

    @timer_decorator
    def _run_azure_generators_thread(self, runs: Iterable[PipelineRun]) -> list[dict]:
        with ThreadPoolExecutor(max_workers=4) as executor:
            return list(executor.map(lambda run: self._filter_run_details(run.get_details()), runs))