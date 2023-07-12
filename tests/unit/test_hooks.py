"""Unit test file for the mlops.hooks module."""

import pytest
from unittest.mock import MagicMock
from mlops.hooks import Hooks
from typing import Any


@pytest.fixture
def mock_get_webhook(monkeypatch: Any) -> None:
    """Mock the get_webhook method to return a test webhook URL."""
    def mock_get_webhook() -> str:
        return "https://example.com/webhook"

    monkeypatch.setattr(Hooks, "get_webhook", mock_get_webhook)


@pytest.fixture
def mock_connectorcard(monkeypatch: Any) -> None:
    """Mock the connectorcard class to avoid making actual connections."""
    class MockConnectorCard:
        def __init__(self: Any) -> None:
            pass

        def send(*args: Any) -> None:
            pass

    mock = MagicMock(return_value=MockConnectorCard)
    monkeypatch.setattr("mlops.hooks.pymsteams.connectorcard", mock)


def test_generate_payload() -> None:
    """Test the generate_payload method."""
    # Test case setup
    title = "Test Title"
    message = "Test Message"
    severity = "high"

    # Generate payload
    payload = Hooks.generate_payload(title, message, severity)

    # Assertion
    assert payload["title"] == title
    assert payload["text"] == message
    assert payload["themeColor"] == "FF0000"


def test_check_dict() -> None:
    """Test the check_dict method with a valid dictionary."""
    # Test case setup
    alert_dict = {
        "title": "Test Title",
        "message": "Test Message",
        "severity": "high"
    }

    # Call check_dict method
    Hooks.check_dict(alert_dict)  # Should not raise any exceptions


def test_check_dict_missing_fields() -> None:
    """Test the check_dict method with missing fields."""
    # Test case setup
    alert_dict = {
        "title": "Test Title",
        "severity": "high"
    }

    # Call check_dict method and assert exception
    with pytest.raises(ValueError) as e:
        Hooks.check_dict(alert_dict)

    assert str(e.value) == "Campos faltando: message"


def test_send_teams_alert() -> None:
    """Test the send_teams_alert method."""
    # Test case setup
    alert_dict = {
        "title": "Test Title",
        "message": "Test Message",
        "severity": "high"
    }

    # Call send_teams_alert method
    Hooks.send_teams_alert(alert_dict)  # Should not raise any exceptions


def test_send_teams_alert_missing_fields() -> None:
    """Test the send_teams_alert method with missing fields."""
    # Test case setup
    alert_dict = {
        "title": "Test Title",
        "severity": "high"
    }

    # Call send_teams_alert method and assert exception
    with pytest.raises(ValueError) as e:
        Hooks.send_teams_alert(alert_dict)

    assert str(e.value) == "Campos faltando: message"
