import os
import pytest
from datadog_api_client.v2 import ApiClient, Configuration
from datadog_api_client.v2.api import logs_api
from logging import getLogger
from mlops.sender import DDHandler


@pytest.fixture
def configuration():
    return Configuration()


@pytest.fixture
def service_name():
    return "test-service"


@pytest.fixture
def ddsource():
    return "test-ddsource"


@pytest.fixture
def handler(configuration, service_name, ddsource):
    return DDHandler(configuration, service_name, ddsource)


def test_submit_log_success(handler, caplog):
    logger = getLogger("test")
    logger.addHandler(handler)

    logger.info("Test message")

    assert "Test message" in caplog.text

    api_client = ApiClient(handler.configuration)
    logs_api_instance = logs_api.LogsApi(api_client)
    response = logs_api_instance.list_logs()
    assert response.get("status") == "ok"


def test_submit_log_failure(handler, caplog):
    handler.configuration.host = "https://api.datadog-fake-host.com"
    logger = getLogger("test")
    logger.addHandler(handler)

    logger.info("Test message")

    assert "Test message" in caplog.text

    api_client = ApiClient(handler.configuration)
    logs_api_instance = logs_api.LogsApi(api_client)

    with pytest.raises(Exception) as e:
        logs_api_instance.list_logs()
        assert "Failed to establish a new connection" in str(e.value)
