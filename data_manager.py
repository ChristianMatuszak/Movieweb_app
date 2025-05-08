import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
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
        try:
            users = session.query(User).all()
            return users
        except SQLAlchemyError as error:
            session.rollback()
            logging.error(f"Error retrieving users: {error}")
            raise SQLAlchemyError(f"Error retrieving users: {error}")
        finally:
            session.close()

    def get_user_movies(self, user_id):
        """
        Retrieves all movies for a specific user.

        Args:
            user_id (int): The ID of the user whose movies are to be retrieved.

        Returns:
            list: A list of all movies for the specified user.
        """
        session = self.Session()
        try:
            user = session.query(User).get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            return user.movies
        except ValueError as error:
            logging.error(f"ValueError: {error}")
            raise ValueError(f"User with ID {user_id} not found.")
        except SQLAlchemyError as error:
            logging.error(f"Error retrieving movies for user {user_id}: {error}")
            raise SQLAlchemyError(f"Error retrieving movies for user {user_id}: {error}")
        finally:
            session.close()

    def add_user(self, user):
        """
        Adds a new user to the database.

        Args:
            user (User): The User instance to be added.
        """
        session = self.Session()
        try:
            session.add(user)
            session.commit()
        except SQLAlchemyError as error:
            session.rollback()
            logging.error(f"Error adding user: {error}")
            raise SQLAlchemyError(f"Error adding user: {error}")
        finally:
            session.close()

    def add_movie(self, movie):
        """
        Adds a new movie to the database.

        Args:
            movie (Movie): The Movie instance to be added.
        """
        session = self.Session()
        try:
            session.add(movie)
            session.commit()
        except SQLAlchemyError as error:
            session.rollback()
            logging.error(f"Error adding movie: {error}")
            raise SQLAlchemyError(f"Error adding movie: {error}")
        finally:
            session.close()

    def update_movie(self, movie):
        """
        Updates the details of a specific movie in the database.

        Args:
            movie (Movie): The Movie instance with updated details.
        """
        session = self.Session()
        try:
            existing_movie = session.query(Movie).get(movie.id)
            if not existing_movie:
                raise ValueError(f"Movie with ID {movie.id} not found for update.")
            existing_movie.name = movie.name
            existing_movie.director = movie.director
            existing_movie.year = movie.year
            existing_movie.rating = movie.rating
            session.commit()
        except ValueError as error:
            logging.warning(f"ValueError: {error}")
            raise ValueError(f"Movie with ID {movie.id} not found for update.")
        except SQLAlchemyError as error:
            session.rollback()
            logging.error(f"Error updating movie {movie.id}: {error}")
            raise SQLAlchemyError(f"Error updating movie {movie.id}: {error}")
        finally:
            session.close()

    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database by its ID.

        Args:
            movie_id (int): The ID of the movie to be deleted.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).get(movie_id)
            if not movie:
                raise ValueError(f"Movie with ID {movie_id} not found for deletion.")
            session.delete(movie)
            session.commit()
        except ValueError as error:
            logging.warning(f"ValueError: {error}")
            raise ValueError(f"Movie with ID {movie_id} not found for deletion.")
        except SQLAlchemyError as error:
            session.rollback()
            logging.error(f"Error deleting movie {movie_id}: {error}")
            raise SQLAlchemyError(f"Error deleting movie {movie_id}: {error}")
        finally:
            session.close()
