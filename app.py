import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from data.database import init_database, User, db, Movie
from omdb_api import fetch_movie_data

app = Flask(__name__)

init_database(app)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def home():
    """
    Route to render the homepage of the application.

    This is the landing page users will see when they visit the root URL.

    Returns:
        str: Rendered HTML template of the home page (home.html).
    """
    return render_template('home.html')

@app.route("/users")
def list_users():
    """
    Route to list all users in the database.

    It queries the database for all users and displays them on the users page.
    If an error occurs during database interaction, an error message is shown.

    Returns:
        str: Rendered HTML template displaying all users (users.html).
    """
    try:
        users = User.query.all()
        return render_template('users.html', users=users)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        flash("An error occurred while loading users.", "danger")
        return redirect(url_for("home"))

@app.route("/users/<int:user_id>")
def user_movies(user_id):
    """
    Route to display the movies of a specific user.

    This route takes a user ID, retrieves the corresponding user from the database,
    and renders the user's movie collection page. If an error occurs, it redirects back to the user list.

    Args:
        user_id (int): The ID of the user whose movies are to be displayed.

    Returns:
        str: Rendered HTML template displaying the user's movies (user_movies.html).
    """
    try:
        user = User.query.get_or_404(user_id)
        return render_template("user_movies.html", user=user)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        flash("An error occurred while loading user's movies.", "danger")
        return redirect(url_for("list_users"))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Route to add a new user.

    If the request method is POST, the function attempts to add a new user to the database with the given name.
    It redirects to the user list page after successful addition, or shows an error message if something goes wrong.

    Returns:
        str: Rendered HTML template to add a user (add_user.html).
    """
    if request.method == 'POST':
        user_name = request.form['name']
        try:
            new_user = User(name=user_name)
            db.session.add(new_user)
            db.session.commit()
            flash("User added successfully.", "success")
            return redirect(url_for('list_users'))
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error(f"Error adding user: {e}")
            flash("Failed to add user.", "danger")

    return render_template('add_user.html')


@app.route("/add_movie/<int:user_id>", methods=["GET", "POST"])
def add_movie(user_id):
    """
    Route to add a new movie to a user's collection.

    If the request method is POST, it attempts to search for a movie title using the OMDb API.
    If a valid movie is found, it is added to the user's movie collection.
    Returns an error message if the movie cannot be found or if an API error occurs.

    Args:
        user_id (int): The ID of the user who the movie will be added to.

    Returns:
        str: Rendered HTML template to add a movie (add_movie.html).
    """
    user = User.query.get_or_404(user_id)
    error = None

    if request.method == "POST":
        title = request.form.get("title")

        if not title:
            error = "Please enter a movie title."
        else:
            try:
                movie_data = fetch_movie_data(title)
                if movie_data:
                    new_movie = Movie(
                        name=movie_data['title'],
                        director="Unknown",
                        year=movie_data['year'],
                        rating=movie_data['rating'],
                        poster=movie_data['poster'],
                        user_id=user.id
                    )
                    db.session.add(new_movie)
                    db.session.commit()
                    flash("Movie added successfully.", "success")
                    return redirect(url_for('user_movies', user_id=user.id))
                else:
                    error = f"Movie '{title}' not found in OMDb."
            except Exception as e:
                app.logger.error(f"OMDb API error: {e}")
                error = "An error occurred while searching for the movie."

    return render_template("add_movie.html", user=user, error=error)



@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """
    Route to update a movie's details for a specific user.

    This route takes the movie ID and allows the user to edit the movie's title, director, year, and rating.
    The changes are committed to the database upon form submission. If an error occurs, an error message is shown.

    Args:
        user_id (int): The ID of the user who owns the movie.
        movie_id (int): The ID of the movie to be updated.

    Returns:
        str: Rendered HTML template to update the movie (update_movie.html).
    """
    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":
        try:
            movie.name = request.form["name"]
            movie.director = request.form["director"]
            movie.year = int(request.form["year"])
            movie.rating = float(request.form["rating"])
            db.session.commit()
            flash("Movie updated successfully.", "success")
            return redirect(url_for("user_movies", user_id=user_id))
        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            app.logger.error(f"Error updating movie: {e}")
            flash("Failed to update movie.", "danger")

    return render_template("update_movie.html", movie=movie, user_id=user_id)

@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>", methods=["POST"])
def delete_movie(user_id, movie_id):
    """
    Route to delete a movie from a user's collection.

    This route deletes the specified movie from the user's collection in the database.
    If the deletion is successful, a success message is displayed; otherwise, an error message is shown.

    Args:
        user_id (int): The ID of the user who owns the movie.
        movie_id (int): The ID of the movie to be deleted.

    Returns:
        Response: Redirects to the user's movie collection page after deletion.
    """
    movie = Movie.query.get_or_404(movie_id)
    try:
        db.session.delete(movie)
        db.session.commit()
        flash("Movie deleted successfully.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Error deleting movie: {e}")
        flash("Failed to delete movie.", "danger")

    return redirect(url_for("user_movies", user_id=user_id))


@app.errorhandler(404)
def not_found_error(error):
    """
    Error handler for 404 Not Found errors.

    This handler is triggered when a requested page cannot be found. It renders a custom 404 error page.

    Args:
        error (Exception): The error that triggered this handler.

    Returns:
        tuple: The rendered 404 error page with a status code of 404.
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Error handler for 500 Internal Server errors.

    This handler is triggered when an unexpected server error occurs. It rolls back any active database session and renders a custom 500 error page.

    Args:
        error (Exception): The error that triggered this handler.

    Returns:
        tuple: The rendered 500 error page with a status code of 500.
    """
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
