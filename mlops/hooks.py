import pymsteams
from dotenv import load_dotenv
import os
import logging


class Hooks:

    @staticmethod
    def generate_payload(title: str, message: str, severity: str) -> dict:
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
        #Load environment and return webhook str.

        load_dotenv()
        return os.getenv('WEBHOOK_URL')
    
    @staticmethod
    def check_dict(alert_dict: dict) -> str:
        # Check input.
        required_fields = ["title", "message", "severity"]
        missing_fields = [field for field in required_fields if field not in alert_dict]

        if missing_fields:
            error_message = f"Os seguintes campos estão faltando: {', '.join(missing_fields)}"
            raise ValueError(error_message)

    @staticmethod
    def send_teams_alert(alert_dict: dict) -> None: 
        #Check dictionary fields.
        try:
            Hooks.check_dict(alert_dict)
        except ValueError as e:
            logging.error(e)
            raise ValueError(e)
        
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
        