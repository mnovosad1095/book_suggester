from hidden import nyt_api, google_api
from googleapiclient.discovery import build
from ranker import RankCrawler
import datetime


class BookRecommender:
    """
    Class for recommending books
    """
    def __init__(self, user):
        self._preferred_books = user.books
        self.recommended_books = user.recommended

    def recommend(self, pages):
        ranker = RankCrawler(self.recommended_books)
        books = ranker.get_books(*pages)
        return books


class BookRanker:
    """
    Class for representing a book
    """
    def __init__(self, isbn, rank, author, name, pages=None):
        self.isbn = isbn
        self.rank = int(rank)
        self.author = author
        self.name = name
        self._pages = pages

    @property
    def pages(self):
        if self._pages: return self._pages
        else:
            service = build('books', 'v1', developerKey=google_api)
            request = service.volumes().list(
                source='public',
                q='isbn = {}'.format(self.isbn))
            response = request.execute()
            try:
                self._pages = int(response['items'][0]['volumeInfo']['pageCount'])
            except:
                return 0
            return self._pages

    @pages.setter
    def pages(self, value):
        self._pages = value

    def __str__(self):
        return '{}, {}, {}'.format(
            self.name,
            self.author,
            self.pages
        )

    def __repr__(self):
        return "BookRanker(isbn='{}', rank={}, author='{}', name='{}', pages={})".format(
            self.isbn,
            self.rank,
            self.author,
            self.name,
            self._pages
        )


class Chart:
    """
    Class for representing a NYT chart
    """
    def __init__(self, books, date, next_date):
        self.books = books
        self.date = datetime.datetime(*[int(i) for i in date.split('-')])
        self.next_date = datetime.datetime(*[int(i) for i in next_date.split('-')])

    def to_dict(self):
        """
        Turn itself into dict, so it can be saved into Json
        :return: dict
        """
        return {
            'date': str(self.date).split()[0],
            'next_date': str(self.next_date).split()[0],
            'books': [repr(book) for book in self.books]
        }

    def __str__(self):
        return str([repr(book) for book in self.books]) + '\n{}'.format(self.date)


if __name__ == '__main__':
    crawl = RankCrawler([])
    chart = crawl.get_books(900, 100)
    c = Chart(chart, '11-11-11', '12-12-12')
    print(repr(c))
    # print([str(i) for i in chart])

    # isbn = '9781524796280'
    # service = build('books', 'v1', developerKey=google_api)
    # request = service.volumes().list(
    #     source='public',
    #     q='isbn = {}'.format(isbn))'\n'.join([str(i) for i in chart.books])
    # response = request.execute()
    # import pprint
    # pprint.pprint(response['items'][0]['volumeInfo']['pageCount'])
    # #pages = int(response['items'][0]['volumeInfo']['pageCount'])
    # #print(pages)
