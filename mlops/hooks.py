import pymsteams

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
    def send_teams_alert(alert_dict: dict) -> None:
        # Establishes the connection with the Teams webhook
        teams = pymsteams.connectorcard("link")
        # Extract alert information from the dictionary
        title = alert_dict["title"]
        message = alert_dict["message"]
        severity = alert_dict["severity"]

        # Generate payload
        payload = Hooks.generate_payload(title, message, severity)
        teams.payload = payload

        # Send alert
        teams.send()