import pytest
from flask.testing import FlaskClient
from data.database import db, User, Movie
from app import app


@pytest.fixture
def client() -> FlaskClient:
    """
    Creates a Flask test client for testing the application routes.

    This fixture initializes a test database, sets up the Flask app context,
    and creates the necessary database tables before each test.
    After each test, the database tables are dropped.

    Returns:
        FlaskClient: The Flask test client used to simulate requests to the app.
    """
    app.config['SECRET_KEY'] = 'testsecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def test_home(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Movie Database' in response.data


def test_list_users(client):
    """
    Tests the route that lists all users.

    This test creates a user in the test database, sends a GET request to the
    '/users' route, and checks if the user's name appears in the response.

    Args:
        client (FlaskClient): The Flask test client used to send requests to the app.
    """
    user = User(name="John Doe")
    db.session.add(user)
    db.session.commit()

    response = client.get('/users')
    assert response.status_code == 200
    assert b"John Doe" in response.data


def test_add_user(client):
    """
    Tests the route for adding a new user.

    This test sends a POST request with a user's name, checks if the response
    redirects to the user list page, and ensures that the new user has been added to the database.

    Args:
        client (FlaskClient): The Flask test client used to send requests to the app.
    """
    response = client.post('/add_user', data={'name': 'Jane Doe'})
    assert response.status_code == 302  # Check for redirect
    assert User.query.filter_by(name='Jane Doe').first() is not None


def test_add_movie(client):
    """
    Tests the route for adding a new movie to a user's collection.

    This test creates a user, sends a POST request to add a movie to that user's collection,
    and ensures that the movie appears in the database.

    Args:
        client (FlaskClient): The Flask test client used to send requests to the app.
    """
    user = User(name="John Doe")
    db.session.add(user)
    db.session.commit()

    response = client.post(f'/add_movie/{user.id}', data={'title': 'Top Gun'})
    assert response.status_code == 302
    assert Movie.query.filter_by(name='Top Gun').first() is not None


def test_update_movie(client):
    """
    Tests the route for updating an existing movie's information.

    This test creates a user, adds a movie, then sends a POST request to update that movie's details,
    and ensures the changes are reflected in the database.

    Args:
        client (FlaskClient): The Flask test client used to send requests to the app.
    """
    user = User(name="John Doe")
    db.session.add(user)
    db.session.commit()

    movie = Movie(name="Top Gun", director="Tony Scott", year=1986, rating=6.9, user_id=user.id)
    db.session.add(movie)
    db.session.commit()

    response = client.post(f'/users/{user.id}/update_movie/{movie.id}', data={
        'name': 'Top Gun: Maverick',
        'director': 'Joseph Kosinski',
        'year': '2022',
        'rating': '7.8'
    })
    assert response.status_code == 302
    updated_movie = Movie.query.get(movie.id)
    assert updated_movie.name == 'Top Gun: Maverick'
    assert updated_movie.director == 'Joseph Kosinski'
    assert updated_movie.year == 2022
    assert updated_movie.rating == 7.8


def test_delete_movie(client):
    """
    Tests the route for deleting a movie from a user's collection.

    This test creates a user, adds a movie, sends a POST request to delete that movie,
    and ensures the movie is removed from the database.

    Args:
        client (FlaskClient): The Flask test client used to send requests to the app.
    """
    user = User(name="John Doe")
    db.session.add(user)
    db.session.commit()

    movie = Movie(name="Top Gun", director="Tony Scott", year=1986, rating=6.9, user_id=user.id)
    db.session.add(movie)
    db.session.commit()

    response = client.post(f'/users/{user.id}/delete_movie/{movie.id}')
    assert response.status_code == 302
    deleted_movie = Movie.query.get(movie.id)
    assert deleted_movie is None


def test_404_error(client):
    """
    Tests the 404 error handler.

    This test sends a GET request to a non-existent route and checks if the response
    status code is 404 and if the 404 error page is displayed.

    Args:
        client (FlaskClient): The Flask test client used to send requests to the app.
    """
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b"404 - Page Not Found" in response.data




