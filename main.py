from models.university import University
from models.laboratory import Laboratory
from models.laboratory_tool import LaboratoryTool
from models.student import Student
from controllers.university_controller import UniversityController

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

    students = [
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
    ]

    university = University(labs, tools, students)
    controller = UniversityController(university)

    # Ejemplo de reserva: Juan reserva Instrumentation con Oscilloscope y Multimeter
    controller.concurrent_ramdom_bookings([1,2,4,5])
    controller.show_bookings()
    controller.show_pending_bookings_graph()

if __name__ == "__main__":
    main()