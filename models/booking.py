from enum import Enum, auto
from time import time

class StatusBooking(Enum):
    "Enumeration of possible booking statuses"
    PENDING = auto()
    APPROVED = auto()
    REJECTED = auto()
    CANCELLED = auto()
    IN_USE = auto()
    FINISHED = auto()

class Booking:
    "Represents a booking for a room and tools in a laboratory"
    def __init__(self, booking_id: int, user_id: int, room_id_solicited , tool_ids_solicited):
        self.booking_id = booking_id
        self.user_id = user_id
        self.room_id = 0
        self.room_id_solicited = room_id_solicited
        self.tool_ids: list[int] = []
        self.tool_ids_solicited: list[int] = tool_ids_solicited
        self.status = StatusBooking.PENDING
        self.reference_time  = time()
        self.end_time = 0
        self.approved_time = 0 

    def add_room(self, room_id: int):
        """Adds a room to the booking if it is not already included."""
        self.room_id = room_id
        self.room_id_solicited = 0

    def add_tool(self, tool_id: int):
        """Adds a tool to the booking if it is not already included."""
        if tool_id not in self.tool_ids:
            self.tool_ids.append(tool_id)
            self.remove_tool_solicited(tool_id)

    def remove_tool(self, tool_id: int):
        """Removes a tool from the booking if it is included."""
        if tool_id in self.tool_ids:
            self.tool_ids.remove(tool_id)

    def remove_tool_solicited(self, tool_id: int):
        """Removes a tool from the booking if it is included."""
        self.tool_ids_solicited.remove(tool_id)

    def approve(self):
        """Changes the status of the booking to APPROVED."""
        self.status = StatusBooking.APPROVED
        self.approved_time = (time() - self.reference_time)*1000  # Convert to milliseconds

    def reject(self):
        """Changes the status of the booking to REJECTED."""
        self.status = StatusBooking.REJECTED

    def cancel(self):
        """Changes the status of the booking to CANCELLED."""
        self.status = StatusBooking.CANCELLED

    def finish(self):
        """Changes the status of the booking to FINISHED."""
        self.status = StatusBooking.FINISHED
        self.end_time = (time() - self.reference_time) * 1000  # Convert to milliseconds

    def in_use(self):
        """Changes the status of the booking to IN_USE."""
        self.status = StatusBooking.IN_USE

    def is_active(self):
        """Checks if the booking is active (not cancelled or finished)."""
        return self.status not in {StatusBooking.CANCELLED, StatusBooking.FINISHED}
    


    def __str__(self):
        return f"Booking ID: {self.booking_id}, User ID: {self.user_id}, Room ID: {self.room_id}, Tools: {self.tool_ids}, Status: {self.status.name}"
    
    def __repr__(self):
        return f"Booking({self.booking_id}, {self.user_id}, {self.status.name})"