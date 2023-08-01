from datetime import datetime
import pytest
from Factory import EventFactory
from JsonReader import JsonReader


@pytest.fixture(scope="module")
def test_create_right_json():
    ef = EventFactory(datetime(2023, 7, 24), datetime(2023, 7, 31))
    ef.generate_json(100)
    return ef


@pytest.fixture(scope="function")
def test_check_load(test_create_right_json):
    # создание объекта для тестирования
    ef = test_create_right_json
    reader = JsonReader(ef.input_path, None)
    reader.load_json_data()

    yield ef, reader


@pytest.mark.right_data_test
@pytest.mark.use_json_test
def test_is_not_empty(test_check_load):
    _, reader = test_check_load
    # проверка наличия загруженных евентов
    assert len(reader.list_events.events) > 0


@pytest.mark.right_data_test
@pytest.mark.use_json_test
def test_is_right_range(test_check_load):
    ev, reader = test_check_load
    # проверка совпадения дипазона дат
    for event in reader.list_events.events:
        assert ev.start_date.date() <= event.event_time.date() <= ev.end_date.date()


@pytest.mark.parametrize("event_time, event_type, event_name", [
    (None,                      "private", "name"),
    (1,                         "private", "name"),
    ("datetime(2021, 2, 24)",   "private", "name"),
    ("00:00:00T2021-02-24",     "private", "name"),
    ("24/07/2023",              "private", "name"),
    ("July 24, 2023",           "private", "name"),
    ("24-07-2023",              "private", "name"),
    ("07/24/23",                "private", "name"),
    ("24 July 2023",            "private", "name"),
    ("24/07/23",                "private", "name"),
    ("July 24, 2023 12:34 PM",  "private", "name"),

    (datetime(2021, 2, 24), "private1",             "name"),
    (datetime(2021, 2, 24), None,             "name"),
    (datetime(2021, 2, 24), 1,                      "name"),
    (datetime(2021, 2, 24), datetime(2021, 2, 24),  "name"),

    (datetime(2021, 2, 24), "private",  "123456789012345678901"),
    (datetime(2021, 2, 24), "private",  "12345678901234567890 123456789012345678901"),
    (datetime(2021, 2, 24), "private",  "12345 "*20),
    (datetime(2021, 2, 24), "private",  ""),
    (datetime(2021, 2, 24), "private",  None),
    (datetime(2021, 2, 24), "private",  "$"),
    (datetime(2021, 2, 24), "private",  "="),
    (datetime(2021, 2, 24), "private",  ['n', 'a', 'm', 'e']),
])
@pytest.mark.bad_data_test
def test_bad_json_data(event_time, event_type, event_name):
    ef = EventFactory(None, None)
    ev_list = ef.generate_event_from_data(event_time, event_type, event_name)
    ef.generate_json(event=ev_list)

    reader = JsonReader(ef.input_path, None)
    with pytest.raises(ValueError):
        reader.load_json_data()
