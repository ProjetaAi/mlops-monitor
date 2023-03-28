import os
from datadog_api_client.v2 import ApiClient, ApiException
from datadog_api_client.v2.api import logs_api
from datadog_api_client.v2.models import *
from logging import StreamHandler

from datadog import initialize, statsd
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


class DDmetric():
    def __init__(self, api_key,):
        self.api_key = api_key

    def config(self):
        options = {
        'api_key': self.api_key,
        'statsd_host':'127.0.0.1',
        'statsd_port':8125
        }
        initialize(**options)


            

class Metrics(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.config = DDmetric(self.api_key)
        self.config.config() #inicia o ambiente de configuração do datadog

    def _publish(self, tipo, metric, value, tags, sample_rate=None):
        match tipo:
            case "increment":
                statsd.increment(metric, value, tags=tags, sample_rate=sample_rate)
            case "decrement":
                statsd.decrement(metric, value, tags=tags, sample_rate=sample_rate)
            case "gauge":
                statsd.gauge(metric, value, tags=tags, sample_rate=sample_rate)
            case "set":
                statsd.set(metric, value, tags=tags, sample_rate=sample_rate)
            case "histogram":
                statsd.histogram(metric, value, tags=tags, sample_rate=sample_rate)
            case "timer":
                statsd.timed(metric, tags=tags, sample_rate=sample_rate)
            case "distribution":
                statsd.distribution(metric, value, tags=tags, sample_rate=sample_rate)

    def send(self,tipo, metric, value, tags, sample_rate=None):
        self._publish(tipo, metric, value, tags, sample_rate)
        return 1