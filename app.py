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
    return render_template('home.html')

@app.route("/users")
def list_users():
    try:
        users = User.query.all()
        return render_template('users.html', users=users)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        flash("An error occurred while loading users.", "danger")
        return redirect(url_for("home"))

@app.route("/users/<int:user_id>")
def user_movies(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return render_template("user_movies.html", user=user)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        flash("An error occurred while loading user's movies.", "danger")
        return redirect(url_for("list_users"))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
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
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
