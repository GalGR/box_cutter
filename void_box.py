import numpy as np
from coord import Coord

class VoidBox:

    def __init__(self, index, height, width):
        self.size = height * width
        self.index = Coord(index)
        self.height = height
        self.width = width
        self.low = Coord(index[0], index[1])
        self.high = Coord(index[0] + height, index[1] + width)

    def overlap(self, other):
        # Calculate the intersection area
        inter_size = (
            max(0,
                min(self.high.x, other.high.x) -
                max(self.low.x, other.low.x)) *
            max(0,
                min(self.high.y, other.high.y) -
                max(self.low.y, other.low.y))
        )

        # Calculate and return the overlap percentage
        return inter_size / (self.size + other.size - inter_size)