import numpy as np
from coord import Coord

class Chart:

    EMPTY = 0
    OCCUPIED = 1
    DATA_TYPE = np.bool

    def __init__(self, atlas, id):
        

    def from_atlas(cls, atlas, chart_id):
        # Bounding box variables of the chart
        low = Coord(atlas.shape[0] - 1, atlas.shape[1] - 1)
        high = Coord(0, 0)

        # Search the atlas for the chart and find the bounding
        for i in range(atlas.shape[0]):
            for j in range(atlas.shape[1]):
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
        chart_arr = np.ndarray((height, width), dtype=DATA_TYPE)
        chart_arr.fill(EMPTY)

        # Copy the chart from the atlas to the array
        for i in range(height):
            for j in range(width):
                tmp_id = atlas[low.x + i, low.y + j]
                if tmp_id == chart_id:
                    chart_arr[i, j] = OCCUPIED

        # Create a new Chart object and return it
        raise NotImplementedError