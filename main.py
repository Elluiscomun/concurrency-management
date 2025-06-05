from models.university import University
from models.concurrence_control.university_mutex_abroad import UniversityMutexAbroad
from models.concurrence_control.university_mutex import UniversityMutex
from models.concurrence_control.university_release import UniversityRelease
from models.concurrence_control.university_prevention import UniversityPrevention
from models.concurrence_control.university_banker import UniversityBanker

from models.laboratory import Laboratory
from models.laboratory_tool import LaboratoryTool
from models.student import Student
from controllers.university_controller import UniversityController

from views.simulation_gui import SimulationGUI

def main():
    """Main function to run the university booking system."""

    # Crear herramientas
    tools = [
        LaboratoryTool("Oscilloscope", 1),
        LaboratoryTool("Opticskit", 2),
        LaboratoryTool("Calorimeter", 3),
        LaboratoryTool("PressureSensors", 4),
        LaboratoryTool("Multimeter", 5),
    ]

    # Diccionario para fácil acceso por nombre
    tool_dict = {tool.name: tool.id for tool in tools}

    # Crear laboratorios con las herramientas correspondientes (por id)
    labs = [
        Laboratory("Instrumentation", 1, [
            tool_dict["Oscilloscope"],
            tool_dict["PressureSensors"],
            tool_dict["Multimeter"]
        ]),
        Laboratory("Thermodynamics Calorimetry", 2, [
            tool_dict["Calorimeter"],
            tool_dict["PressureSensors"],
            tool_dict["Multimeter"]
        ]),
        Laboratory("Optics", 3, [
            tool_dict["Opticskit"],
            tool_dict["PressureSensors"]
        ]),
        Laboratory("GeneralPhysics", 4, [
            tool_dict["Opticskit"],
            tool_dict["Calorimeter"],
            tool_dict["PressureSensors"],
            tool_dict["Multimeter"]
        ]),
    ]

    """students = [
        Student("Juan", 1),
        Student("Maria", 2),
        Student("Luis", 3),
        Student("Ana", 4),
        Student("Carlos", 5),
        Student("Sofia", 6),
        Student("Pedro", 7),
        Student("Lucia", 8),
        Student("Miguel", 9),
        Student("Elena", 10),
    ]"""

    n = 1  # Cambia este valor para la cantidad de estudiantes que desees

    students = [Student(f"Student_{i+1}", i+1) for i in range(n)]

    #university = UniversitySorted(labs, tools, students)
    #university = UniversityRelease(labs, tools, students)
    #university = University(labs, tools, students)
    #university = UniversityMutexAbroad(labs, tools, students)
    #university = UniversityPrevention(labs, tools, students)
    university = UniversityBanker(labs, tools, students)

    #controller = UniversityController(university)

    #controller.concurrent_ramdom_bookings([(i+1) for i in range(n)])
    #controller.show_pending_bookings_graph()
    #controller.show_booking_stats()


    university_classes = [
        University, UniversityMutexAbroad, UniversityMutex,
        UniversityRelease, UniversityPrevention, UniversityBanker
    ]
    controller = UniversityController(university)
    gui = SimulationGUI(controller, university_classes)
    gui.run()

if __name__ == "__main__":
    main()   