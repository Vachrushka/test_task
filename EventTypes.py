from enum import Enum


class EventType(Enum):
    PRIVATE = 1
    MEETING = 2
    CORPORATE = 3
    OTHER = 4

    def __str__(self):
        return self.name.lower()
