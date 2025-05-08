import pytest
from unittest.mock import MagicMock
from data_manager import SQLiteDataManager


@pytest.fixture
def data_manager():
    """
    Fixture that creates and returns an instance of SQLiteDataManager
    for use in tests.

    Returns:
        SQLiteDataManager: An instance of the SQLiteDataManager class.
    """
    return SQLiteDataManager("test.db")


def test_get_all_users(data_manager):
    """
    Tests the get_all_users method of the SQLiteDataManager class.

    This test mocks the database session and simulates the retrieval
    of all users from the database. It then checks if the returned
    users have the correct name values.

    Args:
        data_manager (SQLiteDataManager): The instance of SQLiteDataManager
                                          used to interact with the database.

    Asserts:
        - The length of the returned users list should be 2.
        - The name of the first user should be "John Doe".
        - The name of the second user should be "Jane Doe".
    """
    mock_session = MagicMock()
    data_manager.Session = MagicMock(return_value=mock_session)

    mock_user1 = MagicMock(id=1)
    mock_user1.name = "John Doe"

    mock_user2 = MagicMock(id=2)
    mock_user2.name = "Jane Doe"

    mock_session.query.return_value.all.return_value = [mock_user1, mock_user2]

    users = data_manager.get_all_users()

    assert len(users) == 2
    assert users[0].name == "John Doe"
    assert users[1].name == "Jane Doe"


def test_add_user(data_manager):
    """
    Tests the add_user method of the SQLiteDataManager class.

    This test mocks the database session, simulates adding a user to the
    database, and checks if the session's add and commit methods were called
    correctly. It ensures that the add_user method attempts to add the user
    to the session and commits the transaction.

    Args:
        data_manager (SQLiteDataManager): The instance of SQLiteDataManager
                                          used to interact with the database.

    Asserts:
        - The session's add method is called with the mock user.
        - The session's commit method is called once to save the changes.
    """
    mock_session = MagicMock()
    data_manager.Session = MagicMock(return_value=mock_session)

    mock_user = MagicMock(name="John Doe")

    data_manager.add_user(mock_user)

    mock_session.add.assert_called_with(mock_user)
    mock_session.commit.assert_called_once()


def test_update_movie(data_manager):
    """
    Tests the update_movie method of the SQLiteDataManager class.

    This test mocks the database session and simulates the update of an
    existing movie in the database. It checks if the session's commit method
    is called after updating the movie details.

    Args:
        data_manager (SQLiteDataManager): The instance of SQLiteDataManager
                                          used to interact with the database.

    Asserts:
        - The session's commit method is called once to save the updated movie.
    """
    mock_session = MagicMock()
    data_manager.Session = MagicMock(return_value=mock_session)

    mock_movie = MagicMock(id=1, name="Old Name", director="Director", year=2000, rating=5)

    mock_session.query.return_value.get.return_value = mock_movie

    mock_movie.name = "New Name"
    data_manager.update_movie(mock_movie)

    mock_session.commit.assert_called_once()


def test_delete_movie(data_manager):
    """
    Tests the delete_movie method of the SQLiteDataManager class.

    This test mocks the database session and simulates the deletion of an
    existing movie from the database. It ensures that the session's delete and
    commit methods are called correctly.

    Args:
        data_manager (SQLiteDataManager): The instance of SQLiteDataManager
                                          used to interact with the database.

    Asserts:
        - The session's delete method is called with the mock movie.
        - The session's commit method is called once to finalize the deletion.
    """
    mock_session = MagicMock()
    data_manager.Session = MagicMock(return_value=mock_session)

    mock_movie = MagicMock(id=1, name="Old Movie", director="Director", year=2000, rating=5)
    mock_session.query.return_value.get.return_value = mock_movie

    data_manager.delete_movie(mock_movie.id)

    mock_session.delete.assert_called_with(mock_movie)
    mock_session.commit.assert_called_once()


def test_get_user_movies_not_found(data_manager):
    """
    Tests the get_user_movies method of the SQLiteDataManager class when the user
    is not found.

    This test simulates a scenario where the user ID passed to the get_user_movies
    method does not exist in the database. It verifies that a ValueError is raised
    when no movies are found for the specified user.

    Args:
        data_manager (SQLiteDataManager): The instance of SQLiteDataManager
                                          used to interact with the database.

    Asserts:
        - A ValueError is raised when trying to retrieve movies for a non-existent user.
    """
    mock_session = MagicMock()
    data_manager.Session = MagicMock(return_value=mock_session)
    mock_session.query.return_value.get.return_value = None

    with pytest.raises(ValueError):
        data_manager.get_user_movies(999)

