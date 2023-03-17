import logging
from mlops.sender import DDHandler
from datadog_api_client.v2 import Configuration
from mlops.formater import Formater

class Logging(object):
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

class Lodge(object):
    def __init__(self, config):
        self.ddsource = 'mlops-source'
        self.service_name = 'mlops'
        self.logger_name = 'coe'
        self.logger = Logging(
                        service_name=self.service_name, 
                        ddsource=self.ddsource, 
                        logger_name=self.logger_name)
        self.config = config

    def info(self, data):
        data = Formater.join_dict(data, self.config)
        self.logger.logger.info(data)

    def error(self, data):
        data = Formater.join_dict(data, self.config)
        self.logger.logger.error(data)    