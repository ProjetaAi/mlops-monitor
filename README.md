# MLOps Monitor

A MLOps Monitor é uma biblioteca de monitoramento de Machine Learning Operations (MLOps) que permite coletar logs, métricas e dados do modelo e execução em um ambiente de produção.

## Funcionalidades

* Coletar logs (concluído)
* Coletar métricas (em andamento)
* Coletar dados do modelo e execução (em andamento)

# Uso de Logs

Os logs são informações detalhadas sobre a execução de uma aplicação. Eles são importantes para solucionar problemas, rastrear erros e garantir que o aplicativo esteja funcionando corretamente.

Para utilizar o coletor de logs da MLOps Monitor, basta importar o módulo log_collector e chamar a função collect_logs. Exemplo:

``` python
from mlops.logger import Lodge 

config = {"model": "pricing", "model_owner": "Juan Manoel", "squad": "mlops"}
console  = Lodge(config)

console.info({"test":"Olá Mundo"})

console.error({"test":"Olá Mundo"})
```

# Instalação

Para instalar a biblioteca, basta executar o seguinte comando:

``` bash
$ pip install git+https://github.com/ProjetaAi/mlops-monitor.git

```

## Passe as Variaveis de Ambiente no seu Codigo

``` python
import os
os.environ['DD_API_KEY'] = "" # Inserir a API_KEY 
os.environ['DD_SITE'] = "us5.datadoghq.com"
os.environ['ENV'] = "DEV"
os.environ['WEBHOOK_URL'] = "" # Inserir a URL do webhook que deseja enviar os alertas.

```
# Monitoramento de Workspace

O acesso dos dados de um Workspace no Azure Machine Learning necessita de autenticação. A autenticação local pode ser feita utilizando az login, no entanto, para executar no Azure Machine Learning Studio é necessário realizar a autenticação do service principal.

## Execução local

Para executar localmente basta conectar-se a Azure atravez do terminal utilizando o az login

O primeiro passo para o monitorar um Workspace no Azure Machine Learning é importar a classe PipelineFormater. 

``` python
from mlops.azureml.pipeline_monitor import PipelineFormatter
```
Em seguida, crie uma instância dessa classe e inicialize os recursos do Azure ML.

``` python
formatter = PipelineFormatter()
formatter.init_azure_resource()
```

Por fim, use-se o método ``get_pipe_by_workspace()``, que recebe como parâmetro o nome do Workspace a ser monitorado e a quantidade de horas que se deseja ler.

``` python
data = formatter.get_pipe_by_workspace('my_workspace', hours_to_monitor)
```

A saída desse método é um dicionário com as informações das pipelines que rodaram nesse ambiente durante o período selecionado, como pode-se ver no exemplo abaixo:

``` python
data = {
    'pipe_1': [
        {
            'pipe_id': '',
            'pipe_status': '',
            'pipe_start': '',
            'pipe_end': '',
            'pipe_logs': {
                'logs/azureml/executionlogs.txt': '',
                'logs/azureml/stderrlogs.txt': '',
                'logs/azureml/stdoutlogs.txt': ''
            },
            'pipe_submitted_by': ''
        }
    ],
    'pipe_2': []
}
```

## Execução no Azure Machine Learning Studio

Importe a classe de autenticação do service principal e definição de Workspace:

``` bash
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core import Workspace
```

Para autenticação é necessário configurar três variáveis de ambiente:

* tenant_id: O identificador exclusivo do tenant da Microsoft Azure.
* client_id: O identificador único do aplicativo registrado no Azure Active Directory.
* client_secret: A senha secreta associada ao aplicativo usado.

``` python
import os
tenant_id = os.environ['tenant_id']
client_id = os.environ['client_id']
client_secret = os.environ['password']

```

Passe as variáveis de ambiente a função ServicePrincipalAuthentication:

``` python
    auth = ServicePrincipalAuthentication(tenant_id=tenant_id,
                                          service_principal_id=client_id,
                                          service_principal_password=client_secret)
```
Defina o Workspace que deseja monitorar:
``` python
ws = Workspace(subscription_id='123',
               resource_group='my_resource_group',
               workspace_name='my_workspace',
               auth=auth)
```
Por fim, repita os passos anteriores, mas passando o Workspace na inicialização dos recursos do Azure ML.

``` python
formatter = PipelineFormatter()
formatter.init_azure_resource(ws=[ws])
data = formatter.get_pipe_by_workspace('aml-ipp-datascience-prd', hours_to_monitor)
```

A saída será a mesma da gerada a partir da autenticação local.

# Contribuição

Se você deseja contribuir com a biblioteca, basta seguir os seguintes passos:

* Faça um fork do repositório
* Crie uma branch para sua feature (git checkout -b minha-feature)
* Faça o commit das suas alterações (git commit -am 'Minha feature')
* Faça o push para a branch (git push origin minha-feature)
* Abra um Pull Request

# Licença

Esta biblioteca está licenciada sob a Licença MIT. Consulte o arquivo LICENSE para obter mais informações.
