import os
from datadog_api_client.v2 import ApiClient, ApiException
from datadog_api_client.v2.api import logs_api
from datadog_api_client.v2.models import *
from logging import StreamHandler

class DDHandler(StreamHandler):
    def __init__(self, configuration, service_name, ddsource):
        StreamHandler.__init__(self)
        self.configuration = configuration
        self.service_name = service_name
        self.ddsource = ddsource
 
    def emit(self, record):
        msg = self.format(record)
 
        with ApiClient(self.configuration) as api_client:
            api_instance = logs_api.LogsApi(api_client)
            body = HTTPLog(
                [
                    HTTPLogItem(
                        ddsource=self.ddsource,
                        ddtags="env: {}".format(
                            os.getenv("ENV"),
 
                        ),
                        message=msg,
                        service=self.service_name,
                    ),
                ]
            )
 
            try:
                # Send logs
                api_response = api_instance.submit_log(body)
            except ApiException as e:
                print("Exception when calling LogsApi->submit_log: %s\n" % e)
