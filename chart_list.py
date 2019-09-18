import numpy as np
from atlas import Atlas
from chart import Chart

class ChartList:

    INIT_ID = Atlas.INIT_ID

    def __init__(self):
        self.ids = set()
        self.charts = dict()
        self._new_id = INIT_ID

    def import_from_atlas(self, atlas):
        # Get the IDs of the charts and put them in a local set
        self._import_ids_from_atlas(atlas)

        # Initialize a new local list to store charts
        charts = dict()

        # For each id create a new chart and store it in charts
        for tmp_id in sorted(self.ids):
            charts[tmp_id] = Chart.from_atlas(atlas, tmp_id)

        # Update the attributes
        self.charts = charts

    def _import_ids_from_atlas(atlas):
        # Create an empty set for the IDs
        ids = set()
        max_id = INIT_ID

        # Run over the graphs searching for IDs
        for i in range(atlas.shape[0]):
            for j in range(atlas.shape[1]):
                tmp_id = atlas[i, j]
                if tmp_id != Atlas.EMPTY:
                    ids.add(tmp_id)
                    if max_id < tmp_id:
                        max_id = tmp_id

        # Update the attributes
        self.ids = ids
        self._new_id = max_id