import json
from datetime import datetime, date
from collections import defaultdict
from Event import EventList, Event, EventGroup
from EventTypes import EventType
from Validator import ValidEvent


def no_serializable_to_str(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, EventType):
        return str(obj)
    elif isinstance(obj, EventList):
        serialized_list = [event.__dict__ for event in obj.events]
        return serialized_list


class JsonReader:
    def __init__(self, inputFile, outputFile):
        self.inputFilePath = inputFile
        self.outputFilePath = outputFile
        # print(inputFile, outputFile)

        self.list_events = EventList([])
        self.list_groups = []

    def load_json_data(self):
        # считывание
        with open(self.inputFilePath, "r") as json_file:
            json_data = json.load(json_file)

        validator = ValidEvent()

        # валидация данных
        validator.check_json_is_list(json_data)

        for event in json_data:
            validator.check_data_for_event(event)

            new_event = Event(datetime.fromisoformat(event["event_time"]),
                              EventType[event["event_type"].upper()],
                              event["event_name"],
                              event["event_members"],
                              event["event_place"])
            self.list_events.events.append(new_event)



    def group_by_time_events(self):
        if self.list_events.events is None or len(self.list_events.events) == 0:
            return
        self.list_events.delete_type_other()
        self.list_events.close_data_sort()

        group_list = []
        group_date = self.list_events.events[0].event_time.date()
        group_list_temp = EventList([])
        for event in self.list_events.events:
            if group_date == event.event_time.date():
                group_list_temp.events.append(event)
            else:
                # создание группы со старой датой
                group_list.append(EventGroup(group_date, group_list_temp))

                group_date = event.event_time.date()
                group_list_temp = EventList([])
                group_list_temp.events.append(event)

        group_list.append(EventGroup(group_date, group_list_temp))

        for group in group_list:
            group.events_list.close_time_sort()

        self.list_groups = group_list

    def group_by_time_events_dict(self):
        if not self.list_events.events:
            return

        self.list_events.delete_type_other()
        self.list_events.close_data_sort()

        group_dict = defaultdict(list)
        for event in self.list_events.events:
            group_dict[event.event_time.date()].append(event)

        print(group_dict)
        # self.list_groups = group_dict

    def write_groups_data(self):
        # сериализация по группам
        serialized_list = [groups.__dict__ for groups in self.list_groups]
        # print(serialized_list)
        json_data = json.dumps(serialized_list, default=no_serializable_to_str, indent=2)
        # print(json_data)
        with open(self.outputFilePath, "w") as file:
            file.write(json_data)

    def write_json_data(self):
        # сериализация сортированного листа событий
        serialized_list = [event.__dict__ for event in self.list_events.events]
        json_data = json.dumps(serialized_list, default=no_serializable_to_str, indent=2)

        # print(self.outputFilePath)
        with open(self.outputFilePath, "w") as file:
            file.write(json_data)
