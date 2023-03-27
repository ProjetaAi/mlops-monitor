# MLOps Monitor

A MLOps Monitor é uma biblioteca de monitoramento de Machine Learning Operations (MLOps) que permite coletar logs, métricas e dados do modelo e execução em um ambiente de produção.

## Funcionalidades

* Coletar logs (concluído)
* Coletar métricas (concluído)
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

# Uso de métricas
Este pacote disponibiliza a criação de métricas do DataDog. Estas são importantes para medir diversas informações e acompanhar evoluções dos dados.

Para sua utilização, tenha em mãos uma chave da API do DataDog e utilize a biblioteca. Exemplo:

```python
from mlops.sender import DDmetric

dd = DDmetric(api_key)

dd.send(tipo, nome, valor,tags,sample_rate)

```
Os tipos de métricas podem ser encontrados [aqui](https://docs.datadoghq.com/metrics/custom_metrics/dogstatsd_metrics_submission/).
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
```
# Contribuição

Se você deseja contribuir com a biblioteca, basta seguir os seguintes passos:

* Faça um fork do repositório
* Crie uma branch para sua feature (git checkout -b minha-feature)
* Faça o commit das suas alterações (git commit -am 'Minha feature')
* Faça o push para a branch (git push origin minha-feature)
* Abra um Pull Request

# Licença

Esta biblioteca está licenciada sob a Licença MIT. Consulte o arquivo LICENSE para obter mais informações.
