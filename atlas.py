import numpy as np
from chart_list import ChartList
from chart import Chart
from PIL import Image

class Atlas:

    EMPTY = -1
    INIT_ID = 0
    DATA_TYPE = np.int16

    # Score formula == packing_efficiency / ((boundary_length / max_axis(first_atlas)) ^ ALPHA)
    ALPHA = 0.2
    MAX_AXIS = 256

    # Image related constants
    WHITE = (255, 255, 255)
    FULL_24BITS = 16777215
    START_COLOR = 255
    BYTE_SIZE = 256

    def __init__(self):
        self.shape = None
        self.arr = None
        self.chart_list = None
        self.rows = None
        self.cols = None
        self.height = None
        self.width = None

    @classmethod
    def create(cls, arr):
        obj = cls()

        obj.shape = (len(arr), len(arr[0]))
        obj.arr = np.array(arr, dtype=Atlas.DATA_TYPE)
        obj.chart_list = ChartList()
        obj.rows = obj.shape[0]
        obj.cols = obj.shape[1]
        obj.height = obj.rows
        obj.width = obj.cols

        obj.chart_list.import_from_atlas(obj)

        return obj


    @classmethod
    def from_image(cls, image):
        colors_dict = dict()
        height = image.height
        width = image.width
        shape = (height, width)
        arr = np.ndarray(shape=shape, dtype=Atlas.DATA_TYPE)
        arr.fill(Atlas.EMPTY)
        new_id = Atlas.INIT_ID
        for i in range(height):
            for j in range(width):
                pixel = image.getpixel((j + 0.5, i + 0.5))
                if pixel != Atlas.WHITE:
                    if pixel not in colors_dict:
                        colors_dict[pixel] = new_id
                        new_id += 1
                    arr[i, j] = colors_dict[pixel]
        return cls.create(arr)

    def to_image(self):
        im = Image.new(mode='RGB', size=(self.width, self.height), color=Atlas.WHITE)
        num_of_charts = len(self.chart_list)
        color_distance = Atlas.FULL_24BITS // num_of_charts
        color_int = Atlas.START_COLOR + color_distance
        ids2colors = dict()
        for chart_id in self.chart_list.ids:
            tmp = color_int
            blue = tmp % Atlas.BYTE_SIZE
            tmp = tmp // Atlas.BYTE_SIZE
            green = tmp % Atlas.BYTE_SIZE
            tmp = tmp // Atlas.BYTE_SIZE
            red = tmp % Atlas.BYTE_SIZE
            ids2colors[chart_id] = (red, green, blue)
        for i in range(self.height):
            for j in range(self.width):
                chart_id = self[i, j]
                if chart_id != Atlas.EMPTY:
                    im.putpixel((j + 0.5, i + 0.5), ids2colors[chart_id])
        return im

    @classmethod
    def from_chart(cls, chart):
        obj = cls()

        obj.shape = (chart.height, chart.width)
        obj.arr = np.ndarray(shape=obj.shape, dtype=Atlas.DATA_TYPE)
        obj.arr.fill(Atlas.EMPTY)
        obj.chart_list = ChartList()
        obj.chart_list.ids.add(chart.chart_id)
        obj.chart_list.charts[chart.chart_id] = chart
        obj.chart_list._new_id = chart.chart_id + 1
        obj.rows = obj.shape[0]
        obj.cols = obj.shape[1]
        obj.height = obj.rows
        obj.width = obj.cols

        for i in range(chart.height):
            for j in range(chart.width):
                if chart[i, j] == Chart.OCCUPIED:
                    obj.arr[i, j] = chart.chart_id

        return obj

    def get_chart(self, chart_id):
        return self.chart_list[chart_id]

    def __getitem__(self, key):
        return self.arr[key]

    def __setitem__(self, key, value):
        self.arr[key] = value

    def calc_score(self):
        return self._calc_packing_eff() / ((self._calc_boundary_len() / Atlas.MAX_AXIS) ** Atlas.ALPHA)

    def _calc_packing_eff(self):
        occupied_pixels = self._count_occupied_pixels()
        all_pixels = self.height * self.width
        return occupied_pixels / all_pixels

    def _count_occupied_pixels(self):
        sum = 0
        for i in range(self.height):
            for j in range(self.width):
                if self[i, j] != Atlas.EMPTY:
                    sum += 1
        return sum

    def _calc_boundary_len(self):
        sum = 0
        for i in range(self.height):
            for j in range(self.width):
                # Check if the current element is not empty
                if self[i, j] != Atlas.EMPTY:
                    # Check if north empty
                    if i > 0 and self[i - 1, j] == Atlas.EMPTY:
                        sum += 1
                        continue
                    # Check if west empty
                    if j > 0 and self[i, j - 1] == Atlas.EMPTY:
                        sum += 1
                    # Check if south empty
                    if i < self.height - 1 and self[i + 1, j] == Atlas.EMPTY:
                        sum += 1
                    # Check if east empty
                    if j < self.width - 1 and self[i, j + 1] == Atlas.EMPTY:
                        sum += 1

        return sum