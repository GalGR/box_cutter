import numpy as np

class CutEdge:

    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, axis, orientation):
        self.axis = axis
        self.orientation = orientation

    def __getitem__(self, key):
        if key == 0:
            return self.axis
        elif key == 1:
            return self.orientation
        else:
            raise Exception('Invalid key to access a CutEdge')