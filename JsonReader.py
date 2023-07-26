import json
import re
from datetime import datetime, date, timezone

from Event import EventList, Event, EventGroup
from EventTypes import EventType

expected_keys = ["event_time", "event_type", "event_name", "event_members", "event_place"]


def is_iso_datetime(s):
    try:
        if s.endswith("Z"):
            dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
            return dt.replace(tzinfo=timezone.utc)
        else:
            return datetime.fromisoformat(s)
    except Exception:
        raise ValueError("Date format does not match ISO: {}".format(s))


def is_event_type(t):
    try:
        return EventType[t.upper()]
    except Exception:
        raise ValueError("Unsupported event format: {}".format(t))


def is_event_name(n):

    in_format = True
    if len(n) > 100 or len(n) == 0:
        in_format = False

    try:
        # Проверка каждой последовательности в строке
        sequences = n.split()
        for seq in sequences:
            if len(seq) > 20 or not re.match("^[a-zA-Z0-9]+$", seq):
                in_format = False
    except Exception:
        raise ValueError("Event name does not match the requirements: {}".format(n))

    if in_format:
        return n
    else:
        raise ValueError("Event name does not match the requirements: {}".format(n))


def is_members_list(m):
    if isinstance(m, list) and len(m) > 0:
        return m
    else:
        raise ValueError("Event participants does not match the requirements: {}".format(m))


def is_location(l):
    return l


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

        # валидация данных
        if isinstance(json_data, list):

            for event in json_data:
                if (event.keys()) != set(expected_keys):
                    raise ValueError("Following keys {0} are expected".format(expected_keys))
                elif not all(value is not None for value in event.values()):
                    raise ValueError("Values should not be empty")
                else:
                    # проверка значений
                    data = is_iso_datetime(event["event_time"])
                    event_type = is_event_type(event["event_type"])
                    name = is_event_name(event["event_name"])
                    members = is_members_list(event["event_members"])
                    location = is_location(event["event_place"])

                    new_event = Event(data, event_type, name, members, location)
                    self.list_events.events.append(new_event)

        elif isinstance(json_data, dict):
            data = is_iso_datetime(json_data["date_and_time"])
            event_type = is_event_type(json_data["event_type"])
            name = is_event_name(json_data["event_name"])
            members = is_members_list(json_data["participants"])
            location = is_location(json_data["location"])

            new_event = Event(data, event_type, name, members, location)
            self.list_events.events.append(new_event)
        else:
            raise ValueError("Invalid format data input")

    def group_by_time_events(self):
        if self.list_events.events is None or len(self.list_events.events) == 0:
            return
        self.list_events.delete_type_other()
        self.list_events.close_data_sort()

        group_list = []
        group_data = self.list_events.events[0].event_time.date()
        group_list_temp = EventList([])
        for event in self.list_events.events:
            if group_data == event.event_time.date():
                group_list_temp.events.append(event)
            else:
                # создание группы со старой датой
                group_list.append(EventGroup(group_data, group_list_temp))

                group_data = event.event_time.date()
                group_list_temp = EventList([])
                group_list_temp.events.append(event)

        group_list.append(EventGroup(group_data, group_list_temp))

        for group in group_list:
            group.events_list.close_time_sort()

        self.list_groups = group_list


    def write_groups_data(self):
        # сериализация по группам
        serialized_list = [groups.__dict__ for groups in self.list_groups]
        #print(serialized_list)
        json_data = json.dumps(serialized_list, default=no_serializable_to_str, indent=2)
        #print(json_data)
        with open(self.outputFilePath, "w") as file:
            file.write(json_data)

    def write_json_data(self):
        # сериализация сортированного листа событий
        serialized_list = [event.__dict__ for event in self.list_events.events]
        json_data = json.dumps(serialized_list, default=no_serializable_to_str, indent=2)

        #print(self.outputFilePath)
        with open(self.outputFilePath, "w") as file:
            file.write(json_data)
