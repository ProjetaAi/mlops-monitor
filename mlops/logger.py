import os
import time
import logging
from logging import StreamHandler
from mlops.logger import DatadogLogger

class DDHandler(StreamHandler):
    def __init__(self, configuration, service_name, ddsource):
        super().__init__()
        self.datadog_logger = DatadogLogger(configuration, service_name, ddsource)

    def emit(self, record):
        message = self.format(record)
        self.datadog_logger.log(message)


class Logde(object):
    def __init__(self, service_name, ddsource, logger_name='demoapp'):
 
        self.service_name = service_name
        self.ddsource = ddsource
        self.logger_name = logger_name
 
 
        self.configuration = Configuration()
        format = "[%(asctime)s] %(name)s %(levelname)s %(message)s"
        self.logger = logging.getLogger(self.logger_name)
        formatter = logging.Formatter(
            format,
        )
 
        # Logs to Datadog
        dd = DDHandler(self.configuration, service_name=self.service_name,ddsource=self.ddsource)
        dd.setLevel(logging.INFO)
        dd.setFormatter(formatter)
        self.logger.addHandler(dd)
 
        if logging.getLogger().hasHandlers():
            logging.getLogger().setLevel(logging.INFO)
        else:
            logging.basicConfig(level=logging.INFO)

class Logging:
    def __init__(self, service_name, ddsource, logger_name='demoapp'):
        self.logger = Logde(service_name='first-service', ddsource='source1', logger_name='demoapp') 
    
    def info(self, message):
        self.logger.logger.info(message)

if __name__ == "__main__":
    logger = Logging(service_name='first-service', ddsource='source1', logger_name='demoapp') 
    logger.info({"test":"Ola Mundo"})
