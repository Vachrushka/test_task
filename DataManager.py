import json
from datetime import datetime
from collections import defaultdict
from Event import EventList, Event
from EventTypes import EventType
from Validator import ValidEvent


class DataManager:
    def __init__(self, inputFile, outputFile):
        self.inputFilePath = inputFile
        self.outputFilePath = outputFile
        self.list_events = EventList([])
        self.dict_groups = {}

    def load_json_data(self):
        # считывание
        with open(self.inputFilePath, "r") as json_file:
            json_data = json.load(json_file)

        # валидация данных
        validator = ValidEvent()
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
        if not self.list_events.events:
            return

        self.list_events.delete_type_other()
        self.list_events.close_data_sort()

        group_dict = defaultdict(list)
        for event in self.list_events.events:
            group_dict[event.event_time.date()].append(event)

        for key, event_list in group_dict.items():
            group_dict[key] = EventList(event_list).close_time_sort()

        self.dict_groups = group_dict

    def write_groups_data(self):
        # сериализация по группам
        serialized_data = {key.isoformat(): value for key, value in self.dict_groups.items()}
        json_data = json.dumps(serialized_data, default=self.no_serializable_to_str, indent=2)
        with open(self.outputFilePath, "w") as file:
            file.write(json_data)

    def write_json_data(self):
        # сериализация сортированного листа событий
        json_data = json.dumps(self.list_events.events, default=self.no_serializable_to_str, indent=2)
        with open(self.outputFilePath, "w") as file:
            file.write(json_data)

    def no_serializable_to_str(self, obj):
        if isinstance(obj, defaultdict):
            return dict(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, EventType):
            return str(obj)
        elif isinstance(obj, Event):
            return obj.to_json()
