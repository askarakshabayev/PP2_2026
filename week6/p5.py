text = "cat bat world tat lllat hello"

import re

matches = re.findall(r"\w+at", text)
print(matches)

