from flask import Flask,redirect, render_template, request, url_for, make_response
import constants
from user import User
from books import BookRecommender, books_to_choose
app = Flask(__name__)
app.config['SECRET_KEY'] = 'blagdfgdfgdfg'


@app.route('/')
def home():
    userId = request.cookies.get('userID', default=False)
    if userId:
        return render_template('home.html', context={'userid': userId})
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=["GET", 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        resp = make_response(render_template('recom.html'))
        constants.userID += 1
        resp.set_cookie('userID', str(constants.userID))
        resp.set_cookie('username', username)
        user = User(constants.userID, username=username)
        user.password = password
        return resp

    return render_template('signbase.html', title='Sign',)


@app.route('/bookpage', methods=['GET', 'POST'])
def book_page():
    userID = request.cookies.get('userID', default=False)
    username = request.cookies.get('username', default=False)
    if request.method == 'GET':
        if userID:
            user = User(userID, username=username)
            if user.has_books():
                return render_template('recom.html', context={'has_books': True})
            else:
                return render_template('recom.html', context={
                    'has_book': False,
                    'books': books_to_choose
                })
        else:
            return redirect(url_for('login'))

    elif request.method == 'POST':
        user = User(userID)
        try:
            books = request.form['books']
            user.books = books
        finally:
            max_pages = request.form['max_pages']
            recommender = BookRecommender(user)
            books = recommender.recommend(max_pages)
            return render_template('books.html', context={'books': books,
                                                          'pages': max_pages})


if __name__ == "__main__":
    app.run()
