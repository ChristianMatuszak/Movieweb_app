import pytest
import requests
from unittest.mock import patch
from omdb_api import fetch_movie_data


@pytest.fixture
def mock_valid_response():
    return {
        "Response": "True",
        "Title": "Inception",
        "Year": "2010",
        "imdbRating": "8.8",
        "Poster": "someposterurl"
    }


@pytest.fixture
def mock_invalid_response():
    return {
        "Response": "False",
        "Error": "Movie not found!"
    }


def test_fetch_movie_data_success(mock_valid_response):
    """
    Tests the successful retrieval of movie data from the OMDb API.

    This test simulates a valid API response for a movie (Inception) and
    verifies that the `fetch_movie_data` function returns a dictionary
    containing the movie's title, year, rating, and poster. It ensures
    that the function processes a valid response correctly and does not
    return `None`.

    Args:
        mock_valid_response (dict): Mocked response simulating a successful
                                     movie data retrieval from the OMDb API.

    Asserts:
        The result of `fetch_movie_data` is not `None` and contains the expected
        movie data (title, year, rating, poster).
    """
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_valid_response

        result = fetch_movie_data("Inception")

        assert result is not None
        assert result["title"] == "Inception"
        assert result["year"] == 2010
        assert result["rating"] == 8.8
        assert result["poster"] == "someposterurl"


def test_fetch_movie_data_movie_not_found(mock_invalid_response):
    """
    Tests the case when the movie is not found in the OMDb API.

    This test simulates a response from the OMDb API indicating that the
    movie is not found. The test verifies that the `fetch_movie_data` function
    correctly handles this scenario by returning `None` and printing an error
    message stating that the movie was not found.

    Asserts:
        The error message "Movie not found" is printed and the result is `None`.
    """
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_invalid_response

        result = fetch_movie_data("NonExistentMovie")

        assert result is None


def test_fetch_movie_data_api_error():
    """
    Tests the scenario when there is an error in the API request.

    This test simulates a failure in the API request (such as a network issue)
    by raising a `requests.exceptions.RequestException`. It verifies that the
    `fetch_movie_data` function handles the exception correctly by printing an
    error message and returning `None`.

    Asserts:
        The error message "Request error" is printed and the result is `None`.
    """
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("API request error")

        result = fetch_movie_data("Inception")

        assert result is None
