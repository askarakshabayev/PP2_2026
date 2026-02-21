import json
with open("student.txt", "r") as f:
    data = json.load(f)

print(data)

with open("stud.out", "w") as f:
    json.dump(data, f, indent=4)