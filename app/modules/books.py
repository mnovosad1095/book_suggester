from hidden.hidden import google_api
from googleapiclient.discovery import build


class BookRanker:
    """
    Class for representing a book
    """
    def __init__(self, isbn, rank, author, name, pages=None, img_url=None, descr=None):
        self.isbn = isbn
        self.rank = int(rank)
        self.author = author
        self.name = name
        self._pages = pages
        self.img_url = img_url
        self.descr = descr

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
        return "BookRanker(isbn=\"{}\", rank={}, author=\"{}\", name=\"{}\", pages={}, img_url=\"{}\", descr=\"{}\")".format(
            self.isbn,
            self.rank,
            self.author,
            self.name,
            self._pages,
            self.img_url,
            self.descr
        )


if __name__ == '__main__':
    from .user import User
    usr = User(1)
    rec = BookRecommender(usr)
    books = rec.recommend((100, 300))
    for i in books:
        print(type(i))

