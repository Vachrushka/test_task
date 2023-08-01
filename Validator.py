import re
from datetime import datetime, timezone
from EventTypes import EventType


class ValidEvent:
    expected_keys = ["event_time", "event_type", "event_name", "event_members", "event_place"]

    def check_json_is_list(self, json_data):
        if isinstance(json_data, list):
            pass
        else:
            raise ValueError("Invalid input format: {}".format(json_data))

    def check_key_values(self, event):
        if (event.keys()) != set(self.expected_keys):
            raise ValueError("Following keys {0} are expected".format(self.expected_keys))
        elif not all(value is not None for value in event.values()):
            raise ValueError("Values should not be empty")

    def check_data_for_event(self, event):
        self.check_key_values(event)

        self.is_iso_datetime(event["event_time"])
        self.is_event_type(event["event_type"])
        self.is_event_name(event["event_name"])
        self.is_members_list(event["event_members"])

    def is_iso_datetime(self,s):
        try:
            datetime.fromisoformat(s)
        except Exception:
            raise ValueError("Date format does not match ISO: {}".format(s))

    def is_event_type(self,t):
        try:
            EventType[t.upper()]
        except Exception:
            raise ValueError("Unsupported event format: {}".format(t))

    def is_event_name(self, name):
        if not 1 <= len(name) <= 100:
            raise ValueError("Event name length should be between 1 and 100 characters")

        sequences = name.split()
        for seq in sequences:
            if not 1 <= len(seq) <= 20 or not re.match("^[a-zA-Z0-9]+$", seq):
                raise ValueError("Event name contains invalid characters or exceeds 20 characters")


    def is_members_list(self,m):
        if isinstance(m, list) and len(m) > 0:
            pass
        else:
            raise ValueError("Event participants does not match the requirements: {}".format(m))


