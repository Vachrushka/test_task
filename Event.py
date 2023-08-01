from datetime import datetime
from EventTypes import EventType


class EventList:
    def __init__(self, events: list):
        self.events = events

    def print_events_info(self):
        for e in self.events:
            print(e.info())

    def close_data_sort(self):
        # сортировка по времени проведения
        self.events = sorted(self.events, key=lambda x: x.event_time.date())

    def close_time_sort(self):
        # сортировка по времени проведения
        self.events = sorted(self.events, key=lambda x: x.event_time)
        return self.events

    def delete_type_other(self):
        # удаление событий типа other
        self.events = [event for event in self.events if event.event_type != EventType.OTHER]

    def to_json(self):
        return self.__dict__


class Event:
    def __init__(self, event_time: datetime, event_type: EventType, event_name: str,
                 event_members: list, event_place: str):
        self.event_time = event_time
        self.event_type = event_type
        self.event_name = event_name
        self.event_members = event_members
        self.event_place = event_place

    def info(self):
        return str(self.event_time) + " " + str(self.event_type) + " " + str(self.event_name) + " " + \
               str(self.event_members) + " " + self.event_place

    def to_json(self):
        return self.__dict__


