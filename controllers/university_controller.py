from views.university_view import show_booking_result
from views.pending_bookings_graph import PendingBookingsGraph
import threading
from models.university import University

class UniversityController:
    """Controller for managing university lab bookings."""
    def __init__(self, university: University):
        self.university = university

    def book_lab(self, student_id, room_id, tool_ids):
        """Books a laboratory room and tools for a student."""
        id = self.university.to_book(student_id, room_id, tool_ids)
        show_booking_result(f"Reserva realizada con id {id}")

    def use_booking(self, id_booking):
        """Marks a booking as in use."""
        self.university.use_booking(id_booking)

    def random_book(self, student_id):
        """Randomly books a laboratory for a student."""
        self.university.random_booking(student_id)

    def show_bookings(self):
        """Returns the list of all bookings."""
        show_booking_result(self.university.get_all_booking_details())

    def show_blocking_bookings(self):
        """Returns the list of all bookings."""
        show_booking_result(self.university.get_blocking_bookings())
        
    def show_pending_bookings_graph(self):
        """Displays a graph of pending bookings and their requested resources."""
        pending_bookings = self.university.get_pending_bookings()
        graph = PendingBookingsGraph(
            pending_bookings,
            self.university.laboratories,
            self.university.laboratory_tools
        )
        graph.build_graph()
        graph.draw()
        
    def concurrent_ramdom_bookings(self, studens_ids):
        """Creates multiple threads to book laboratories concurrently for a list of students."""
        threads = []

        for student_id in studens_ids:
            t = threading.Thread(target=self.random_book, args=(student_id,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
