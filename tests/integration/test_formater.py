import pytest
from mlops.formater import Formater

@pytest.fixture
def data():
    return {'name': 'John', 'age': 30}

@pytest.fixture
def config():
    return {'id': 123, 'timestamp': '2022-03-17T12:00:00Z'}

def test_join_dict_integration(data, config):
    result = Formater.join_dict(data, config)
    assert result == {'name': 'John', 'age': 30, 'id': 123, 'timestamp': '2022-03-17T12:00:00Z'}
