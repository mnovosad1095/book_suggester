import json
import os
import sys


class User:
    def __init__(self, userID, username=None):
        self.userID = userID
        self.username = username
        self._password = None
        self._books = []
        self.load_data()

    def load_data(self):
        """
        Loads user's data from json file
        :return:None
        """
        file_name = os.path.join(sys.path[1], 'users', 'user_data.json')
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data: pass
            try:
                usr_data = data['users'][str(self.userID)]
                if usr_data['books']: self._books.extend(usr_data['books'])
                self._password = usr_data['password']
            except KeyError: pass

    def update(self):
        """
        Updates it's data in json file
        :return: None
        """
        file_name = os.path.join(sys.path[1], 'users', 'user_data.json')
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data['users'][str(self.userID)] = {
                'username': self.username,
                'books': [i.name for i in self.books if type(i) != str],
                'password': self._password
            }
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def update_books(self, books):
        """
        Updates list of books, which were recommended to a user
        :param books:
        :return:
        """
        if self._books:
            self._books.extend(books)
            self.books = self._books
        else: self.books = books

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
        print(value )
        self._books = value
        self.update()

    @staticmethod
    def get_biggest_id():
        """
        Extracts maxID from user_data file
        :return: int
        """
        file_name = os.path.join(sys.path[1], 'users', 'user_data.json')
        f = open(file_name)
        data = json.load(f)
        return int(data['maxID'])

if __name__ == '__main__':
    import os
    import sys
    print(str(os.path))
    print(sys.path)