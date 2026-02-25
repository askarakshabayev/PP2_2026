import re
text = "date = 23.12.1986"

match = re.search(r"(\d{2}).(\d{2}).(\d{4})", text)

print(match.group(2))
print(match.span())
print(match.span(1))
print(match.span(2))