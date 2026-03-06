import json

f = open("student.txt", "r")
text = f.read()

student = json.loads(text)
print(student["name"])
print(student["surname"])
print(student["id"])

