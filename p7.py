text = "test test cat test cat test dog"

import re
matches = re.findall(r"cat|dog", text)
print(matches)