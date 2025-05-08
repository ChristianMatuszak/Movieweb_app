# 🎬 MovieWeb App

A simple web application to manage users and their movie collections. It integrates with the OMDb API to fetch movie data and uses Flask and SQLAlchemy for the backend.

## 🚀 Features

- Add and list users
- Add, update, and delete movies for each user
- Fetch movie data automatically via OMDb API
- Error handling for missing pages or internal issues
- Styled with Tailwind CSS
- Environment configuration via `.env`

## 🛠️ Technologies Used

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [OMDb API](https://www.omdbapi.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- Python 3.11+

## 📦 Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/movieweb-app.git
   cd movieweb-app
   ```
2. **Install dependencies** 
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**
   ```bash
   SECRET_KEY=your_secret_key_here
   OMDB_API_KEY=your_omdb_api_key_here
   ```
5. **Run the application**
   ```bash
   flask run
   ```
7. **Visit in your browser**
   ```bash
   http://127.0.0.1:5000
   ```

## 🧪 Running Tests

  Run all tests with:
  ```bash
  pytest
  ```

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.
