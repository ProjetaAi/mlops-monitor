# Variáveis
SOURCES_DIR = mlops
LINT_OPTIONS = --ignore=E501
MYPY_OPTIONS = --ignore-missing-imports
FLAKE8_OPTIONS = --ignore=E501

# Regras
lint:
	pylint $(LINT_OPTIONS) $(SOURCES_DIR)

mypy:
	mypy $(MYPY_OPTIONS) $(SOURCES_DIR)

flake8:
	flake8 $(FLAKE8_OPTIONS) $(SOURCES_DIR)

format:
	black $(SOURCES_DIR)

check-unit:
	python -m pytest tests/unit/

check-integration:
	python -m pytest tests/integration/

help:
	@echo "Por favor, escolha uma das seguintes regras:"
	@echo "  make lint            - Executa o Pylint em todos os arquivos fonte."
	@echo "  make mypy            - Executa o Mypy em todos os arquivos fonte."
	@echo "  make flake8          - Executa o Flake8 em todos os arquivos fonte."
	@echo "  make format          - Formata o código fonte com o Black."
	@echo "  make check-unit      - Executa os testes unitários da pasta tests/unit."
	@echo "  make check-integration - Executa os testes de integração da pasta tests/integration."

