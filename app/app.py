from flask import Flask,redirect, render_template, request, url_for, make_response
from hidden import constants
from user import User
from recommendation import BookRecommender


app = Flask(__name__)
app.config['SECRET_KEY'] = 'blagdfgdfgdfg'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['STATIC_AUTO_RELOAD'] = True


@app.route('/')
def home():
    """
    Function which represents landing page and
    redirects user to another pages
    :return: None
    """
    userId = request.cookies.get('userID', default=False)
    if userId:
        return redirect(url_for('book_page'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=["GET", 'POST'])
def login():
    """
    This is a login page, which takes users username
    to find his data in the file
    :return: None
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        id_usr = request.cookies.get('userID', False)
        if not id_usr:  id_usr = User.get_biggest_id() + 1
        user = User(id_usr, username=username)
        user.password = password
        resp = make_response(render_template('recom.html', context={'user': user}))
        resp.set_cookie('userID', str(constants.userID))
        resp.set_cookie('username', username)
        return resp

    return render_template('signbase1.html', title='Sign')


@app.route('/bookpage', methods=['GET', 'POST'])
def book_page():
    """
    This is a page where user can select a range of pages
    and app will recommend him books
    :return: None
    """
    userID = request.cookies.get('userID', default=False)
    username = request.cookies.get('username', default=False)
    print(userID, username)
    if request.method == 'GET':
        if userID:
            user = User(userID, username=username)
            return render_template('recom.html', context={'user': user})
        else:
            return redirect(url_for('login'))

    elif request.method == 'POST':
        user = User(userID, username=username)
        try:
            books = request.form['books']
            user.books = books
        finally:
            pages = (int(request.form['Minimum_pages']), int(request.form['Max_pages']))
            recommender = BookRecommender(user)
            books = recommender.recommend(pages)
            return render_template('books.html', context={'books': books})


if __name__ == "__main__":
    app.run(host='0000')
