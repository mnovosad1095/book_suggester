from ranker import RankCrawler


class BookRecommender:
    """
    Class for recommending books
    """
    def __init__(self, user):
        self.recommended_books = user.books
        self.user = user

    def recommend(self, pages):
        """
        Recommends books by using New York Times best-sellers
        :param pages:
        :return: list(BookRanker obj)
        """
        ranker = RankCrawler(self.recommended_books)
        books = ranker.get_books(*pages)
        self.user.update_books(books)
        return books
