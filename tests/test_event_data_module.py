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

    reader = None


@pytest.mark.no_json_test
def test_groups_created(test_grouping):
    # проверка наличия групп
    assert len(test_grouping.list_groups) > 0


@pytest.mark.no_json_test
def test_groups_check_time_between_groups(test_grouping):
    # проверка наличия порядка времени между групп
    for i in range(len(test_grouping.list_groups) - 1):
        assert test_grouping.list_groups[i].events_time < test_grouping.list_groups[i + 1].events_time


@pytest.mark.no_json_test
def test_groups_check_time_between_group_and_events(test_grouping):
    # проверка наличия соответствия даты группы и событий группы
    for group in test_grouping.list_groups:
        for event in group.events_list.events:
            assert group.events_time == event.event_time.date()


@pytest.mark.no_json_test
def test_groups_check_time_between_events(test_grouping):
    # проверка наличия соответствия сортировки событий внутри групп
    for group in test_grouping.list_groups:
        for i in range(len(group.events_list.events) - 1):
            assert group.events_list.events[i].event_time < group.events_list.events[i + 1].event_time
