import numpy as np
from hierarchical_buffer import HierarchicalBuffer
from atlas import Atlas
from coord import Coord
from chart_list import ChartList
from chart import Chart

BLOCKED = -1

ORIENTATIONS = 1
MIRROR_X = 1
MIRROR_Y = 1

# list_cut_charts_dicts == [{chart_id_1: [cut_chart_1_1, cut_chart_1_2], ...}, ...]
# list_cut_charts_dicts == this is a list of cut charts, for each of the cuts
#                          dictionaries with the id of the cut chart as key,
#                          containing the resulting two charts for each cut
def pack_charts(chart_list, list_cut_charts_dicts=[dict(),]):
    # List of computed packed atlases
    atlas_list = list()

    # List of the computed packed atlases' scores
    score_list = list()

    # Run for each of the cuts
    for cut_charts_dict in list_cut_charts_dicts:
        # Create a new charts dictionary for each cut
        chart_dict = dict(chart_list.charts)
        new_id = chart_list._new_id

        # Replace the charts with the cut charts for each affected chart
        for key in cut_charts_dict:
            cut_charts_dict[key][0].chart_id = key
            chart_dict[key] = cut_charts_dict[key][0]
            cut_charts_dict[key][1].chart_id = new_id
            chart_dict[new_id] = cut_charts_dict[key][1]
            new_id += 1

        # Get a sorted list from big to small charts
        sorted_list_charts = _sorted_chart_dict(chart_dict)

        if not sorted_list_charts:
            raise RuntimeError('pack_charts: sorted_list_charts is empty')

        # Create atlas from the biggest chart
        atlas = Atlas.from_chart(sorted_list_charts[0])
        # Pop the biggest chart
        sorted_list_charts.pop(0)

        # Run as long as the list is not empty (pop every iteration)
        while sorted_list_charts:
            _add_chart_to_atlas(atlas, sorted_list_charts.pop(0))

        # Add the atlas to the list of computed packed atlases
        atlas_list.append(atlas)

        # Add the atlas's score to the list
        score_list.append(atlas.calc_score())

    # Find the atlas with the maximal score
    max_score_ind = 0
    for i in range(len(score_list)):
        if score_list[i] > score_list[max_score_ind]:
            max_score_ind = i

    # Return the atlas with the maximal score
    return (atlas_list[max_score_ind], score_list[max_score_ind])

def _sorted_chart_dict(chart_dict):
    return sorted(chart_dict.values(), reverse=True, key=lambda chart: chart.pixels)

def _add_chart_to_atlas(atlas, chart):
    current_pixels = None
    current_i = None
    current_j = None
    current_rotation = chart.orientation
    current_mirror_x = chart.mirror[0]
    current_mirror_y = chart.mirror[1]

    is_break = False

    for mirror_x in range(MIRROR_X):
        for mirror_y in range(MIRROR_Y):
            for orientation in range(ORIENTATIONS):
                for i in range(atlas.height + 1):
                    for j in range(atlas.width + 1):
                        added_pixels = _try_add(atlas, chart, i, j)
                        if added_pixels == 0:
                            current_pixels = added_pixels
                            current_i = i
                            current_j = j
                            current_rotation = chart.orientation
                            current_mirror_x = chart.mirror[0]
                            current_mirror_y = chart.mirror[1]
                            is_break = True
                            break
                        if added_pixels != BLOCKED and (not current_pixels or added_pixels < current_pixels):
                            current_pixels = added_pixels
                            current_i = i
                            current_j = j
                            current_rotation = chart.orientation
                            current_mirror_x = chart.mirror[0]
                            current_mirror_y = chart.mirror[1]
                    if is_break:
                        break
                if is_break:
                    break

                chart.rotate_clockwise()
            chart.mirror_x()
        chart.mirror_y()

    chart.restore_orientation_mirror(current_rotation, (current_mirror_x, current_mirror_y))

    _add(atlas, chart, current_i, current_j)

def _add(atlas, chart, row, col, is_try=False):
    for i in range(min(chart.height, atlas.height - row)):
        for j in range(min(chart.width, atlas.width - col)):
            if chart[i, j] == Chart.OCCUPIED:
                if atlas[row + i, col + j] != Atlas.EMPTY:
                    if is_try:
                        return BLOCKED
                    else:
                        raise RuntimeError('pack_charts._add: Cannot add a chart to a blocked area')
                if not is_try:
                    atlas[row + i, col + j] = chart.chart_id

    included_height = min(atlas.height - row, chart.height)
    included_width = min(atlas.width - col, chart.width)
    remainder_height = max(chart.height - included_height, 0)
    remainder_width = max(chart.width - included_width, 0)
    new_height = atlas.height + remainder_height
    new_width = atlas.width + remainder_width

    if is_try:
        return (new_height * new_width) - (atlas.height * atlas.width)
    elif remainder_height > 0 or remainder_width > 0:
        # The previous atlas's height and width
        old_height = atlas.height
        old_width = atlas.width
        old_arr = atlas.arr

        # Reshape the atlas to the new expanded size
        atlas.shape = (new_height, new_width)
        atlas.arr = np.ndarray(shape=atlas.shape, dtype=Atlas.DATA_TYPE)
        atlas.arr.fill(Atlas.EMPTY)
        for i in range(old_height):
            for j in range(old_width):
                atlas.arr[i, j] = old_arr[i, j]
        # Throws an exception for some reason
        # atlas.arr = atlas.arr.reshape(atlas.shape[0], atlas.shape[1]) 
        atlas.rows = new_height
        atlas.cols = new_width
        atlas.height = new_height
        atlas.width = new_width
        atlas.chart_list.ids.add(chart.chart_id)
        atlas.chart_list.charts[chart.chart_id] = chart
        if chart.chart_id + 1 > atlas.chart_list._new_id:
            atlas.chart_list._new_id = chart.chart_id + 1

        # Fill the new parts with Atlas.EMPTY
        # _fill(atlas, old_height, old_width, new_height, new_width)

        # Insert the remaining chart to the new parts
        if included_height != chart.height:
            for i in range(included_height):
                for j in range(included_width, chart.width):
                    if chart[i, j] == Chart.OCCUPIED:
                        atlas[row + i, col + j] = chart.chart_id
        for i in range(included_height, chart.height):
            for j in range(chart.width):
                if chart[i, j] == Chart.OCCUPIED:
                    atlas[row + i, col + j] = chart.chart_id

def _try_add(atlas, chart, row, col):
    return _add(atlas, chart, row, col, is_try=True)

def _fill(atlas, old_height, old_width, new_height, new_width):
    # Fill the new width first if it exists (row major for better performance)
    if old_width != new_width:
        for i in range(old_height):
            for j in range(old_width, new_width):
                atlas[i, j] = Atlas.EMPTY

    # Fill the new height
    for i in range(old_height, new_height):
        for j in range(new_width):
            atlas[i, j] = Atlas.EMPTY
