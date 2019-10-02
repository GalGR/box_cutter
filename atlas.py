import numpy as np
from chart_list import ChartList

class Atlas:

    EMPTY = -1
    INIT_ID = 0
    DATA_TYPE = np.int16

    def __init__(self):
        self.shape = None
        self.arr = None
        self.chart_list = None
        self.rows = None
        self.cols = None

    @classmethod
    def create(cls, arr):
        obj = cls()

        obj.shape = (len(arr), len(arr[0]))
        obj.arr = np.array(arr, dtype=Atlas.DATA_TYPE)
        obj.chart_list = ChartList()
        obj.rows = obj.shape[0]
        obj.cols = obj.shape[1]

        obj.chart_list.from_atlas(obj)

        return obj


    @classmethod
    def from_image(cls, image):
        raise NotImplementedError('Atlas.from_image')