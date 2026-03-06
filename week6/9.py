# text = "hello world 1234 test 456 lll 888"

text = "hello world askar@fit.app"
# \d - digit
# \w
# \w+ 

import re

pattern = r"\w+@\w+\.\w+"
match = re.search(pattern, text)

print(match.group())

