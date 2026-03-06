pattern = r"(?P<day>\d\d)/(?P<month>\d\d)/(\d{4})"

text = "hello world 12/02/2024 test test "

import re
match = re.search(pattern, text)
print(match.group())
print(match.group("day"))
print(match.span())