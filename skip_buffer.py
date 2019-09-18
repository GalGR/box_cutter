import numpy as np
from atlas import Atlas

class SkipBuffer(np.ndarray):
    OCCUPIED = 0
    START = 1
    DATA_TYPE = np.uint16

    def __new__(cls, atlas):
        itself = np.ndarray.__new__(cls, shape=atlas.shape, dtype=DATA_TYPE)
        itself.fill(OCCUPIED)
        itself._fill_buffer(atlas)
        return itself

    def _fill_buffer(self, atlas):
        # Initialize the counter to the starting value
        count = START

        for i in range(self.shape[0]):
            # Start reading the atlas from right to left (reversed)
            for j in reversed(range(self.shape[1])):
                if atlas[i, j] == Atlas.EMPTY:
                    # Write how many empty spots are on the right
                    self[i, j] = count
                    # Increment the counter
                    count += 1
                else:
                    # Indicate the spot is occupied
                    self[i, j] = OCCUPIED
                    # Reset the counter
                    count = START

    # def __getitem__(self, key):
    #     return self.arr[key]

    # def __setitem__(self, key, value):
    #     self.arr[key] = value