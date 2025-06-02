from models.university import University
import threading
from models.booking import Booking, StatusBooking
from models.laboratory_tool import LaboratoryTool
from models.laboratory import Laboratory
from models.student import Student
from time import time

class UniversityShemaphore(University):

    def __init__(self, laboratories: list[Laboratory], 
                 laboratory_tools: list[LaboratoryTool], students: list[Student]):
        self.laboratories = laboratories
        self.laboratory_tools = laboratory_tools
        self.bookings: list[Booking] = []
        self.booking_id_counter = 0
        self.students = students
        self.semaphore = threading.Semaphore(1)  # Mutex for concurrency control

    def to_book(self, student_id: int, room_id: int, tool_ids: list[int]):
        """Creates a booking for a student with the specified room and tools."""
        start_time = time()
        self.booking_id_counter += 1
        booking = Booking(user_id=student_id, booking_id=self.booking_id_counter, room_id_solicited=room_id, tool_ids_solicited=tool_ids)
        self.bookings.append(booking)
        #print(f"[DEBUG] Creating booking {booking.booking_id} for student {student_id}")

        room_id = self.book_room(room_id)
        if room_id == 0:
            #print(f"[DEBUG] Booking {booking.booking_id} rejected: room unavailable")
            booking.reject()
            return booking.booking_id
        
        booking.add_room(room_id)
        #print(f"[DEBUG] Room {room_id} added to booking {booking.booking_id}")
        
        while tool_ids:
            tool_ids_copy = tool_ids[:]
            for tool_id in tool_ids_copy:
                for tool in self.laboratory_tools:
                    if tool.id == tool_id:
                        #print(f"[DEBUG] Checking tool {tool.id} status: {tool.status}")
                        with self.semaphore:  # Acquire the semaphore for thread safety
                            if tool.is_available():
                                #print(f"[DEBUG] Booking tool {tool.id} for booking {booking.booking_id}")
                                try:
                                    tool.to_book()
                                except ValueError as e:
                                    #print(f"[DEBUG] Error booking tool {tool.id}: {e}")
                                    continue    
                                booking.add_tool(tool_id)
                                tool_ids_copy.remove(tool_id)
            if time() - start_time > 5:  # Timeout
                #print(f"[DEBUG] Timeout booking tools for booking {booking.booking_id}")
                booking.reject()
                return booking.booking_id                

        if not tool_ids:
            #print(f"[DEBUG] Booking {booking.booking_id} approved")
            booking.approve()
            self.use_booking(booking.booking_id)
            return booking.booking_id
        
        if booking.status == StatusBooking.PENDING:
            #print(f"[DEBUG] Booking {booking.booking_id} pending, no tools available")
            booking.reject()
            return booking.booking_id

    def book_room(self, room_id: int):
        """Attempts to book a room by its ID, returning the room ID if successful or 0 if not."""
        start_time = time()
        room = None

        # Entrada a la sección crítica
        for laboratory in self.laboratories:
            if laboratory.id == room_id:
                room = laboratory 

        if room is not None:
            while True:
                #print(f"[DEBUG] Checking room {room.id} status: {room.status}")
                #print(f"[DEBUG)] Room {room.id} available: {room.is_available()}")
                with self.semaphore:  # Acquire the semaphore for thread safety
                    if room.is_available():
                        #print(f"[DEBUG] Booking room {room.id}")
                        try:
                            room.to_book()
                        except ValueError as e:
                            #print(f"[DEBUG] Error booking room {room.id}: {e}")
                            continue
                        return room.id
                    elif time() - start_time > 5:  # Timeout
                        #print(f"[DEBUG] Timeout booking room {room.id}")
                        return 0                           
        #print(f"[DEBUG] Room {room_id} not found")
        return 0
