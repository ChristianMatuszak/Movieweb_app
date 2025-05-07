from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """
    Abstract base class for data manager interfaces.
    This defines the methods for interacting with the database,
    which must be implemented by any concrete data manager class.
    """

    @abstractmethod
    def get_all_users(self):
        """
        Retrieves all users from the database.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieves all movies of a specific user.

        Args:
            user_id (int): The ID of the user whose movies are to be retrieved.
        """
        pass

    @abstractmethod
    def add_user(self, user):
        """
        Adds a new user to the database.

        Args:
            user (User): The User instance to be added.
        """
        pass

    @abstractmethod
    def add_movie(self, movie):
        """
        Adds a new movie to the database.

        Args:
            movie (Movie): The Movie instance to be added.
        """
        pass

    @abstractmethod
    def update_movie(self, movie):
        """
        Updates a movie's details in the database.

        Args:
            movie (Movie): The Movie instance with updated details.
        """
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database.

        Args:
            movie_id (int): The ID of the movie to be deleted.
        """
        pass
