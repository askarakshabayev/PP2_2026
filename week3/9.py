students = {
    "studnet1" : {"id": "123", "gpa": 3.9, "age": 18},
    "studnet2" : {"id": "124", "gpa": 3.7, "age": 19},
    "studnet3" : {"id": "125", "gpa": 3.6, "age": 20}
}

for student, info in students.items():
    print(student)
    for key, value in info.items():
        print("  ", key, value)
