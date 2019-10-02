import numpy as np
from atlas import Atlas
from chart import Chart
from copy import deepcopy

class ChartList:

    INIT_ID = Atlas.INIT_ID

    def __init__(self):
        self.ids = set()
        self.charts = dict()
        self._new_id = ChartList.INIT_ID

    @classmethod
    def copy(cls, chart_list):
        obj = cls()

        obj.ids = set(chart_list.ids)
        for key in chart_list.charts:
            obj.charts[key] = Chart.copy(chart_list.charts[key])
        obj._new_id = chart_list._new_id

        return obj

    def import_from_atlas(self, atlas):
        # Get the IDs of the charts and put them in a local set
        self._import_ids_from_atlas(atlas)

        # Initialize a new local list to store charts
        charts = dict()

        # For each id create a new chart and store it in charts
        for cur_id in sorted(self.ids):
            charts[cur_id] = Chart.from_atlas(atlas, cur_id)

        # Update the attributes
        self.charts = charts

    def _import_ids_from_atlas(self, atlas):
        # Create an empty set for the IDs
        ids = set()
        max_id = ChartList.VERTICAL

        # Run over the graphs searching for IDs
        for i in range(atlas.rows):
            for j in range(atlas.cols):
                cur_id = atlas[i, j]
                if cur_id != Atlas.EMPTY:
                    ids.add(cur_id)
                    if max_id == ChartList.VERTICAL or max_id < cur_id:
                        max_id = cur_id

        # Update the attributes
        self.ids = ids
        self._new_id = max_id + 1

    def remove(self, chart_id, correct=False):
        chart = None
        if chart_id in self.ids:
            self.ids.remove(chart_id)
            chart = self.charts.pop(chart_id)
        if correct:
            self.correct_ids()
        return chart

    def add(self, chart, copy=False, correct=False):
        dst_chart = chart
        if copy == True:
            dst_chart = Chart.copy(chart)

        if dst_chart.chart_id == None:
            dst_chart.chart_id = self._new_id
            self._new_id += 1
        elif dst_chart.chart_id in self.ids:
            raise Exception('chart_id already exists in ChartList.ids')

        self.ids.add(dst_chart.chart_id)
        self.charts[dst_chart.chart_id] = dst_chart

        if correct:
            self.correct_ids()

    def replace(self, old_chart_id, new_chart, copy=False, correct=False):
        if old_chart_id not in self.ids:
            raise Exception('chart_id to be replaced is not in ChartList.ids')
        if new_chart is self.charts[old_chart_id]:
            return

        dst_chart = new_chart
        if copy == True:
            dst_chart = Chart.copy(new_chart)

        old_chart = self.charts[old_chart_id]
        new_chart_id = dst_chart.chart_id
        dst_chart.chart_id = old_chart_id
        self.charts[old_chart_id] = dst_chart

        if new_chart_id != None and new_chart_id in self.ids:
            self.charts[new_chart_id] = old_chart

        if correct:
            self.correct_ids()

        return old_chart


    def correct_ids(self):
        li = list(self.ids)
        li.sort()
        it = iter(li)
        prv = next(it)
        if prv != Chart.INIT_ID:
            self.ids.remove(prv)
            self.ids.add(Chart.INIT_ID)
            self.charts[Chart.INIT_ID] = self.charts.pop(prv)
        for cur in it:
            if cur != prv + 1:
                self.ids.remove(cur)
                self.ids.add(prv + 1)
                self.charts[prv + 1] = self.charts.pop(cur)
            prv = cur
        self._new_id = max(self.ids) + 1
