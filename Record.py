import random

class Record:
    def __init__(self, key, empty, overflow_pointer):
        self.key = key
        self.overflow_pointer = overflow_pointer
        self.empty = empty
        self.first = False
        self.data = self.generate_record()
        self.to_delete = False

    def generate_record(self):
        real = random.uniform(-100, 100)
        imag = random.uniform(-100, 100)

        z = complex(real, imag)
        return z
