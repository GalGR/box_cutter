import numpy as np
from coord import Coord
from cut_edge import CutEdge
from copy import deepcopy

class Chart:

    EMPTY = 0
    OCCUPIED = 1
    DATA_TYPE = np.bool

    ORIENTATIONS = 4
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __init__(self):
        self.arr = None
        self.chart_id = None
        self.height = None
        self.width = None
        self.index = None
        self.low = None
        self.high = None
        self.pixels = None
        self.orientation = Chart.NORTH
        self.mirror = (False, False)

    @classmethod
    def copy(cls, chart):
        obj = cls()

        obj.arr = np.array(chart.arr, dtype=Chart.DATA_TYPE, copy=True)
        obj.chart_id = chart.chart_id
        obj.height = chart.height
        obj.width = chart.width
        obj.index = Coord(chart.index)
        obj.low = Coord(chart.low)
        obj.high = Coord(chart.high)
        obj.pixels = chart.pixels
        obj.orientation = chart.orientation

        return obj

    @classmethod
    def create(cls, arr, height=None, width=None, chart_id=None, index=None, pixels=None, orientation=Chart.NORTH, mirror=(False, False)):
        obj = cls()

        obj.arr = np.array(arr, dtype=Chart.DATA_TYPE, copy=True)
        obj.chart_id = chart_id
        if height == None:
            obj.height = obj.arr.shape[0]
        else:
            obj.height = height
        if width == None:
            obj.width = obj.arr.shape[1]
        else:
            obj.width = width
        if index != None:
            obj.index = Coord(index)
            obj.low = Coord(index[0], index[1])
            obj.high = Coord(index[0] + height, index[1] + width)
        if pixels == None:
            obj.pixels = obj._count_pixels()
        else:
            obj.pixels = pixels
        if orientation < 0 or orientation > 3:
            raise Exception('Invalid orientation in Chart.create')
        obj.orientation = orientation

        return obj

    @classmethod
    def from_atlas(cls, atlas, chart_id):
        # Bounding box variables of the chart
        low = Coord(atlas.rows - 1, atlas.cols - 1)
        high = Coord(0, 0)

        # Search the atlas for the chart and find the bounding
        for i in range(atlas.rows):
            for j in range(atlas.cols):
                tmp_id = atlas[i, j]
                if tmp_id == chart_id:
                    low.x = min(low.x, i)
                    low.y = min(low.y, j)
                    high.x = max(high.x, i)
                    high.y = max(high.y, j)

        # Calculate dimensions
        height = high.x - low.x + 1
        width = high.y - low.y + 1

        # Create array for the chart
        chart_arr = np.ndarray(shape=(height, width), dtype=Chart.DATA_TYPE)
        chart_arr.fill(Chart.EMPTY)

        # Copy the chart from the atlas to the array
        pixels = 0
        for i in range(height):
            for j in range(width):
                tmp_id = atlas[low.x + i, low.y + j]
                if tmp_id == chart_id:
                    chart_arr[i, j] = Chart.OCCUPIED
                    pixels += 1

        # Create a new Chart object and return it
        index = low
        chart = Chart.create(chart_arr, height, width, chart_id=chart_id, index=index, pixels=pixels)

        return chart

    def _count_pixels(self):
        pixels = 0
        for i in range(self.height):
            for j in range(self.width):
                if self[i, j] == Chart.OCCUPIED:
                    pixels += 1
        return pixels

    def cut(self, edge):
        arr_list = None
        if edge.orientation == CutEdge.HORIZONTAL:
            arr_list = self._cut_horizontal(edge.axis - self.low.x)
        elif edge.orientation == CutEdge.VERTICAL:
            arr_list = self._cut_vertical(edge.axis - self.low.y)
        else:
            raise Exception('Invalid orientation for cutting in Chart')
        return [Chart.create(arr_list[0]), Chart.create(arr_list[1])]

    def _cut_horizontal(self, x):
        return [self[0:x, :], self[x:self.rows, :]]

    def _cut_vertical(self, y):
        return [self[:, 0:y], self[:, y:self.cols]]

    def __getitem__(self, key):
        key = self._transform_key(key)
        return self.arr[key]

    def __setitem__(self, key, value):
        key = self._transform_key(key)
        self.arr[key] = value

    def rotate_clockwise(self):
        self.orientation = (self.orientation + 1) % Chart.ORIENTATIONS
        tmp_width = self.width
        self.width = self.height
        self.height = tmp_width
        self.mirror = (self.mirror[1], self.mirror[0])
        self.invalidate_pos()

    def rotate_counter_clockwise(self):
        self.orientation = (self.orientation - 1) % Chart.ORIENTATIONS
        tmp_width = self.width
        self.width = self.height
        self.height = tmp_width
        self.mirror = (self.mirror[1], self.mirror[0])
        self.invalidate_pos()

    def mirror_x(self):
        if self.orientation % 2 == 0:
            self.mirror = (not self.mirror[0], self.mirror[1])
        else:
            self.mirror = (self.mirror[0], not self.mirror[1])

    def mirror_y(self):
        if self.orientation % 2 == 0:
            self.mirror = (self.mirror[0], not self.mirror[1])
        else:
            self.mirror = (not self.mirror[0], self.mirror[1])

    def invalidate_pos(self):
        self.index = None
        self.low = None
        self.high = None

    def _get_key(self, key):
        key = _rotate_key(key)
        key = _mirror_key(key)
        return key

    def _rotate_key(self, key):
        if self.orientation == 0:
            key = (key[0], key[1])
        elif self.orientation == 1:
            key = (self.width - 1 - key[1], key[0])
        elif self.orientation == 2:
            key = (self.height - 1 - key[0], self.width - 1 - key[1])
        elif self.orientation == 3:
            key = (key[1], self.height - 1 - key[0])
        else:
            raise Exception('Invalid orientation in Chart._roatate_key')
        return key

    def _mirror_key(self, key):
        if self.mirror[0]:
            key = (self.height - 1 - key[0], key[1])
        if self.mirror[1]:
            key = (key[0], self.width - 1 - key[1])
        return key