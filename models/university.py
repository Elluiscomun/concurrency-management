from .laboratory import Laboratory
from .laboratory_tool import LaboratoryTool
from .student import Student
from .booking import Booking, StatusBooking
from .booking_request import BookingRequest
import random
from time import sleep, time
from .status_source import Status

class University:
    """Represents a university with laboratories, tools, and student bookings."""
    def __init__(self, laboratories: list[Laboratory], 
                 laboratory_tools: list[LaboratoryTool], students: list[Student]):
        self.laboratories = laboratories
        self.laboratory_tools = laboratory_tools
        self.bookings: list[Booking] = []
        self.booking_id_counter = 0
        self.students = students

    def get_laboratory_status(self, laboratory_id: int):
        """Returns the status of a laboratory by its ID."""
        for lab in self.laboratories:
            if lab.id == laboratory_id:
                print(f"[DEBUG] Laboratory {lab.id} status: {lab.status}")
                return lab.status

    def get_tool_status(self, tool_id: int):
        """Returns the status of a tool by its ID."""
        for tool in self.laboratory_tools:
            if tool.id == tool_id:
                print(f"[DEBUG] Tool {tool.id} status: {tool.status}")
                return tool.status

    def book_room(self, room_id: int):
        """Attempts to book a room by its ID, returning the room ID if successful or 0 if not."""
        start_time = time()
        room = None
        for laboratory in self.laboratories:
            if laboratory.id == room_id:
                room = laboratory 

        if room is not None:
            while True:
                print(f"[DEBUG] Checking room {room.id} status: {room.status}")
                print(f"[DEBUG)] Room {room.id} available: {room.is_available()}")
                if room.is_available():
                    print(f"[DEBUG] Booking room {room.id}")
                    room.to_book()
                    return room.id
                elif time() - start_time > 5:  # Timeout
                    print(f"[DEBUG] Timeout booking room {room.id}")
                    return 0                           
        print(f"[DEBUG] Room {room_id} not found")
        return 0

    def to_book(self, student_id: int, room_id: int, tool_ids: list[int]):
        """Creates a booking for a student with the specified room and tools."""
        start_time = time()
        self.booking_id_counter += 1
        booking = Booking(user_id=student_id, booking_id=self.booking_id_counter, room_id_solicited=room_id, tool_ids_solicited=tool_ids)
        self.bookings.append(booking)
        print(f"[DEBUG] Creating booking {booking.booking_id} for student {student_id}")

        room_id = self.book_room(room_id)
        if room_id == 0:
            print(f"[DEBUG] Booking {booking.booking_id} rejected: room unavailable")
            booking.reject()
            return booking.booking_id
        
        booking.add_room(room_id)
        print(f"[DEBUG] Room {room_id} added to booking {booking.booking_id}")
        
        while tool_ids:
            tool_ids_copy = tool_ids[:]
            for tool_id in tool_ids_copy:
                for tool in self.laboratory_tools:
                    if tool.id == tool_id:
                        print(f"[DEBUG] Checking tool {tool.id} status: {tool.status}")
                        if tool.is_available():
                            print(f"[DEBUG] Booking tool {tool.id} for booking {booking.booking_id}")
                            tool.to_book()
                            booking.add_tool(tool_id)
                            tool_ids_copy.remove(tool_id)
            if time() - start_time > 5:  # Timeout
                print(f"[DEBUG] Timeout booking tools for booking {booking.booking_id}")
                booking.reject()
                return booking.booking_id                

        if not tool_ids:
            print(f"[DEBUG] Booking {booking.booking_id} approved")
            booking.approve()
            self.use_booking(booking.booking_id)
            return booking.booking_id

    def use_booking(self, booking_id: int):
        """Marks the booking as in use and updates the status of the laboratory and tools."""
        booking = self.get_booking_by_id(booking_id)
        if booking.is_active():
            print(f"[DEBUG] Booking {booking_id} in use")
            booking.in_use()
            for laboratory in self.laboratories:
                if laboratory.id == booking.room_id:
                    print(f"[DEBUG] Laboratory {laboratory.id} in use for booking {booking_id}")
                    laboratory.to_use()

            for tool_id in booking.tool_ids:
                for tool in self.laboratory_tools:
                    if tool.id == tool_id:
                        print(f"[DEBUG] Tool {tool.id} in use for booking {booking_id}")
                        tool.to_use()
                        sleep(random.uniform(0, 0.1))
            booking.finish()
            self.release_booking(booking_id)
            return True
        print(f"[DEBUG] Booking {booking_id} not active")
        return False
    
    def release_booking(self, booking_id: int):
        """Releases the booking and its associated tools if the booking is finished."""
        booking = self.get_booking_by_id(booking_id)
        if booking.status == StatusBooking.FINISHED:
            print(f"[DEBUG] Releasing booking {booking_id}")

            for laboratory in self.laboratories:
                if laboratory.id == booking.room_id:
                    print(f"[DEBUG] Releasing Laboratory {laboratory.id} for booking {booking_id}")
                    laboratory.release()

            for tool_id in booking.tool_ids:
                for tool in self.laboratory_tools:
                    if tool.id == tool_id:
                        print(f"[DEBUG] Releasing tool {tool.id} from booking {booking_id}")
                        tool.release()
            return True
        print(f"[DEBUG] Booking {booking_id} not finished, cannot release")
        return False

    def random_booking(self, student_id: int):
        """Creates a random booking for a student with a random laboratory and tools."""
        room_id = random.choice(self.laboratories).id
        tool_ids = [tool.id for tool in self.laboratory_tools]
        if not tool_ids:
            print("[DEBUG] No available tools to book")
            raise ValueError("No available tools to book")
        booking_id = self.to_book(student_id, room_id, random.sample(tool_ids, k=min(3, len(tool_ids))))
        print(f"[DEBUG] Random booking {booking_id} created for student {student_id}")
        return booking_id

    def get_bookings_by_student(self, student_id: int):
        """Returns a list of bookings for a specific student."""
        bookings = [booking for booking in self.bookings if booking.user_id == student_id]
        print(f"[DEBUG] Bookings for student {student_id}: {[b.booking_id for b in bookings]}")
        return bookings

    def get_booking_by_id(self, booking_id: int):
        """Returns a booking by its ID."""
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                print(f"[DEBUG] Found booking {booking_id}")
                return booking
        print(f"[DEBUG] Booking {booking_id} not found")
        raise ValueError(f"Booking with ID {booking_id} not found") 
    
    def get_tool_name_by_id(self, tool_id: int):
        """Returns the name of a tool by its ID."""
        for tool in self.laboratory_tools:
            if tool.id == tool_id:
                print(f"[DEBUG] Found tool {tool_id}: {tool.name}")
                return tool.name
        print(f"[DEBUG] Tool {tool_id} not found")
        raise ValueError(f"Tool with ID {tool_id} not found")  

    def get_pending_bookings(self):
        """Returns a list of pending bookings."""
        pending_bookings = []
        for booking in self.bookings:
            if booking.status != StatusBooking.APPROVED:
                print(f"[DEBUG] Found pending booking {booking.booking_id} with status {booking.status}")
                pending_bookings.append(booking)   
        return pending_bookings                    

    # ---------------------------------------------------------------
    # All functions below are for visualization and analysis purposes only.
    # They do not affect the main booking system functionality.
    # ---------------------------------------------------------------
    
    def get_all_booking_details(self):
        """Returns a list of dictionaries with details of all bookings."""
        details = []
        for booking in self.bookings:
            student = next((s for s in self.students if s.code == booking.user_id), None)
            laboratory = next((l for l in self.laboratories if l.id == booking.room_id), None)
            tools = [tool for tool in self.laboratory_tools if tool.id in booking.tool_ids]
            details.append({
                "student": student,
                "laboratory": laboratory,
                "tools": tools,
                "status": booking.status
            })
        return details

    
    
    def __str__(self):
        return f"University with {len(self.laboratories)} laboratories, {len(self.laboratory_tools)} tools, and {len(self.bookings)} bookings."