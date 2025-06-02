from .laboratory import Laboratory
from .laboratory_tool import LaboratoryTool
from .student import Student
from .booking import Booking, StatusBooking
import random
from time import sleep, time
from .status_source import Status

class University:
    """Represents a university with laboratories, tools, and student bookings."""
    def __init__(self, laboratories: list[Laboratory], 
                 laboratory_tools: list[LaboratoryTool], students: list[Student]):
        # Lista de laboratorios disponibles en la universidad
        self.laboratories = laboratories
        # Lista de herramientas de laboratorio disponibles
        self.laboratory_tools = laboratory_tools
        # Lista de todas las reservas realizadas
        self.bookings: list[Booking] = []
        # Contador para asignar IDs únicos a las reservas
        self.booking_id_counter = 0
        # Lista de estudiantes registrados
        self.students = students

    def book_room(self, room_id: int):
        """Attempts to book a room by its ID, returning the room ID if successful or 0 if not."""
        start_time = time()
        room = None
        
        # Buscar el laboratorio con el ID solicitado
        for laboratory in self.laboratories:
            if laboratory.id == room_id:
                room = laboratory 

        if room is not None:
            while True:
                # Si el laboratorio está disponible, intentar reservarlo
                if room.is_available():
                    try:
                        room.to_book()
                    except ValueError as e:
                        # Si ocurre un error al reservar, intentar de nuevo
                        continue
                    return room.id
                # Si pasa más de 5 segundos, cancelar la reserva
                elif time() - start_time > 5:  # Timeout
                    return 0                           
        # Si no se encuentra el laboratorio, retornar 0
        return 0

    def to_book(self, student_id: int, room_id: int, tool_ids: list[int]):
        """Creates a booking for a student with the specified room and tools."""
        start_time = time()
        # Incrementar el contador de reservas y crear una nueva reserva
        self.booking_id_counter += 1
        booking = Booking(user_id=student_id, booking_id=self.booking_id_counter, room_id_solicited=room_id, tool_ids_solicited=tool_ids)
        self.bookings.append(booking)

        # Intentar reservar el laboratorio
        room_id = self.book_room(room_id)
        if room_id == 0:
            # Si no se pudo reservar el laboratorio, rechazar la reserva
            booking.reject()
            return booking.booking_id
        
        booking.add_room(room_id)
        
        # Intentar reservar todas las herramientas solicitadas
        while tool_ids:
            tool_ids_copy = tool_ids[:]
            for tool_id in tool_ids_copy:
                for tool in self.laboratory_tools:
                    if tool.id == tool_id:
                        if tool.is_available():
                            try:
                                tool.to_book()
                            except ValueError as e:
                                continue    
                            booking.add_tool(tool_id)
                            tool_ids_copy.remove(tool_id)
            # Si pasa más de 5 segundos, cancelar la reserva
            if time() - start_time > 5:  # Timeout
                booking.reject()
                self.release_booking(booking_id=booking.booking_id)
                return booking.booking_id                

        # Si todas las herramientas fueron reservadas, aprobar la reserva
        if not tool_ids:
            booking.approve()
            self.use_booking(booking.booking_id)
            return booking.booking_id
        
        # Si la reserva sigue pendiente, rechazarla
        if booking.get_status() == "PENDING":
            booking.reject()
            return booking.booking_id

    def use_booking(self, booking_id: int):
        """Marks the booking as in use and updates the status of the laboratory and tools."""
        booking = self.get_booking_by_id(booking_id)
        if booking.is_active():
            # Cambiar el estado de la reserva a "en uso"
            booking.in_use()
            # Cambiar el estado del laboratorio a "en uso"
            for laboratory in self.laboratories:
                if laboratory.id == booking.room_id:
                    laboratory.to_use()

            # Cambiar el estado de cada herramienta a "en uso"
            for tool_id in booking.tool_ids:
                for tool in self.laboratory_tools:
                    if tool.id == tool_id:
                        tool.to_use()
                        sleep(0.1)
            # Finalizar la reserva y liberar los recursos
            booking.finish()
            self.release_booking(booking_id)
            return True
        return False
    
    def release_booking(self, booking_id: int):
        """Releases the booking and its associated tools if the booking is finished."""
        booking = self.get_booking_by_id(booking_id)
        if booking.status == StatusBooking.FINISHED:
            # Liberar el laboratorio reservado
            for laboratory in self.laboratories:
                if laboratory.id == booking.room_id:
                    laboratory.release()

            # Liberar todas las herramientas reservadas
            for tool_id in booking.tool_ids:
                for tool in self.laboratory_tools:
                    if tool.id == tool_id:
                        tool.release()
            return True
        return False

    def random_booking(self, student_id: int):
        """Creates a random booking for a student with a random laboratory and tools."""
        room_id = random.choice(self.laboratories).id
        tool_ids = [tool.id for tool in self.laboratory_tools]
        if not tool_ids:
            raise ValueError("No available tools to book")
        booking_id = self.to_book(student_id, room_id, random.sample(tool_ids, k=min(3, len(tool_ids))))
        return booking_id
    
    # ---------------------------------------------------------------
    # Functions below are for retrieving information about bookings, students, laboratories, and tools.
    # ----------------------------------------------------------------"""

    def get_bookings_by_student(self, student_id: int):
        """Returns a list of bookings for a specific student."""
        bookings = [booking for booking in self.bookings if booking.user_id == student_id]
        return bookings

    def get_booking_by_id(self, booking_id: int):
        """Returns a booking by its ID."""
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        raise ValueError(f"Booking with ID {booking_id} not found") 
    
    def get_tool_name_by_id(self, tool_id: int):
        """Returns the name of a tool by its ID."""
        for tool in self.laboratory_tools:
            if tool.id == tool_id:
                return tool.name
        raise ValueError(f"Tool with ID {tool_id} not found")  

    def get_pending_bookings(self):
        """Returns a list of pending bookings."""
        pending_bookings = []
        for booking in self.bookings:
            if booking.status != StatusBooking.FINISHED:
                pending_bookings.append(booking)   
        return pending_bookings                    

    def get_laboratory_status(self, laboratory_id: int):
        """Returns the status of a laboratory by its ID."""
        for lab in self.laboratories:
            if lab.id == laboratory_id:
                return lab.status

    def get_laboratory_by_id(self, laboratory_id: int):
        """Returns a laboratory by its ID."""
        for laboratory in self.laboratories:
            if laboratory.id == laboratory_id:
                return laboratory
        raise ValueError(f"Laboratory with ID {laboratory_id} not found")


    def get_tool_status(self, tool_id: int):
        """Returns the status of a tool by its ID."""
        for tool in self.laboratory_tools:
            if tool.id == tool_id:
                return tool.status

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
                "booking_id": booking.booking_id,
                "student": student,
                "laboratory": laboratory,
                "tools": tools,
                "status": booking.status.name
            })
        return details
    
    def get_booking_stats(self):
        """Returns a dictionary with booking statistics."""
        stats = {
            "total_bookings": len(self.bookings),
            "pending": sum(1 for b in self.bookings if b.status == StatusBooking.PENDING),
            "approved": sum(1 for b in self.bookings if b.status == StatusBooking.APPROVED),
            "rejected": sum(1 for b in self.bookings if b.status == StatusBooking.REJECTED),
            "cancelled": sum(1 for b in self.bookings if b.status == StatusBooking.CANCELLED),
            "in_use": sum(1 for b in self.bookings if b.status == StatusBooking.IN_USE),
            "finished": sum(1 for b in self.bookings if b.status == StatusBooking.FINISHED),
            "Average Approved time" : sum(b.approved_time for b in self.bookings if b.status == StatusBooking.FINISHED) / max(1, sum(1 for b in self.bookings if b.status == StatusBooking.FINISHED)),
            "Average End time": sum(b.end_time for b in self.bookings) / max(1, sum(1 for b in self.bookings)), 
            "Min Approved time": min((b.approved_time for b in self.bookings if b.status == StatusBooking.FINISHED), default=0),
            "Max Approved time": max((b.approved_time for b in self.bookings if b.status == StatusBooking.FINISHED), default=0),
            "Min End time": min((b.end_time for b in self.bookings), default=0),
            "Max End time": max((b.end_time for b in self.bookings), default=0),
        }
        return stats

    
    def __str__(self):
        return f"University with {len(self.laboratories)} laboratories, {len(self.laboratory_tools)} tools, and {len(self.bookings)} bookings."