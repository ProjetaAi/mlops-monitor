"""This file contains the definition of the "Hooks" class.

Which provides functionalities for sending alerts to Teams.
"""

import pymsteams
from dotenv import load_dotenv
import os


class Hooks:
    """A class that provides functionalities for sending alerts to Teams.

    This class includes methods for generating payload, retrieving
    the webhook URL, checking the required fields in the alert
    dictionary, and sending the alert to Teams using the pymsteams library.
    """

    @staticmethod
    def generate_payload(title: str, message: str, severity: str) -> dict:
        """Generate the payload for a Teams alert.

        Args:
            title (str): The title of the alert.
            message (str): The message content of the alert.
            severity (str): The severity level of the alert.

        Returns:
            dict: The generated payload dictionary for the Teams alert.
        """
        severity_colors = {
            "high": "FF0000",   # Red color
            "medium": "FFA500",  # Orange color
            "low": "FFFF00"      # Yellow color
        }

        color = severity_colors.get(severity, "FFFFFF")  # Default to white

        payload = {
            "text": message,
            "themeColor": color,
            "title": title,
        }

        return payload

    @staticmethod
    def get_webhook() -> str:
        """
        Retrieve the webhook URL from the environment.

        Returns:
            str: The webhook URL retrieved from the environment.
        """
        load_dotenv()
        return os.getenv('WEBHOOK_URL')

    @staticmethod
    def check_dict(alert_dict: dict) -> None:
        """
        Check if the required fields are present in the alert dictionary.

        Args:
            alert_dict (dict): The dictionary representing the alert.

        Raises:
            ValueError: If any of the required fields are missing.
        """
        required_fields = ["title", "message", "severity"]
        missing_fields = [field for field in required_fields
                          if field not in alert_dict]

        if missing_fields:
            error_message = ("Campos faltando: {}"
                             .format(", ".join(missing_fields)))
            raise ValueError(error_message)

    @staticmethod
    def send_teams_alert(alert_dict: dict) -> None:
        """
        Send an alert to Teams using the provided alert dictionary.

        Args:
            alert_dict (dict): The dictionary representing the alert.
                It must contain the following fields:
                - "title": The title of the alert.
                - "message": The message content of the alert.
                - "severity": The severity level of the alert.

        Raises:
            ValueError: If any of the required fields are missing in
            the alert dictionary.
        """
        # Check dictionary fields.
        Hooks.check_dict(alert_dict)

        # Establishes the connection with the Teams webhook
        teams = pymsteams.connectorcard(Hooks.get_webhook())

        # Extract alert information from the dictionary
        title = alert_dict["title"]
        message = alert_dict["message"]
        severity = alert_dict["severity"]

        # Generate payload
        payload = Hooks.generate_payload(title, message, severity)
        teams.payload = payload

        # Send alert
        teams.send()
