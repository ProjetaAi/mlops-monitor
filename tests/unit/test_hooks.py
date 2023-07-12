import unittest
from unittest.mock import patch, MagicMock
from mlops.hooks import Hooks

class TestHooks(unittest.TestCase):
    def setUp(self):
        self.alert_dict = {
            "title": "Título do alerta",
            "message": "Mensagem do alerta",
            "severity": "high"
        }

    @patch('mlops.hooks.load_dotenv')
    @patch('mlops.hooks.os.getenv')
    def test_get_webhook(self, mock_getenv, mock_load_dotenv):
        mock_getenv.return_value = 'https://example.com/webhook'
        webhook_url = Hooks.get_webhook()
        self.assertEqual(webhook_url, 'https://example.com/webhook')

    def test_generate_payload(self):
        title = "Título do alerta"
        message = "Mensagem do alerta"
        severity = "high"

        expected_payload = {
            "text": message,
            "themeColor": "FF0000",
            "title": title
        }

        payload = Hooks.generate_payload(title, message, severity)
        self.assertEqual(payload, expected_payload)

    @patch('mlops.hooks.Hooks.generate_payload')
    @patch('mlops.hooks.Hooks.get_webhook')
    @patch('mlops.hooks.pymsteams.connectorcard')
    def test_send_teams_alert(self, mock_connectorcard, mock_get_webhook, mock_generate_payload):
        mock_get_webhook.return_value = 'https://example.com/webhook'
        mock_generate_payload.return_value = {'text': 'Test message'}

        teams_instance = MagicMock()
        mock_connectorcard.return_value = teams_instance

        Hooks.send_teams_alert(self.alert_dict)

        mock_get_webhook.assert_called_once()
        mock_generate_payload.assert_called_once_with(
            self.alert_dict['title'], self.alert_dict['message'], self.alert_dict['severity']
        )
        mock_connectorcard.assert_called_once_with('https://example.com/webhook')

        teams_instance.send.assert_called_once_with()

    def test_check_dict(self):
        alert_dict = {
            "title": "Título do alerta",
            "message": "Mensagem do alerta",
            "severity": "high"
        }
        self.assertIsNone(Hooks.check_dict(alert_dict))

        missing_title_dict = {
            "message": "Mensagem do alerta",
            "severity": "high"
        }
        with self.assertRaises(ValueError):
            Hooks.check_dict(missing_title_dict)

if __name__ == '__main__':
    unittest.main()
