import unittest
from unittest.mock import MagicMock
from models.university import University
from models.laboratory import Laboratory
from models.laboratory_tool import LaboratoryTool
from models.student import Student
from models.booking import Booking, StatusBooking

class TestUniversity(unittest.TestCase):
    def setUp(self):
        # Crea herramientas y laboratorios de prueba
        self.tools = [
            LaboratoryTool("Oscilloscope", 1),
            LaboratoryTool("Multimeter", 2)
        ]
        self.labs = [
            Laboratory("Instrumentation", 1, [1, 2])
        ]
        self.students = [Student("Juan", 1)]
        self.university = University(self.labs, self.tools, self.students)

    def test_get_laboratory_status(self):
        status = self.university.get_laboratory_status(1)
        self.assertIsNotNone(status)

    def test_get_tool_status(self):
        status = self.university.get_tool_status(1)
        self.assertIsNotNone(status)

    def test_book_room_and_to_book(self):
        booking_id = self.university.to_book(1, 1, [1])
        booking = self.university.get_booking_by_id(booking_id)
        self.assertEqual(booking.user_id, 1)
        self.assertIn(1, booking.tool_ids)
        self.assertTrue(booking.status in [StatusBooking.APPROVED, StatusBooking.REJECTED, StatusBooking.IN_USE])

    def test_random_booking(self):
        booking_id = self.university.random_booking(1)
        booking = self.university.get_booking_by_id(booking_id)
        self.assertEqual(booking.user_id, 1)

    def test_get_bookings_by_student(self):
        self.university.to_book(1, 1, [1])
        bookings = self.university.get_bookings_by_student(1)
        self.assertTrue(len(bookings) > 0)

    def test_get_booking_by_id_not_found(self):
        with self.assertRaises(ValueError):
            self.university.get_booking_by_id(999)

    def test_str(self):
        s = str(self.university)
        self.assertIn("University with", s)

if __name__ == '__main__':
    unittest.main()