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
        # Identificador único de la reserva
        self.booking_id = booking_id
        # Identificador del usuario que realiza la reserva
        self.user_id = user_id
        # ID del laboratorio asignado (0 si aún no se ha asignado)
        self.room_id = 0
        # ID del laboratorio solicitado
        self.room_id_solicited = room_id_solicited
        # Lista de herramientas asignadas
        self.tool_ids: list[int] = []
        # Lista de herramientas solicitadas eliminadas a medida que se van reservando
        self.tool_ids_solicited: list[int] = tool_ids_solicited
        # Estado actual de la reserva
        self.status = StatusBooking.PENDING
        # Tiempo de referencia (momento de creación de la reserva)
        self.reference_time  = time() 
        # Tiempo en que finaliza la reserva (relativo a reference_time)
        self.end_time = 0
        # Tiempo en que la reserva fue aprobada (relativo a reference_time)
        self.approved_time = 0 

    def add_room(self, room_id: int):
        """Asigna un laboratorio a la reserva y limpia el solicitado."""
        self.room_id = room_id
        self.room_id_solicited = 0

    def add_tool(self, tool_id: int):
        """Agrega una herramienta a la reserva si no está incluida y la elimina de las solicitadas."""
        if tool_id not in self.tool_ids:
            self.tool_ids.append(tool_id)
            self.remove_tool_solicited(tool_id)

    def remove_tool(self, tool_id: int):
        """Elimina una herramienta de la reserva si está incluida."""
        if tool_id in self.tool_ids:
            self.tool_ids.remove(tool_id)

    def remove_tool_solicited(self, tool_id: int):
        """Elimina una herramienta de la lista de solicitadas."""
        self.tool_ids_solicited.remove(tool_id)

    def approve(self):
        """Cambia el estado a APROBADA y registra el tiempo de aprobación."""
        self.status = StatusBooking.APPROVED
        self.approved_time = (time() - self.reference_time) 

    def reject(self):
        """Cambia el estado a RECHAZADA y registra el tiempo de finalización."""
        self.status = StatusBooking.REJECTED
        self.end_time = (time() - self.reference_time)
        #print(f"[DEBUG] Booking {self.booking_id} rejected at {self.end_time}, total time: {self.end_time - self.reference_time:.2f} seconds")

    def cancel(self):
        """Cambia el estado a CANCELADA."""
        self.status = StatusBooking.CANCELLED

    def finish(self):
        """Cambia el estado a FINALIZADA y registra el tiempo de finalización."""
        self.status = StatusBooking.FINISHED
        self.end_time = (time() - self.reference_time)  

    def in_use(self):
        """Cambia el estado a EN USO."""
        self.status = StatusBooking.IN_USE

    def is_active(self):
        """Verifica si la reserva está activa (no cancelada ni finalizada)."""
        return self.status not in {StatusBooking.CANCELLED, StatusBooking.FINISHED}
    
    def get_status(self):
        """Devuelve el estado actual de la reserva como string."""
        return self.status.name
    

    def __str__(self):
        # Representación legible de la reserva
        return f"Booking ID: {self.booking_id}, User ID: {self.user_id}, Room ID: {self.room_id}, Tools: {self.tool_ids}, Status: {self.status.name}"
    
    def __repr__(self):
        # Representación resumida para depuración
        return f"Booking({self.booking_id}, {self.user_id}, {self.status.name})"