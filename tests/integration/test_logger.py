import pytest
from mlops.logger import Lodge

@pytest.fixture
def lodge():
    return Lodge({'key': 'value'})

def test_lodge_info(lodge, caplog):
    data = {'info': 'test'}
    lodge.info(data)
    assert 'test' in caplog.text

def test_lodge_error(lodge, caplog):
    data = {'error': 'test'}
    lodge.error(data)
    assert 'test' in caplog.text
