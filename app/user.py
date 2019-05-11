import json


class User:
    def __init__(self, userID, username=None):
        self.userID = userID
        self.username = username
        data = self.load_data()
        self._books = data['books']
        self._password = data['password']

    def load_data(self):
        with open('users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if self.userID > int(data['maxID']):
                pass
            else:
                return data['users'][str(self.userID)]

    def update(self):
        with open('users.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data['users'][str(self.userID)] = {
                'username': self.username,
                'books': self.books,
                'password': self._password
            }

    def has_books(self):
        return self._books is not None

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
        self.update()

    @property
    def books(self):
        return self._books

    @books.setter
    def books(self, value):
        self._books = value
        self.update()



