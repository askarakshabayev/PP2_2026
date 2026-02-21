# 10, 9, 8, ..., 0
class Countdown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current # 10
        self.current -= 1 # 9
        return value

a = Countdown(3)
it = iter(a)
print(next(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))

for num in Countdown(10):
    print(num)
# it = iter(a)
# while True:
#     try:
#         value = next(it)
#         print(value)
#     except Exception as e:
#         break