import pytest
from unittest.mock import MagicMock
from mlops.hooks import Hooks


@pytest.fixture
def mock_get_webhook(monkeypatch):
    # Mock the get_webhook method to return a test webhook URL
    def mock_get_webhook():
        return "https://example.com/webhook"

    monkeypatch.setattr(Hooks, "get_webhook", mock_get_webhook)


@pytest.fixture
def mock_connectorcard(monkeypatch):
    # Mock the pymsteams.connectorcard class to avoid making actual connections
    class MockConnectorCard:
        def __init__(self, webhook_url):
            pass

        def send(*args, **kwargs):
            pass

    mock = MagicMock(return_value=MockConnectorCard)
    monkeypatch.setattr("mlops.hooks.pymsteams.connectorcard", mock)


def test_generate_payload():
    # Test the generate_payload method
    title = "Test Title"
    message = "Test Message"
    severity = "high"

    payload = Hooks.generate_payload(title, message, severity)

    assert payload["title"] == title
    assert payload["text"] == message
    assert payload["themeColor"] == "FF0000"


def test_check_dict():
    # Test the check_dict method with a valid dictionary
    alert_dict = {
        "title": "Test Title",
        "message": "Test Message",
        "severity": "high"
    }

    Hooks.check_dict(alert_dict)  # Should not raise any exceptions


def test_check_dict_missing_fields():
    # Test the check_dict method with missing fields
    alert_dict = {
        "title": "Test Title",
        "severity": "high"
    }

    with pytest.raises(ValueError) as e:
        Hooks.check_dict(alert_dict)

    assert str(e.value) == "Os seguintes campos estão faltando: message"


def test_send_teams_alert(mock_get_webhook, mock_connectorcard):
    # Test the send_teams_alert method
    alert_dict = {
        "title": "Test Title",
        "message": "Test Message",
        "severity": "high"
    }

    Hooks.send_teams_alert(alert_dict)  # Should not raise any exceptions


def test_send_teams_alert_missing_fields(mock_get_webhook, mock_connectorcard):
    # Test the send_teams_alert method with missing fields
    alert_dict = {
        "title": "Test Title",
        "severity": "high"
    }

    with pytest.raises(ValueError) as e:
        Hooks.send_teams_alert(alert_dict)

    assert str(e.value) == "Os seguintes campos estão faltando: message"
