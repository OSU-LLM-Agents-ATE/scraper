from enum import Enum


class Status(Enum):
    AVAILABLE = "a"
    IN_PROGRESS = "ip"
    DONE = "d"
    FAILED = "f"
