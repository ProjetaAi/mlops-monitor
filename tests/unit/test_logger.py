from unittest.mock import Mock
from mlops.logger import Lodge

def test_lodge():
    # Create a mock for the Logging class
    logging_mock = Mock()

    # Create a Lodge instance with the mock
    config = {'id': 123, 'timestamp': '2022-03-17T12:00:00Z'}
    lodge = Lodge(config)
    lodge.logger = logging_mock

    # Call the info method with some data
    data = {'name': 'John', 'age': 30}
    lodge.info(data)

    # Assert that the info method of the logging_mock was called with the expected data
    logging_mock.logger.info.assert_called_once_with({'name': 'John', 'age': 30, 'id': 123, 'timestamp': '2022-03-17T12:00:00Z'})

    # Call the error method with some data
    error_data = {"error": "Something went wrong!", "id": 123, "timestamp": "2022-03-17T12:00:00Z"}
    lodge.error(error_data)

    # Assert that the error method of the logging_mock was called with the expected data
    logging_mock.logger.error.assert_called_once_with(error_data)
