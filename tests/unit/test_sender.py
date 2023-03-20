import os
import pytest
from datadog_api_client.v2.models import HTTPLogItem, HTTPLog
from datadog_api_client.v2 import Configuration
from logging import LogRecord, ERROR
from unittest.mock import MagicMock, patch
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


def test_init(handler, configuration, service_name, ddsource):
    assert isinstance(handler, DDHandler)
    assert handler.configuration == configuration
    assert handler.service_name == service_name
    assert handler.ddsource == ddsource


@patch('datadog_api_client.v2.api.logs_api.LogsApi.submit_log')
def test_emit(mock_submit_log, handler, service_name, ddsource):
    mock_submit_log.return_value = MagicMock()
    record = LogRecord(
        name="test logger",
        level=20,
        pathname="path/to/file.py",
        lineno=10,
        msg="test log message",
        args=None,
        exc_info=None,
    )
    handler.emit(record)
    mock_submit_log.assert_called_once()
    args, kwargs = mock_submit_log.call_args
    assert isinstance(args[0], HTTPLog)


