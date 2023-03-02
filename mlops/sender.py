from datadog_api_client.v2 import ApiClient, ApiException, Configuration
from datadog_api_client.v2.api import logs_api
from datadog_api_client.v2.models import *


class DatadogLogger:
    def __init__(self, configuration, service_name, ddsource):
        self.configuration = configuration
        self.service_name = service_name
        self.ddsource = ddsource

    def log(self, message):
        with ApiClient(self.configuration) as api_client:
            api_instance = logs_api.LogsApi(api_client)
            body = HTTPLog(
                [
                    HTTPLogItem(
                        ddsource=self.ddsource,
                        ddtags=f"env:{os.getenv('ENV')}",
                        message=message,
                        service=self.service_name,
                    ),
                ]
            )

            try:
                # Send logs
                api_response = api_instance.submit_log(body)
            except ApiException as e:
                logging.error("Exception when calling LogsApi->submit_log: %s\n", e)

