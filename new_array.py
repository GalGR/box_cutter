import numpy as np
from pprint import pprint

class NewArray(np.ndarray):
    def __new__(cls):
        shelf = np.ndarray.__new__(cls, shape=(2,2), dtype=np.uint16)
        shelf.fill(-1)
        return shelf

def main():
    new_array = NewArray()
    pprint('type(new_array) = ' + str(type(new_array)))
    pprint(new_array)

main()