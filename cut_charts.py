import numpy as np
from skip_buffer import SkipBuffer
from atlas import Atlas
from box_queue import BoxQueue
from void_box import VoidBox
from edge import Edge
from coord import Coord

NO_SKIP = -1
ALPHA = 0.2

NORTH = 0
EAST = 1
SOUTH = 2
EAST = 3

def cut_charts(atlas, eff):
    # Get the global void boxes candidates
    boxes_list = _find_void_boxes(atlas)
    cut_atlases = list()

    for box in boxes_list:
        cut_edges = _get_cut_edges(atlas, box)
        for edge in cut_edges:
            # new_atlas = _cut(edge)
            raise NotImplementedError

def _find_void_boxes(atlas):
    # Calculate the skip buffer
    skip_buffer = SkipBuffer(atlas)
    # Initialize the void boxes queue
    boxq = BoxQueue()

    for i_low in range(skip_buffer.shape[0]):
        min_skip = NO_SKIP
        for i in range(i_low, skip_buffer.shape[0]):
            j = 0
            while j < skip_buffer.shape[1]:
                if skip_buffer[i, j] == SkipBuffer.OCCUPIED:
                    min_skip = NO_SKIP
                    j += 1
                else:
                    if min_skip == NO_SKIP or min_skip > skip_buffer[i, j]:
                        min_skip = skip_buffer[i, j]
                    index = (i, j)
                    height = i - i_low + 1
                    width = min_skip
                    box = VoidBox(index, height, width)
                    boxq.push(box)
                    j += skip_buffer[i, j]

    # Return the boxes list
    return boxq.get_box_list()

def _get_cut_edges(atlas, box):
    # edges = {'N': None, 'E': None, 'S': None, 'W': None}
    edges = dict()

    if box.low.x != 0:
        edge_n = Edge(box.low, Coord(box.low.x, box.high.y))
        edges[NORTH] = edge_n
    if box.high.y != atlas.shape[1] - 1:
        edge_e = Edge(Coord(box.low.x, box.high.y), box.high)
        edges[EAST] = edge_e
    if box.high.x != atlas.shape[0] - 1:
        edge_s = Edge(Coord(box.high.x, box.low.y), box.high)
        edges[SOUTH] = edge_s
    if box.low.y != 0:
        edge_w = Edge(box.low, Coord(box.high.x, box.low.y))
        Edges[WEST] = edge_w

    return edges

def _cut(atlas, edge):
    if edge.orientation == horizontal:
        return _cut_horizontal(atlas, edge)
    else:
        return _cut_vertical(atlas, edge)

def _cut_horizontal(atlas, edge):
    for j in range(atlas.shape[1]):
        