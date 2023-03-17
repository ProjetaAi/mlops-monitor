import os
import pytest
from datadog_api_client.v2.models import HTTPLogItem, HTTPLog
from logging import LogRecord
from unittest.mock import MagicMock, patch
from mlops.sender import DDHandler


@pytest.fixture
def configuration():
    return MagicMock()


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
    assert isinstance(args[0].logs[0], HTTPLogItem)
    assert args[0].logs[0].ddsource == ddsource
    assert f"env: {os.getenv('ENV')}" in args[0].logs[0].ddtags
    assert args[0].logs[0].message == record.msg
    assert args[0].logs[0].service == service_name


@patch('datadog_api_client.v2.api.logs_api.LogsApi.submit_log')
def test_emit_exception(mock_submit_log, handler, caplog):
    mock_submit_log.side_effect = Exception("API error")
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
    assert "Exception when calling LogsApi->submit_log" in caplog.text
