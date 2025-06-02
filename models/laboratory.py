from .status_source import Status
from threading import Lock

class Laboratory():
    """Represents a laboratory with tools and its status."""
    def __init__(self, name: str, id: int, tools: list[int]):
        self.status: Status = Status.AVAILABLE
        self.name = name
        self.id = id
        self.tools = tools
        
        self.lock = Lock()

    def to_book(self):
        """Changes the status of the laboratory to BOOKED."""
        if self.status != Status.AVAILABLE:
            raise ValueError("Laboratory is not available for booking")
        self.status = Status.RESERVERD

    def to_use(self):
        """Changes the status of the laboratory to IN_USE."""
        self.status = Status.IN_USE

    def release(self):
        """Changes the status of the laboratory to AVAILABLE."""
        self.status = Status.AVAILABLE

    def is_available(self):
        """Checks if the laboratory is available."""
        return self.status == Status.AVAILABLE    

    def __str__(self):
        return f"Laboratory(name={self.name}, id={self.id}, status={self.status})" 
    
    def __repr__(self):
        return f"Laboratory({self.name}, Id: {self.id}, {self.status.name})"
