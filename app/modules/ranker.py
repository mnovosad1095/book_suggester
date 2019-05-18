from charts.chartADT import ChartMultiSet
import os
import sys
import datetime


class RankCrawler:
    """
    Class for going through charts and finding books
    for user
    """
    def __init__(self, recommended):
        self._charts = ChartMultiSet()
        self._charts.load(os.path.join(sys.path[1], 'data', 'charts.json'))
        self._good_books = []
        self._recommended = recommended

    def get_books(self, min_pages, max_pages):
        """
        Searches for books, which have capable number of pages and
        are in high chart positions
        :param min_pages: int
        :param max_pages: int
        :return: list(Book obj)
        """
        used_books = set(self._recommended)
        next_date = None
        start = datetime.datetime.today()
        while len(self._good_books) < 3:
            if (datetime.datetime.today()-start).seconds > 150:
                used_books = set()
                next_date = None
            if next_date is not None:
                next_date = chart.next_date
                chart = self._charts[next_date]
            else: chart = self._charts[datetime.datetime.today()]
            if chart:
                for book in chart.books:
                    if book.name not in used_books \
                            and min_pages * 0.8 <= book.pages <= max_pages * 1.2:
                        self._good_books.append(book), used_books.add(book.name)
                self._recommended.extend(self._good_books)
                next_date = chart.next_date
            else:
                break
        self._charts.save_charts(os.path.join(sys.path[1], 'data', 'charts.json'))
        return self._good_books


if __name__ == '__main__':
    ranker = RankCrawler([])
    books = ranker.get_books(250, 900)
    print(books)
