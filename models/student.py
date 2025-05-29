class Student:
    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code

    def __str__(self):
        return f"Student(name={self.name}, code={self.code})"
    
    def __repr__(self):
        return f"Student({self.name}, Code: {self.code})"