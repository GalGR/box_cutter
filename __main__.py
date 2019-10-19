import os
import sys
from PIL import Image
from atlas import Atlas

from cut_charts import cut_charts
from pack_charts import pack_charts

ITERATIONS = 1

def main():
    # path = 'input.bmp'
    # im = Image.open(path)

    path = sys.argv[1]
    im = Image.open(path)

    atlas = Atlas.from_image(im)

    # atlas = pack_charts(atlas.chart_list)[0]

    for iteration in range(ITERATIONS):
        li = cut_charts(atlas)
        atlas = pack_charts(atlas.chart_list, li)

    new_im = atlas.to_image()

    new_path = path[:len(path) - 4] + '_repacked.bmp'
    new_im.save(new_path)

if __name__ == '__main__':
    main()