import os

from EventTypes import EventType
from Event import Event, EventList
from datetime import timedelta, datetime
import random
import string
import pytz
from DataManager import DataManager


class EventFactory:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.input_path = os.getcwd() + "/data/input.json"

    def generate_random_string(self, name_length):
        # Генерируем случайное имя события
        alphabet = string.ascii_letters + string.digits + " "
        return ''.join(random.choice(alphabet) for _ in range(name_length))

    def generate_random_event_type(self):
        # Генерируем случайный тип события
        event_types = [event_type for event_type in EventType]
        return random.choice(event_types)

    def generate_random_event_loc(self):
        # Генерируем случайную зону события
        event_loc = ["zoom", "telegram", "discord", "telemost", self.generate_random_string(6)]
        return random.choice(event_loc)

    def generate_random_event_time_zone(self, time):
        # Генерируем случайный часовой пояс
        random_timezone = random.choice(pytz.all_timezones)
        time = pytz.timezone(random_timezone).localize(time).isoformat()
        return datetime.fromisoformat(time)

    def generate_random_event_time(self):
        # Генерируем случайное время в диапазоне между start_date и end_date
        time_difference = self.end_date - self.start_date
        random_time_delta = random.randint(0, int(time_difference.total_seconds()))
        random_event_time = self.start_date + timedelta(seconds=random_time_delta)

        return self.generate_random_event_time_zone(random_event_time)

    def generate_event(self, date):
        # Генерируем случайное событие
        event_time = date
        event_name = self.generate_random_string(random.randint(1, 20))
        event_type = self.generate_random_event_type()
        event_loc = self.generate_random_event_loc()
        return Event(event_time, event_type, event_name, ["Alice", "Bob", "Clara"], event_loc)

    def generate_events_list(self, num_events):
        # Генерируем список случайных событий
        events_list = EventList([])
        for _ in range(num_events):
            event = self.generate_event(self.generate_random_event_time())
            events_list.events.append(event)
        return events_list

    def generate_json(self, count_events=50, event=None):
        manager = DataManager(None, self.input_path)
        if event is None:
            manager.list_events = self.generate_events_list(count_events)
        else:
            manager.list_events = EventList([event])
        manager.write_json_data()

    def generate_event_from_data(self, ev_time, ev_type, ev_name):
        event_loc = self.generate_random_event_loc()
        return Event(ev_time, ev_type, ev_name, ["Alice", "Bob", "Clara"], event_loc)
