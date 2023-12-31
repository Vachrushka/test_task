import os

from EventTypes import EventType
from Event import Event, EventList
from datetime import timedelta, timezone, datetime
import random
import string
import pytz

from JsonReader import JsonReader


def generate_random_string(name_length):
    # Генерируем случайное имя события
    alphabet = string.ascii_letters + string.digits + " "
    return ''.join(random.choice(alphabet) for _ in range(name_length))


def generate_random_event_type():
    # Генерируем случайный тип события
    event_types = [event_type for event_type in EventType]
    return random.choice(event_types)


def generate_random_event_loc():
    # Генерируем случайную зону события
    event_loc = ["zoom", "telegram", "discord", "telemost", generate_random_string(6)]
    return random.choice(event_loc)


def generate_random_event_time_zone(time):
    # Генерируем случайный часовой пояс
    iso_types = [1]
    selected_type = random.choice(iso_types)
    if selected_type == 0:
        # время по гринвичу (Z)
        time = time.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        # время c сдвигом поясов
        random_timezone = random.choice(pytz.all_timezones)
        time = pytz.timezone(random_timezone).localize(time).isoformat()
    return datetime.fromisoformat(time)


class EventFactory:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.input_path = os.getcwd() +"/data/input.json"

    def generate_random_event_time(self):
        # Генерируем случайное время в диапазоне между start_date и end_date
        time_difference = self.end_date - self.start_date
        random_time_delta = random.randint(0, int(time_difference.total_seconds()))
        random_event_time = self.start_date + timedelta(seconds=random_time_delta)

        return generate_random_event_time_zone(random_event_time)

    def generate_random_event(self):
        # Генерируем случайное событие
        event_time = self.generate_random_event_time()
        event_name = generate_random_string(random.randint(1, 20))
        event_type = generate_random_event_type()
        event_loc = generate_random_event_loc()
        return Event(event_time, event_type, event_name, ["Alice", "Bob", "Clara"], event_loc)

    def generate_events_list(self, num_events):
        # Генерируем список случайных событий
        events_list = EventList([])
        for _ in range(num_events):
            event = self.generate_random_event()
            events_list.events.append(event)
        return events_list

    def generate_json(self, count_events=50, event=None):
        json_reader = JsonReader(None, self.input_path)
        if event is None:
            json_reader.list_events = self.generate_events_list(count_events)
        else:
            json_reader.list_events = EventList([event])
        json_reader.write_json_data()


    def generate_event_from_data(self, ev_time, ev_type, ev_name):
        event_loc = generate_random_event_loc()
        return Event(ev_time, ev_type, ev_name, ["Alice", "Bob", "Clara"], event_loc)




