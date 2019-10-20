import os
import sys
from PIL import Image
from atlas import Atlas

from cut_charts import cut_charts
from pack_charts import pack_charts

from box_queue import BoxQueue
from pack_charts import ORIENTATIONS
from pack_charts import MIRROR_X
from pack_charts import MIRROR_Y
ITERATIONS = 8
SCORE_RATIO = 0.7

def is_int(obj):
    if (type(obj) == int):
        return True
    try:
        int(obj)
        return True
    except ValueError:
        return False

def is_float(obj):
    if (type(obj) == float):
        return True
    try:
        float(obj)
        return True
    except ValueError:
        return False

def main():
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and (sys.arv[1] == '-h' or sys.argv[1] == '/h' or sys.argv[1] == '--help' or sys.argv[1] == '-help' or sys.argv[1] == 'help')):
        print('Usage: box_cutter PATH_TO_IMAGE FLAGS')
        print('(The image needs to be a bitmap file, and should not be more than 128x128 pixels)')
        print('\t-n INT\t\tMax number of void boxes to consider')
        print('\t-i INT\t\tMax number of cut-repack iterations')
        print('\t-s FLOAT\tMax ratio between starting score to current score')
        print('\t-r\t\tEnable chart rotation for the packing phase')
        print('\t-x\t\tEnable upside-down mirroring')
        print('\t-y\t\tEnable left-to-right mirroring')
        return

    path = sys.argv[1]
    path.strip(' \'\"')
    im = Image.open(path)

    prv_arg = None
    for arg in sys.argv[2:]:
        if prv_arg == '-n':
            if is_int(arg) == int:
                BoxQueue.N = int(arg)
            else:
                raise Exception('__main__.py: The argument following \'-n\' must be an int')
        if prv_arg == '-i':
            if is_int(arg) == int:
                ITERATIONS = int(arg)
            else:
                raise Exception('__main__.py: The argument following \'-i\' must be an int')
        if prv_arg == '-s':
            if is_int(arg) == int or is_float(arg) == float:
                SCORE_RATIO = int(arg)
            else:
                raise Exception('__main__.py: The argument following \'-s\' must be a float')
        if arg == '-r':
            ORIENTATIONS = 4
        if arg == '-x':
            MIRROR_X = 2
        if arg == '-y':
            MIRROR_Y = 2
        prv_arg = arg

    atlas = Atlas.from_image(im)

    (atlas, start_score) = pack_charts(atlas.chart_list)
    Atlas.MAX_AXIS = max(atlas.height, atlas.width)

    for iteration in range(ITERATIONS):
        atlas.chart_list.import_from_atlas(atlas) # Workaround for a bug
        li = cut_charts(atlas)
        (atlas, score) = pack_charts(atlas.chart_list, li)
        if (start_score / score) <= 0.7:
            break

    new_im = atlas.to_image()

    new_path = path[:len(path) - 4] + '_repacked.bmp'
    new_im.save(new_path)

if __name__ == '__main__':
    main()