import numpy as np
from skip_buffer import SkipBuffer
from atlas import Atlas
from box_queue import BoxQueue
from void_box import VoidBox
from cut_edge import CutEdge
from coord import Coord

# NO_SKIP = -1
# ALPHA = 0.2

NORTH = 0
EAST = 1
SOUTH = 2
EAST = 3

def cut_charts(atlas):
    # Get the global void boxes candidates
    boxes_list = _find_void_boxes(atlas)
    # List of cut charts dictionaries
    list_cut_charts_dicts = list()

    for box in boxes_list:
        cut_edges = _find_cut_edges(atlas, box)
        for edge in cut_edges:
            cut_charts_dict = _cut(atlas, edge)
            list_cut_charts_dicts.append(cut_charts_dict)

    return list_cut_charts_dicts

def _find_void_boxes(atlas):
    # Calculate the skip buffer
    skip_buffer = SkipBuffer(atlas)
    # Initialize the void boxes queue
    boxq = BoxQueue()

    for j in range(skip_buffer.cols):
        for i_lo in range(skip_buffer.rows):
            min_skip = skip_buffer[i_lo, j]
            for i_hi in range(i_lo, skip_buffer.rows):
                if skip_buffer[i_hi, j] == SkipBuffer.OCCUPIED:
                    break
                if min_skip > skip_buffer[i_hi, j]:
                    min_skip = skip_buffer[i_hi, j]
                index = (i_lo, j)
                height = i_hi - i_lo + 1
                width = min_skip
                box = VoidBox(index, height, width)
                boxq.push(box)

    # Return the boxes list
    return boxq.get_box_list()

def _find_cut_edges(atlas, box):
    # edges = {'N': None, 'E': None, 'S': None, 'W': None}
    edges = dict()

    # If not coinciding with the TOP boundary edge
    if box.low.x != 0:
        edge_n = CutEdge(box.low.x, CutEdge.HORIZONTAL)
        edges[NORTH] = edge_n
    # If not coinciding with the RIGHT boundary edge
    if box.high.y != atlas.cols:
        edge_e = CutEdge(box.high.y, CutEdge.VERTICAL)
        edges[EAST] = edge_e
    # If not coinciding with the BOTTOM boundary edge
    if box.high.x != atlas.rows:
        edge_s = CutEdge(box.high.x, CutEdge.HORIZONTAL)
        edges[SOUTH] = edge_s
    # If not coinciding with the LEFT boundary edge
    if box.low.y != 0:
        edge_w = CutEdge(box.low.y, CutEdge.VERTICAL)
        Edges[WEST] = edge_w

    return edges

def _cut(atlas, edge):
    x_lo = edge.xy
    x_hi = edge.xy + 1
    y_range = None
    index_lo = None
    index_hi = None

    if edge.orientation == CutEdge.HORIZONTAL:
        y_range = range(atlas.cols)
        index_lo = lambda y: (x_lo, y)
        index_hi = lambda y: (x_hi, y)
    elif edge.orientation == CutEdge.VERTICAL:
        y_range = range(atlas.rows)
        index_lo = lambda y: (y, x_lo)
        index_hi = lambda y: (y, x_hi)
    else:
        raise Exception('Invalid orientation for an edge in cut_charts._cut')

    cutting_set = dict()
    cut_charts_dict = dict()

    # Find intersecting charts
    for y in y_range:
        id_lo = atlas[index_lo(y)]
        id_hi = atlas[index_hi(y)]
        if id_lo != Atlas.EMPTY and id_lo == id_hi:
            cutting_set.add(id_lo)

    # Cut each intersecting chart
    for cur_id in cutting_set:
        # Append the lists of cut charts
        cut_charts_dict[cur_id] = atlas.get_chart(cur_id).cut(edge)

    return cut_charts_dict