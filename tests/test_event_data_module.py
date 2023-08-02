import json
from collections import defaultdict
from datetime import datetime
import pytest

from Event import Event
from Factory import EventFactory
from EventTypes import EventType
from DataManager import DataManager


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
    manager = DataManager(None, None)
    manager.list_events = global_resource
    manager.group_by_time_events()

    yield manager


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
            assert event_list[i].event_time <= event_list[i + 1].event_time


@pytest.fixture(scope="function", params=[
    ([[datetime(2023, 7, 25, 1), -300],
      [datetime(2023, 7, 25, 1), -480],
      [datetime(2023, 7, 26, 23), 480],
      [datetime(2023, 7, 24, 23), 480],
      [datetime(2023, 7, 30, 11), 180],
      [datetime(2023, 7, 29, 17), 120],
      [datetime(2023, 7, 29, 11), 300],
      [datetime(2023, 7, 30, 13), 240],
      [datetime(2023, 7, 30, 12), -120],
      [datetime(2023, 7, 30, 12), -120]

      ],
     {
         datetime(2023, 7, 24): [[datetime(2023, 7, 24, 23), 480]],
         datetime(2023, 7, 25): [[datetime(2023, 7, 25, 1), -300], [datetime(2023, 7, 25, 1), -480]],
         datetime(2023, 7, 26): [[datetime(2023, 7, 26, 23), 480]],
         datetime(2023, 7, 29): [[datetime(2023, 7, 29, 11), 300], [datetime(2023, 7, 29, 17), 120]],
         datetime(2023, 7, 30): [[datetime(2023, 7, 30, 11), 180], [datetime(2023, 7, 30, 13), 240],
                                 [datetime(2023, 7, 30, 12), -120], [datetime(2023, 7, 30, 12), -120]]
     }
     ),
    ([[datetime(2023, 7, 24, 1), 300],
      [datetime(2023, 7, 24, 23), 300],
      [datetime(2023, 7, 25, 1), 300],
      [datetime(2023, 7, 25, 23), 300],
      [datetime(2023, 7, 24, 1), -300],
      [datetime(2023, 7, 24, 23), -300],
      [datetime(2023, 7, 25, 1), -300],
      [datetime(2023, 7, 25, 23), -300]
      ],

     {
         datetime(2023, 7, 24): [[datetime(2023, 7, 24, 1), 300], [datetime(2023, 7, 24, 1), -300],
                                 [datetime(2023, 7, 24, 23), 300], [datetime(2023, 7, 24, 23), -300]],
         datetime(2023, 7, 25): [[datetime(2023, 7, 25, 1), 300], [datetime(2023, 7, 25, 1), -300],
                                 [datetime(2023, 7, 25, 23), 300], [datetime(2023, 7, 25, 23), -300]]
     }),

    ([[datetime(2023, 7, 31, 23), 300],
      [datetime(2023, 8, 1, 1), 300],
      [datetime(2023, 7, 31, 23), -300],
      [datetime(2023, 8, 1, 1), -300]
      ],
     {
         datetime(2023, 7, 31): [[datetime(2023, 7, 31, 23), 300], [datetime(2023, 7, 31, 23), -300]],
         datetime(2023, 8, 1): [[datetime(2023, 8, 1, 1), 300], [datetime(2023, 8, 1, 1), -300]]
     }),

    ([[datetime(2023, 12, 31, 23), 300],
      [datetime(2024, 1, 1, 1), 300],
      [datetime(2023, 12, 31, 23), -300],
      [datetime(2024, 1, 1, 1), -300]
      ],
     {
         datetime(2023, 12, 31): [[datetime(2023, 12, 31, 23), 300], [datetime(2023, 12, 31, 23), -300]],
         datetime(2024, 1, 1): [[datetime(2024, 1, 1, 1), 300], [datetime(2024, 1, 1, 1), -300]]
     })

])
def test_input_and_output(request):
    input_date = request.param[0]
    output_group = request.param[1]

    ef = EventFactory(None, None)
    event_list = ef.generate_test_event_list(input_date)

    group_dict = defaultdict(list)
    for date, date_list in output_group.items():
        for date_for_event in date_list:
            group_dict[date.date()].append(ef.generate_test_event(date_for_event))

    manager = DataManager(None, None)
    manager.list_events = event_list
    manager.group_by_time_events()

    yield manager, group_dict


@pytest.mark.no_json_test
def test_check_count_events(test_input_and_output):
    # проверка количества событий в итоге
    manager, output_group = test_input_and_output

    assert len(manager.dict_groups.items()) == len(output_group.items())


@pytest.mark.no_json_test
def test_check_group_date(test_input_and_output):
    # проверка дат у групп
    manager, output_group = test_input_and_output

    assert set(manager.dict_groups.keys()) == set(output_group.keys())


@pytest.mark.no_json_test
def test_check_group_date(test_input_and_output):
    # проверка порядка и наличия событий
    manager, output_group = test_input_and_output

    serialized_data_input = {key.isoformat(): value for key, value in manager.dict_groups.items()}
    serialized_data_output = {key.isoformat(): value for key, value in output_group.items()}
    input_data = json.dumps(serialized_data_input, default=manager.no_serializable_to_str)
    output_data = json.dumps(serialized_data_output, default=manager.no_serializable_to_str)

    assert input_data == output_data
