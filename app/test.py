import unittest
from chartADT import ChartMultiSet
from books import Chart
import datetime


class TestChartAdt(unittest.TestCase):

    def setUp(self):
        self.charts = ChartMultiSet()
        self.chart1 = Chart([], '2019-05-12', '2019-05-07')
        self.chart2 = Chart([], '2019-05-07', '2019-05-01')

    def test_append(self):
        self.charts.append(self.chart1)
        self.charts.append(self.chart2)
        self.assertEqual(
            self.charts.get_latest_date(),
            datetime.datetime(2019, 5, 12)
        )
        self.assertEqual(
            self.charts.get_oldest_date(),
            datetime.datetime(2019, 5, 7)
        )

    def test_get(self):
        date = datetime.datetime(2019, 5, 12)
        chart = self.charts[date]
        self.assertEqual(
            chart.books[0].name,
            'WHERE THE CRAWDADS SING'
        )



if __name__ == '__main__':
    unittest.main()
    dat = datetime.datetime(2019, 5, 12)
    ad = ChartMultiSet()
    chart = ad[dat]
    print(chart)
    # c = Chart([], '2019-05-12', '2019-05-07')
    # c1 = Chart([], '2019-05-07', '2019-05-01')
    # adt = ChartMultiSet()
    # adt.append(c)
    # adt.append(c1)
    # print(adt.get_oldest_date())
    # print(adt.get_latest_date())