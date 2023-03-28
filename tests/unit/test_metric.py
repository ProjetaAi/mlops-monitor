import os
import pytest
from datadog_api_client.v2.models import HTTPLogItem, HTTPLog
from datadog_api_client.v2 import Configuration
from logging import LogRecord, ERROR
from unittest.mock import MagicMock, patch
from mlops.sender import DDHandler, Metrics


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
def api_key():
    return "test_api_key"

@pytest.fixture
def handler(configuration, service_name, ddsource):
    return DDHandler(configuration, service_name, ddsource)

@pytest.fixture
def metric(api_key):
    return Metrics(api_key)


def test_init(metric, api_key):
    assert isinstance(metric, Metrics)
    assert metric.api_key == api_key



def test_submit_metric_success(metric, caplog):
    ret = metric.send("test_metric", 1, "increment", "test_host", "test_tags")

    assert ret == 1