from app import app
from app.config.mysqlconnection import connectToMySQL
from app.utils import movies_scrapper


class Movie:
    db_name = 'top_25'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.year = data['year']
        self.genre = data['genre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_top_25_movies(cls):
        top_25_movies = movies_scrapper.scrap_top_25_movies_from()
        return top_25_movies

    @classmethod
    def get_all_movies(cls):
        query = "SELECT * FROM movies"
        result = connectToMySQL(cls.db_name).query_db(query)
        return result

    # add movie

    @classmethod
    def add_movie(cls, data):
        query = "INSERT INTO movies (title, year, genre)\
            VALUES (%(title)s, %(year)s, %(genre)s)"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def add_favorite(cls, data):
        query = "SELECT id FROM favorites WHERE user_id = %(user_id)s AND movie_id = %(movie_id)s"
        exist = connectToMySQL(cls.db_name).query_db(query, data)
        if not exist:
            query = "INSERT INTO favorites (user_id, movie_id) VALUES (%(user_id)s, %(movie_id)s)"
            results = connectToMySQL(cls.db_name).query_db(query, data)
            return results
        else:
            return "La película ya está en favoritos"

    @classmethod
    def show_favorites(cls, data):
        query = "SELECT movies.id, movies.title, movies.year, movies.genre FROM favorites JOIN movies ON movies.id = favorites.movie_id WHERE user_id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result

    @classmethod
    def delete_favorite(cls, data):
        query = "DELETE FROM favorites WHERE movie_id = %(id)s AND user_id=%(user_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    # Get movie by title movie

    @classmethod
    def get_movie_by_title(cls, data):
        query = "SELECT * FROM movies WHERE title = %(title)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        movie = Movie(result[0])
        return movie

    @classmethod
    def is_favorite(cls, data):
        query = "SELECT movies.id, movies.title, movies.year, movies.genre FROM movies JOIN favorites ON movies.id = favorites.movie_id JOIN users ON users.id = favorites.user_id WHERE users.id = %(user_id)s AND movies.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result
