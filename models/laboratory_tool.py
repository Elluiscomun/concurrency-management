from .status_source import Status 
from threading import Lock

class LaboratoryTool:
    """Represents a laboratory tool with its name, ID, and status."""
    def __init__(self, name, id):
        self.status: Status = Status.AVAILABLE
        self.name = name
        self.id = id

        #self.lock = Lock()
        

    def to_book(self):
        if self.status != Status.AVAILABLE:
            raise ValueError("Source is not available")
        self.status = Status.RESERVERD

    def to_use(self):
        self.status = Status.IN_USE


    def release(self):
        self.status = Status.AVAILABLE

    def is_available(self):
        """Checks if the tool is available."""
        return self.status == Status.AVAILABLE
    

    def __str__(self):
        return f"LaboratoryTool(name={self.name}, id={self.id}, status={self.status})"
    
    def __repr__(self):
        return f"LaboratoryTool({self.name}, {self.id}, {self.status.name})"