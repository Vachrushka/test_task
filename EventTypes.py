from enum import Enum, auto


class EventType(Enum):
    PRIVATE = auto()
    MEETING = auto()
    CORPORATE = auto()
    OTHER = auto()

    def __str__(self):
        return self.name.lower()
