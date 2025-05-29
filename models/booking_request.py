class BookingRequest:
    """Represents a booking request for a room with specific tools."""
    def __init__(self, booking_id, user_id, room_id, tool_ids: list[int]):
        self.booking_id = booking_id
        self.user_id = user_id
        self.room_id = room_id
        self.tool_ids = tool_ids

    def __repr__(self):
        return f"BookingRequest(booking_id={self.booking_id}, user_id={self.user_id}, room_id={self.room_id}, tool_ids={self.tool_ids})"