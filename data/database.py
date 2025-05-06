import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)

    def __repr__(self):
        return f"<Movie(id={self.id}, name={self.name}, director={self.director})>"


def init_database(app):
    """
    Initializes the database connection for the Flask application.

    This function configures SQLAlchemy to use the provided Flask app
    and sets up the connection to the SQLite database. It also ensures
    that the necessary database tables are created if they do not exist.
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

    with app.app_context():
        db.create_all()
    print("Database initialized and tables created.")