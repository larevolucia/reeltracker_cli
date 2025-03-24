"""
Handles TMDB API calls 
"""
import os
from dotenv import load_dotenv
import requests

# Constants
TMDB_URL ='https://api.themoviedb.org/3'
DEFAULT_LANGUAGE ='language=en-US'

# Load environment variables from .env file
load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

if TMDB_API_KEY is None:
    raise EnvironmentError("TMDB_API_KEY not found! Check your .env file.")

def fetch_tmdb_results(search_key, api_key, page=1, language=DEFAULT_LANGUAGE):
    """
    Fetches a list of titles from TMDB based on user's query

    Args:
        search_key (str): User search query
        api_key (str): TMDb API authentication key
        page(int): Page number of results
        language(str): language code for results
    Returns:
        list: A list of dictionaries with results data
    """
    url = f'{TMDB_URL}/search/multi'
    params = {
        'query': search_key,
        'api_key': api_key,
        'language': language,
        'page': page,
        'include_adult': False  
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return []


# Test TMDB API by fetching popular titles
# def fetch_popular_movies(api_key):
#     """
#     Fetches a list of  popular movies from TMDb API.
#     Args:
#         api_key (str): TMDb API key authenticates the request.
#     Returns:
#         list: A list of dictionaries with movie data
#               Or an empty list if the request fails
#     """
#     url = f'{TMDB_URL}/movie/popular?api_key={api_key}&{DEFAULT_LANGUAGE}&page=1'
#     response = requests.get(url,timeout=10)
#     if response.status_code == 200:
#         data = response.json()
#         return data['results']
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return []
