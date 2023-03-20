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
def dd(configuration, service_name, ddsource):
    return DDHandler(configuration, service_name, ddsource)


def test_submit_log_success(dd, caplog):
    logger = getLogger("test")
    logger.addHandler(dd)

    logger.info("Test message")

    assert "Test message" in caplog.text


def test_submit_log_failure(dd, caplog):
    logger = getLogger("test")
    logger.addHandler(dd)

    logger.error("Test message Error")

    assert "Test message Error" in caplog.text
