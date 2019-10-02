import numpy as np
from pprint import pprint

# class NewArray(np.ndarray):
class NewArray:

    DATA_TYPE = np.int32
    SHAPE = (10, 20)

    # @classmethod
    # def __new__(cls):
    #     shelf = np.ndarray.__new__(cls, shape=(2,2), dtype=DATA_TYPE)
    #     shelf.fill(-1)
    #     shelf._some_function()
    #     return shelf

    # def __init__(self):
    #     self.arr = np.ndarray(shape=SHAPE, dtype=DATA_TYPE)
    #     self.arr.fill(-1)

    def __init__(self):
        self.arr = None

    @classmethod
    def create(cls):
        obj = cls()
        obj.arr = np.ndarray(shape=cls.SHAPE, dtype=cls.DATA_TYPE)
        obj.arr.fill(-1)
        return obj

    def _some_function(self):
        print('wassup, im zum fungshen')

def main():
    # new_array = NewArray()
    new_array = NewArray.create()
    pprint('type(new_array) = ' + str(type(new_array)))
    pprint(new_array)

main()