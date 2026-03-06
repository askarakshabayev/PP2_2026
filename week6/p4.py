phone = "+7   (777) 99-89"

import re
digits = re.sub(r"\D", '', phone)

print(digits)