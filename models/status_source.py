from enum import Enum, auto

class Status(Enum):
    AVAILABLE = auto()
    RESERVERD = auto()
    IN_USE = auto()