from datetime import datetime
import pytest
from Factory import EventFactory
from EventTypes import EventType
from JsonReader import JsonReader


# глобальные фикстуры
@pytest.fixture(scope="module")
def global_resource():

    ev = EventFactory(datetime(2023, 7, 26), datetime(2023, 7, 28))
    event_list = ev.generate_events_list(200)

    return event_list


@pytest.mark.no_json_test
def test_delete_type_other(global_resource):
    # проверка удаления событий типа other
    have_other = check_other_event(global_resource)

    if have_other:
        global_resource.delete_type_other()
        assert check_other_event(global_resource) is False


def check_other_event(global_resource):
    have_other = False
    for event in global_resource.events:
        if event.event_type == EventType.OTHER:
            have_other = True
            break
    return have_other


@pytest.fixture(scope="function")
def test_grouping(global_resource):
    # создание объекта для тестирования
    reader = JsonReader(None, None)
    reader.list_events = global_resource
    reader.group_by_time_events()

    yield reader


@pytest.mark.no_json_test
def test_groups_created(test_grouping):
    # проверка наличия групп
    assert len(test_grouping.dict_groups) > 0


@pytest.mark.no_json_test
def test_groups_check_time_between_groups(test_grouping):
    # проверка наличия порядка времени между групп
    date_list = list(test_grouping.dict_groups.keys())

    for i in range(len(date_list) - 1):
        assert date_list[i] < date_list[i + 1]


@pytest.mark.no_json_test
def test_groups_check_time_between_group_and_events(test_grouping):
    # проверка наличия соответствия даты группы и событий группы
    for date, event_list in test_grouping.dict_groups.items():
        for event in event_list:
            assert date == event.event_time.date()


@pytest.mark.no_json_test
def test_groups_check_time_between_events(test_grouping):
    # проверка наличия соответствия сортировки событий внутри групп
    for event_list in test_grouping.dict_groups.values():
        for i in range(len(event_list) - 1):
            assert event_list[i].event_time < event_list[i + 1].event_time
