from models.booking import Booking
from models.concurrence_control.banker import Banker
from models.university import University
from time import sleep

class UniversityBanker(University):

    def __init__(self, laboratories, laboratory_tools, students):
        self.laboratories = laboratories
        self.laboratory_tools = laboratory_tools
        self.students = students
        self.bookings = []
        self.booking_id_counter = 0

        #lab almacena el número de laboratorios disponibles
        total_resources = {"lab": len(self.laboratories)}
        # tool_id almacena la disponibilidad de cada herramienta
        for tool in self.laboratory_tools:
            total_resources[f"tool_{tool.id}"] = 1

        max_demand = {}
        # Cada estudiante puede solicitar maximo 1 laboratorio y 1 de cada herramienta
        # Realmente, cada  estudiante puede reservar menos herramientas
        for student in self.students:
            max_demand[student.code] = {"lab": 1}
            for tool in self.laboratory_tools:
                max_demand[student.code][f"tool_{tool.id}"] = 1
        # Inicializar el banquero con los recursos totales y la demanda máxima por estudiante
        self.banker = Banker(total_resources, max_demand)

    def to_book(self, student_id: int, room_id: int, tool_ids: list[int]):
        self.booking_id_counter += 1
        booking = Booking(user_id=student_id, booking_id=self.booking_id_counter,
                          room_id_solicited=room_id, tool_ids_solicited=tool_ids)
        self.bookings.append(booking)

        # Construir solicitud
        request = {"lab": 1}
        # Añadir herramientas que se solicitan
        for tool_id in tool_ids:
            request[f"tool_{tool_id}"] = 1

        # Paso 1: Esperar hasta que el sistema esté en estado seguro
        while not self.banker.request_resources(student_id, request):
            continue  # Reintentar hasta que se pueda reservar

        # Paso 2: Esperar hasta que el laboratorio esté disponible
        booked_lab = 0
        while booked_lab == 0:
            booked_lab = self.book_room(room_id)
            if booked_lab == 0:
                continue  # Espera si el laboratorio está ocupado

        booking.add_room(booked_lab)

        # Paso 3: Esperar hasta que todas las herramientas estén disponibles
        remaining_tools = set(tool_ids)
        while remaining_tools:
            for tool_id in list(remaining_tools):
                for tool in self.laboratory_tools:
                    if tool.id == tool_id and tool.is_available():
                        try:
                            tool.to_book()
                            booking.add_tool(tool_id)
                            remaining_tools.remove(tool_id)
                        except ValueError:
                            continue
            if remaining_tools:
                continue  # Espera si aún hay herramientas pendientes

        # Paso 4: Aprobar y usar reserva
        booking.approve()
        self.use_booking(booking.booking_id)

        return booking.booking_id

    def release_booking(self, booking_id: int):
        booking = self.get_booking_by_id(booking_id)
        if booking.get_status() == "FINISHED":
            for lab in self.laboratories:
                if lab.id == booking.room_id:
                    lab.release()

            for tool_id in booking.tool_ids:
                for tool in self.laboratory_tools:
                    if tool.id == tool_id:
                        tool.release()

            self.banker.release_resources(booking.user_id)
            return True
        return False
