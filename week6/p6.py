text = 'Written on 19.01.2018, updated on 01.09.2024'

import re

it = re.finditer(r"\d\d.\d\d.\d{4}", text)
print(next(it).span())
print(next(it).span())
print(next(it).span())
