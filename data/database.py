import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    """
    Represents a user in the system.
    The User model is used to store user-related data in the database. It includes the user's ID and name.

    Attributes:
        id (int): The primary key identifier for the user.
        name (str): The name of the user.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    movies = db.relationship("Movie", backref="user", lazy=True)

    def __repr__(self):
        """
        Returns a string representation of the User instance.
        This method is used to provide a human-readable representation of the user object, typically for debugging purposes.

        Returns:
            str: A string representing the User instance.
        """
        return f"<User(id={self.id}, name={self.name})>"


class Movie(db.Model):
    """
    Represents a movie in the system.
    The Movie model stores information about a movie, including its name, director, release year, and rating.

    Attributes:
        id (int): The primary key identifier for the movie.
        name (str): The name of the movie.
        director (str): The name of the movie's director.
        year (int): The release year of the movie.
        rating (float): The rating of the movie (e.g., IMDb rating).
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    poster = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the Movie instance.
        This method provides a human-readable representation of the movie object, typically for debugging purposes.

        Returns:
            str: A string representing the Movie instance.
        """
        return f"<Movie(id={self.id}, name={self.name}, director={self.director})>"


def init_database(app):
    """
    Initializes the database for the Flask application.
    This function configures SQLAlchemy with the given Flask app, sets up the connection to the SQLite database,
    and ensures the necessary database tables are created if they do not already exist.

    Args:
        app (Flask): The Flask application instance to bind the database to.
    """
    db_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'movies.sqlite')

    data_folder = os.path.dirname(db_file_path)
    if not os.path.exists(data_folder):
        print(f"Creating directory: {data_folder}")
        os.makedirs(data_folder)

    if not os.path.exists(db_file_path):
        print(f"Creating database file: {db_file_path}")

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
    print("Database initialized and tables created.")
