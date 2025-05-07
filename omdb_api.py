import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/"

def fetch_movie_data(title):
    """
    Fetches movie data from the OMDb API using the given title.

    Args:
        title (str): Title of the movie to search for.

    Returns:
        dict or None: Dictionary with movie data if found, otherwise None.
    """
    if not API_KEY:
        print("OMDb API key not found. Please check your .env file.")
        return None

    try:
        response = requests.get(BASE_URL, params={"apikey": API_KEY, "t": title})
        if response.status_code == 200:
            data = response.json()
            if data.get("Response") == "True":
                return {
                    "title": data.get("Title"),
                    "year": int(data.get("Year", 0)),
                    "rating": float(data.get("imdbRating", 0)),
                    "poster": data.get("Poster")
                }
            else:
                print(f"Movie not found: {data.get('Error')}")
        else:
            print(f"Error: Status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    return None