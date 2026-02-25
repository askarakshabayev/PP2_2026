import re
text = "Order number: 98765"
match = re.search(r"\d+", text)
print(match.group())
print(match.span())
print(match.start())
print(match.end())