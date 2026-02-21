class Person:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def show(self):
        print(f"name={self.name}, surname={self.surname}")

class Student(Person):

    def __init__(self, name, surname, ID, gpa):
        super().__init__(name, surname)
        self.ID = ID
        self.gpa = gpa

    def show(self):
        super().show()
        print(f"ID={self.ID}, gpa={self.gpa}")

a = Person("Askar", "Akshabayev")
b = Person("Kairat", "Moldbayev")
a.show()
b.show()

c = Student("Aaa", "Bbbb", "04BD02", 3.93)
c.show()