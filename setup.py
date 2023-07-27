from setuptools import setup, find_packages

VERSION = '1.0.0'

datadog = ['datadog-api-client==2.10.0']
logger  = ['lodge==0.1.0']

azure_monitor_projetaai = ['projetaai-azure',
                           'pymsteams==0.2.2']

azure_monitor = ['azureml-core==1.45.0',
                 'azureml-pipeline==1.45.0',
                 'azure-ai-ml==0.1.0b4',
                 'azure-cli==2.36.0',
                 'pymsteams==0.2.2']
all = (datadog + logger + azure_monitor_projetaai)

setup(
    name='mlops-monitor',
    version=VERSION,
    description='Set of tools to work with the cloud.',
    url='https://github.com/ProjetaAi/mlops-monitor',
    author=['Juan Manoel'],
    author_email=[
        'juanengml@gmail.com'
    ],
    license='MIT',
    install_requires=datadog,
    packages=find_packages(exclude=['tests*']),
    extras_require={
        'all' : all,
        'datadog' : datadog,
        'logger'  : logger,
        'azure_monitor': azure_monitor,
        'azure_monitor_projetaai': azure_monitor_projetaai
    }
)
