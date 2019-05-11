from chartADT import ChartMultiSet
import datetime


class RankCrawler:
    """
    Class for going through charts and finding books
    for user
    """
    def __init__(self, recommended):
        self._charts = ChartMultiSet()
        self._charts.load('charts.json')
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
        used_books = set()
        next_date = None
        while len(self._good_books) < 4:
            if next_date is not None:
                next_date = chart.next_date
                chart = self._charts[next_date]
            else: chart = self._charts[datetime.datetime.today()]
            if chart:
                for book in chart.books:
                    if book.name not in used_books \
                            and book.name not in self._recommended \
                            and min_pages * 0.9 <= book.pages <= max_pages * 1.1:
                        self._good_books.append(book), used_books.add(book.name)
                self._recommended.extend(self._good_books)
            else:
                break
        self._charts.save_charts('charts.json')
        return self._good_books


if __name__ == '__main__':
    ranker = RankCrawler([])
    books = ranker.get_books(250, 900)
    print(books)
