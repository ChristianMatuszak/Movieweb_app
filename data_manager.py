from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.database import User, Movie
from interfaces.data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    """
    A concrete implementation of DataManagerInterface for managing data in an SQLite database using SQLAlchemy.
    """

    def __init__(self, db_file_name):
        """
        Initializes the SQLiteDataManager with the SQLite database file.

        Args:
            db_file_name (str): The name of the SQLite database file.
        """
        self.db_file_name = db_file_name
        self.engine = create_engine(f'sqlite:///{db_file_name}')
        self.Session = sessionmaker(bind=self.engine)

    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            list: A list of all users in the database.
        """
        session = self.Session()
        users = session.query(User).all()
        session.close()
        return users

    def get_user_movies(self, user_id):
        """
        Retrieves all movies for a specific user.

        Args:
            user_id (int): The ID of the user whose movies are to be retrieved.

        Returns:
            list: A list of all movies for the specified user.
        """
        session = self.Session()
        user = session.query(User).get(user_id)
        if user:
            movies = user.movies
        else:
            movies = []
        session.close()
        return movies

    def add_user(self, user):
        """
        Adds a new user to the database.

        Args:
            user (User): The User instance to be added.
        """
        session = self.Session()
        session.add(user)
        session.commit()
        session.close()

    def add_movie(self, movie):
        """
        Adds a new movie to the database.

        Args:
            movie (Movie): The Movie instance to be added.
        """
        session = self.Session()
        session.add(movie)
        session.commit()
        session.close()

    def update_movie(self, movie):
        """
        Updates the details of a specific movie in the database.

        Args:
            movie (Movie): The Movie instance with updated details.
        """
        session = self.Session()
        existing_movie = session.query(Movie).get(movie.id)
        if existing_movie:
            existing_movie.name = movie.name
            existing_movie.director = movie.director
            existing_movie.year = movie.year
            existing_movie.rating = movie.rating
            session.commit()
        session.close()

    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database by its ID.

        Args:
            movie_id (int): The ID of the movie to be deleted.
        """
        session = self.Session()
        movie = session.query(Movie).get(movie_id)
        if movie:
            session.delete(movie)
            session.commit()
        session.close()
