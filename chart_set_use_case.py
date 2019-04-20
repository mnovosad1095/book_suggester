from chart_set import ChartMultiSet
from book_chart import Chart
import datetime


def get_new_chart():
    date = datetime.date
    charts = ChartMultiSet()
    charts.load('charts.json')
    if date > charts.get_latest_date():
        new_ch = Chart()
        return new_ch.get_latest()
    else:
        return ChartMultiSet[0]
