import numpy as np
from atlas import Atlas

# class SkipBuffer(np.ndarray):
class SkipBuffer:
    OCCUPIED = 0
    START = 1
    DATA_TYPE = np.uint16

    # @classmethod
    # def __new__(cls, atlas):
    #     itself = np.ndarray.__new__(cls, shape=atlas.shape, dtype=SkipBuffer.DATA_TYPE)
    #     itself.fill(SkipBuffer.OCCUPIED)
    #     itself._fill_buffer(atlas)
    #     return itself

    def __init__(self, atlas):
        self.shape = (atlas.rows, atlas.cols)
        self.arr = np.ndarray(shape=self.shape, dtype=SkipBuffer.DATA_TYPE)
        self.rows = atlas.rows
        self.cols = atlas.cols
        self.arr.fill(SkipBuffer.OCCUPIED)
        self._fill_buffer(atlas)

    def _fill_buffer(self, atlas):
        for i in range(self.rows):
            # Initialize the counter to the starting value
            count = SkipBuffer.START
            # Start reading the atlas from right to left (reversed)
            for j in reversed(range(self.cols)):
                if atlas[i, j] == Atlas.EMPTY:
                    # Write how many empty spots are on the right
                    self[i, j] = count
                    # Increment the counter
                    count += 1
                else:
                    # Indicate the spot is occupied
                    self[i, j] = SkipBuffer.OCCUPIED
                    # Reset the counter
                    count = SkipBuffer.START

    def __getitem__(self, key):
        return self.arr[key]

    def __setitem__(self, key, value):
        self.arr[key] = value