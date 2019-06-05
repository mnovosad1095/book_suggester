from hidden.hidden import nyt_api
import json
import datetime
from requests import get
from books import BookRanker
from chart import Chart


class ChartMultiSet:
    """
    Class for representing abstract datatype for storing charts
    """
    def __init__(self):
        self._charts = []
        self._latest_date = None
        self._oldest_date = None
        self._dates = set()

    def get_oldest_date(self):
        """
        :return: private variable for date of the oldest chart
        """
        if self._oldest_date is None:
            return datetime.datetime(2050, 11, 11)
        else:
            return self._oldest_date

    def get_latest_date(self):
        """
        :return: private variable for date of the latest chart
        """
        if self._latest_date is None:
            return datetime.datetime(2050, 12, 11)
        else:
            return self._latest_date

    def load(self, filename):
        """
        Loads charts from selected file
        :param filename: str
        :return: None
        """
        with open(filename, 'r', encoding='utf-8') as chart_file:
            data = json.load(chart_file)
            try:
                self._latest_date = eval(data['latest_date'])
                self._oldest_date = eval(data['oldest_date'])
            except: self._latest_date = self._oldest_date = None
            charts = data['charts']
            for chart in charts:
                date, next_date = chart['date'], chart['next_date']
                books = [eval(i) for i in chart['books']]
                self._charts.append(Chart(books, date, next_date))

    def save_charts(self, file_name):
        """
        Saves charts into selected file
        :param file_name: str
        :return: None
        """
        with open(file_name, 'w', encoding='utf-8') as f:

            data = {
                'latest_date': repr(self._latest_date),
                'oldest_date': repr(self._oldest_date),
                'charts': [i.to_dict() for i in self._charts]
            }
            json.dump(data, f, indent=4)

    def _compare_dates(self, date):
        """
        Returns True if given date is between oldest and latest dates
        :param date: datetime obj
        :return: Bool
        """
        print(self._oldest_date, self._latest_date)
        if self._latest_date is None and self._oldest_date is None: return False
        latest = self._latest_date + datetime.timedelta(days=4)
        oldest = self._oldest_date - datetime.timedelta(days=4)
        return oldest.date() <= date.date() <= latest.date()

    def __getitem__(self, date):
        """
        If chart with given date is already in adt, returns it from memory,
        if not, it downloads it from internet
        :param date: datetime pbj
        :return: Chart obj
        """
        if self._compare_dates(date):
            print(self.get_latest_date(), self.get_oldest_date())
            return self._find_chart(date)
        else:
            req = 'https://api.nytimes.com/svc/books/v3/lists/{}/hardcover-fiction.json?api-key={}'.format(
                str(date.date()),
                nyt_api)
            response = get(req)
            data = response.json()
            try:
                books = [BookRanker(
                    book['primary_isbn13'],
                    int(book['rank']),
                    book['author'],
                    book['title'],
                    img_url=book['book_image'],
                    descr=book['description']
                    ) for book in data['results']['books'] if int(book['rank']) < 10]
                chart = Chart(books,
                              data['results']['published_date'],
                              data['results']['previous_published_date'])
                self.append(chart)
                return chart
            except:
                print(data)
                return None

    def _find_chart(self, date):
        """
        Private method for finding chart with given date
        :param date: datetime obj
        :return: Chart obj
        """
        previous = self._charts[0]
        for chart in self._charts[1:]:
            if chart.date < date <= previous.date:
                return previous
            previous = chart
        return self._charts[-1]

    def append(self, item):
        """
        Appends chart to others and updates its dates
        and sorts itself
        :param item: Chart obj
        :return: None
        """
        if str(item.date) not in self._dates:
            self._charts.append(item)
            self._charts.sort(key=lambda c: c.date, reverse=True)
            self._update_dates(item.date)
            self._dates.add(str(item.date))

    def _update_dates(self, date):
        """
        Private method for updating latest and oldest date
        :param date: datetime obj
        :return: None
        """
        if self._oldest_date is None and self._latest_date is None:
            self._oldest_date = date
            self._latest_date = date
        else:
            if date < self._oldest_date:
                self._oldest_date = date
            elif date > self._latest_date:
                self._latest_date = date

    def __repr__(self):
        return '{}\t{}'.format(self._oldest_date, self._latest_date)


if __name__ == '__main__':
    dates = [
        '2019-05-05',
        '2019-04-28',
        '2019-04-21',
        '2019-04-14'
    ]
    charts = ChartMultiSet()
    for i in dates:
        date = datetime.datetime(*[int(j) for j in i.split('-')])
        c = charts[date]
        print(c)
    print(charts)
    print(charts[datetime.datetime(2019, 4, 27)])

