import json

# a = {
#     "name": "Askar",
#     "surname": "Akshabayev",
#     "id": "04BD",
#     "age": 40
# }

# b = json.dumps(a)
# print(b)

# c = json.loads(b)
# print(c)

# print(a == c)

f = open("input.txt", "r")
text = f.read()

student = json.loads(text)
print(student)

f1 = open("output.txt", "w")
f1.write(json.dumps(student))
f1.close()