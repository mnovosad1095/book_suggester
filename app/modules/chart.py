import datetime


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
