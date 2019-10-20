import numpy as np
from skip_buffer import SkipBuffer
from void_box import VoidBox as Box

class BoxQueue:

    MAX_OVERLAP = 0.1
    N = 1

    def __init__(self):
        self.arr = list()

    def push(self, box):
        remove_queue = list()
        insert_index = len(self.arr)
        for i in range(len(self.arr)):
            overlap = box.overlap(self.arr[i])
            if box.size > self.arr[i].size:
                if i < insert_index:
                    insert_index = i
                if overlap >= BoxQueue.MAX_OVERLAP:
                    remove_queue.append(i)
            else:
                if overlap >= BoxQueue.MAX_OVERLAP:
                    # If the new box is overlapping with a bigger box then it's useless
                    return
        # Remove any overlapping (smaller) boxes
        for i in reversed(remove_queue):
            # The indices changes during the removing, so we are going backwards over the indices
            del self.arr[i]
        # Insert the box at the correct index to keep the list sorted
        self.arr.insert(insert_index, box)
        # Keep only the N biggest boxes
        self.arr = self.arr[:BoxQueue.N]

    def _key(self, box):
        return box.size

    def pop(self):
        return self.arr.pop(0)

    def peek(self):
        return self.arr[0]

    def get_box_list(self):
        return list(self.arr)