import os
import tempfile
import pytest
from flask import Flask
from data.database import db, init_database, User, Movie

@pytest.fixture
def test_app():
    """
    Creates and configures a temporary Flask application for testing.
    Uses a temporary SQLite file that is properly closed and cleaned up to avoid
    Windows file locking issues during deletion.
    """
    with tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False) as tmp:
        db_path = tmp.name

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app

    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            print(f"Could not delete temporary test DB at {db_path}")


@pytest.fixture
def session(test_app):
    """
    Provides a database session for use in tests.

    This fixture ensures that tests operate within the Flask application context,
    providing access to the SQLAlchemy session for adding and querying test data.

    Args:
        test_app (Flask): The Flask application with initialized database.

    Returns:
        SQLAlchemy.Session: A scoped session to interact with the test database.
    """
    with test_app.app_context():
        yield db.session


def test_user_movie_relationship(session):
    """
    Tests the relationship between User and Movie models.

    This test verifies that when a User is created and linked to multiple Movie instances,
    the relationship behaves correctly. It checks that the movies can be accessed via the user
    and that the foreign key linkage is properly maintained.
    """
    user = User(name="Test User")
    movie1 = Movie(name="Movie 1", director="Dir 1", year=2000, rating=7.0, poster="url1", user=user)
    movie2 = Movie(name="Movie 2", director="Dir 2", year=2001, rating=8.0, poster="url2", user=user)

    session.add(user)
    session.add_all([movie1, movie2])
    session.commit()

    queried_user = User.query.first()
    assert queried_user.name == "Test User"
    assert len(queried_user.movies) == 2
    assert queried_user.movies[0].name == "Movie 1"


def test_init_database_creates_file():
    """
    Tests that `init_database` creates the database file and tables.

    This test sets up a minimal Flask app, calls `init_database`, and checks that
    the database file was created on the filesystem. It verifies that the initialization
    logic correctly sets up the DB structure as expected.
    """
    app = Flask(__name__)
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data', 'movies.sqlite')

    if os.path.exists(db_path):
        os.remove(db_path)

    init_database(app)

    assert os.path.exists(db_path)
