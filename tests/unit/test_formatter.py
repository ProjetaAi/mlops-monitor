from mlops.formatter import Formatter

def test_join_dict():
    # Define input data and configuration
    data = {'name': 'John', 'age': 30}
    config = {'id': 123, 'timestamp': '2022-03-17T12:00:00Z'}
    
    # Call the join_dict method of the Formatter class
    result = Formatter.join_dict(data, config)
    
    # Assert that the method returns the expected output
    assert result == {'name': 'John', 'age': 30, 'id': 123, 'timestamp': '2022-03-17T12:00:00Z'}
