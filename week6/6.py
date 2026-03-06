import json

student = {
    "name": "Aaaa",
    "surname": "Bbbb",
    "subjects": ["PP1", "PP2", "Algo", "Web"],
    "id": "04BD",
    "age": 22
}

b = json.dumps(student)

c = json.loads(b)
print(c["name"])
print(c["surname"])

