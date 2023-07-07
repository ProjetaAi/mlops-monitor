"""Bibliotecas utilizadas."""
from azureml.core import Run, Workspace, Experiment
from azureml.pipeline.core.run import PipelineRun
from typing import Generator, Iterable, Iterator
from mlops.azureml.azure_resource import AzureWorkspaceClass
from itertools import chain, takewhile
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
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

        """
        gets the cutoff date normalized
        """

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

        return self.recursive_dict(self.azure_resource_obj.resources_dict, 'workspaces') # type: ignore

    def _get_experiments_map(self) -> Iterable[Experiment]:

        """
        gets the experiments from the workspaces
        """

        return chain.from_iterable(map(lambda workspace: Experiment.list(workspace), self._get_workspaces()))

    def _get_specific_experiment(self,
                                 name: str) -> Iterable[Experiment]:

        """
        filters the experiments by name
        """

        return filter(lambda experiment: experiment.name == name, self._get_experiments_map())

    def _filter_by_days(self, runs: Iterable[Run], days: int) -> Iterable[Run]:

        """
        given the Runs object, filter by
        the number of days we want to read
        of history
        """

        cutoff = self.get_cutoff(days)
        return takewhile(lambda run: run.get_details()['startTimeUtc'] > cutoff, runs)

    def _wrapper_experiments_runs(self) -> Iterable[Run]:

        """
        wrapper function to get the runs
        """

        return chain.from_iterable(map(lambda experiment: self._get_runs(experiment), self._get_experiments_map()))

    def _get_runs(self, experiment: Experiment) -> Iterable[Run]:

        """

        """

        return experiment.get_runs()

    def _get_runs_from_filter(self, experiment: Generator[Experiment, None, None]) -> Iterable[Run]:
        return next(experiment).get_runs()

    def _get_details_from_run(self, run: Iterable[Run]) -> Iterable[dict]:
        return map(lambda run: run.get_details(), run)

    def _get_pipe(self, name: str, days: int) -> Iterable[Run]:
        return self._filter_by_days(self._get_runs_from_filter(self._get_specific_experiment(name)), # type: ignore
                                    days)

    def get_pipe_with_details(self, name: str, days: int) -> Iterable[dict]:

        """
        generate the pipe details
        this takes a long time to run
        """

        return self._wrapper_get_details_and_step(self._get_pipe(name, days))

    def _generate_steps(self, experiment: Experiment) -> Generator[Run, None, None]:
        return PipelineRun.list(experiment)

    def _wrapper_get_details_and_step(self, experiments: Iterable[Run]):
        return self._get_details_from_run(experiments)

class PipelineFormatter(PipelineMonitor):

    _check_if_init = False
    _check_if_init_get_experiments = False

    def init_azure_resource(self):
        if not self._check_if_init:
            super().init_azure_resource()
            self._check_if_init = True
        return

    def init_get_experiments_map(self):
        if not self._check_if_init_get_experiments:
            super()._get_experiments_map()
            self._check_if_init_get_experiments = True
        return

    def __init__(self) -> None:
        pass

    def _filter_run_details(self, run_dicts: Iterable[dict]) -> list[dict]:

        """
        function that gets specific details from the run
        """

        keys = {'pipe_id': 'runId',
                'pipe_status': 'status',
                'pipe_start': 'startTimeUtc',
                'pipe_end': 'endTimeUtc',
                'pipe_logs': 'logFiles',
                'pipe_submitted_by': 'submittedBy'}

        return [{name: run_dict.get(orig_name) for name, orig_name in keys.items()} for run_dict in run_dicts]


    @timer_decorator
    def _run_azure_generators(self, name, days) -> dict:
        return list(self._filter_run_details(self.get_pipe_with_details(name, days)))

    def get_pipe(self, name, days) -> dict:
        self.init_azure_resource()
        self.init_get_experiments_map()
        return {name: self._run_azure_generators(name, days)}

    @timer_decorator
    def _run_azure_generators_thread(self, runs: Iterable[PipelineRun]) -> list[dict]:
        with ThreadPoolExecutor(max_workers=4) as executor:
            return list(executor.map(lambda run: self._filter_run_details(run.get_details()), runs))