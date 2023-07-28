import pprint
from mlops.azureml.pipeline_monitor import PipelineFormatter


obj = PipelineFormatter()
obj.init_azure_resource()
# list_obj = list(obj._get_last_from_workspace('aml-ipp-datascience-prd', 1))
# print(list_obj)
#list_obj = list(obj._get_last_from_workspace('aml-ipp-datascience-prd', 1))
list_obj = obj.get_pipe_by_workspace('aml-ipp-datascience-prd', 24)#[2:]
pprint.pprint(list_obj)
#pprint.pprint(obj._filter_run_details(obj._run_generator(list_obj)))
#pprint.pprint([obj._run_generator(i) for i in list_obj])
#pprint.pprint(obj._filter_run_details())