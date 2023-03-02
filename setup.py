from setuptools import setup, find_packages

VERSION = '1.0.0'

datadog = ['datadog-api-client==2.10.0']
logger  = ['lodge==0.1.0']

all = (datadog + logger)

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
        'logger'  : logger
    }
)
