import numpy as np
import math
from atlas import Atlas
from chart import Chart
from chart_list import ChartList

class HierarchicalBuffer:

    DATA_TYPE = np.uint16

    def __init__(self):
        self.arr_list = None
        self.height_list = None
        self.width_list = None
        self.depth = None
        self.atlas = None
        self.chart = None
        self.free_pixels = None
        self.occupied_pixels = None

    @classmethod
    def from_atlas(cls, atlas):
        obj = cls()

        obj.depth = cls._calc_depth(atlas)
        obj.arr_list = [None] * obj.depth
        obj.height_list = [None] * obj.depth
        obj.width_list = [None] * obj.depth
        obj.atlas = atlas

        obj._create_buffers_from_atlas(atlas)

        return obj

    @classmethod
    def from_chart(cls, chart):
        obj = cls()
        obj.depth = cls._calc_depth(chart)
        obj.arr_list = [None] * obj.depth
        obj.height_list = [None] * obj.depth
        obj.width_list = [None] * obj.depth
        obj.chart = chart

        obj._create_buffers_from_chart(chart)

        return obj

    @classmethod
    def _calc_depth(cls, atlas):
        return math.ceil(math.log2(max(atlas.height, atlas.width))) + 1

    def _create_buffers_from_atlas(self, atlas):
        max_axis = max(atlas.height, atlas.width)
        depth = type(self)._calc_depth(atlas)
        cur_size = 2 ** (depth - 1)
        cur_shape = (cur_size, cur_size)

        cur_arr = np.zeros(shape=cur_shape, dtype=type(self).DATA_TYPE)

        for i in range(atlas.height):
            for j in range(atlas.width):
                if atlas[i, j] == Atlas.EMPTY:
                    cur_arr[i, j] = 1

        k = 0
        self.arr_list[k] = cur_arr
        self.height_list[k] = cur_size
        self.width_list[k] = cur_size

        while cur_size != 1:
            prv_size = cur_size
            cur_size = cur_size // 2
            cur_shape = (cur_size, cur_size)
            k += 1

            prv_arr = cur_arr
            cur_arr = np.zeros(shape=cur_shape, dtype=type(self).DATA_TYPE)

            for i in range(cur_size):
                # Improve performance by iterating over each row first
                for j in range(cur_size):
                    cur_arr[i, j] += prv_arr[i * 2, j * 2]
                    cur_arr[i, j] += prv_arr[i * 2, j * 2 + 1]
                for j in range(cur_size):
                    cur_arr[i, j] += prv_arr[i * 2 + 1, j * 2]
                    cur_arr[i, j] += prv_arr[i * 2 + 1, j * 2 + 1]

            self.arr_list[k] = cur_arr
            self.height_list[k] = cur_size
            self.width_list[k] = cur_size

        self.free_pixels = self.arr_list[k][0][0]

    def _create_buffers_from_chart(self, chart):
        max_axis = max(chart.height, chart.width)
        depth = type(self)._calc_depth(chart)
        cur_size = 2 ** (depth - 1)
        cur_shape = (cur_size, cur_size)

        cur_arr = np.zeros(shape=cur_shape, dtype=type(self).DATA_TYPE)

        for i in range(chart.height):
            for j in range(chart.width):
                if chart[i, j] == Chart.OCCUPIED:
                    cur_arr[i, j] = 1

        k = 0
        self.arr_list[k] = cur_arr
        self.height_list[k] = cur_size
        self.width_list[k] = cur_size

        while cur_size != 1:
            prv_size = cur_size
            cur_size = cur_size // 2
            cur_shape = (cur_size, cur_size)
            k += 1

            prv_arr = cur_arr
            cur_arr = np.zeros(shape=cur_shape, dtype=type(self).DATA_TYPE)

            for i in range(cur_size):
                # Improve performance by iterating over each row first
                for j in range(cur_size):
                    cur_arr[i, j] += prv_arr[i * 2, j * 2]
                    cur_arr[i, j] += prv_arr[i * 2, j * 2 + 1]
                for j in range(cur_size):
                    cur_arr[i, j] += prv_arr[i * 2 + 1, j * 2]
                    cur_arr[i, j] += prv_arr[i * 2 + 1, j * 2 + 1]

            self.arr_list[k] = cur_arr
            self.height_list[k] = cur_size
            self.width_list[k] = cur_size

        self.occupied_pixels = self.arr_list[k][0][0]


    def __getitem__(self, key):
        if (key < 0 or key >= self.depth):
            raise IndexError('HierarchicalBuffer.__getitem__: Index out of bounds')
        return self.arr_list[key]