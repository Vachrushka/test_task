
def pytest_configure(config):
    config.addinivalue_line("markers", "no_json_test: mark test as not using JSON")
    config.addinivalue_line("markers", "use_json_test: mark test as using JSON")
    config.addinivalue_line("markers", "right_data_test: mark test as using right data")
    config.addinivalue_line("markers", "bad_data_test: mark test as using bad data")
