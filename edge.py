import numpy as np

class Edge:

    def __init__(self, coord_low, coord_high):
        self.coords = (coord_low, coord_high)

    def __getitem__(self, key):
        return self.coords[key]