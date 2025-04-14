"""
Handles communication with the TMDb API for search and recommendations.

Provides functions for fetching titles, trending content, and genre data.
"""

import os
from dotenv import load_dotenv
import requests

# Constants
DEFAULT_LANGUAGE ='en-US'

# Load environment variables from .env file
load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_URL = os.getenv('TMDB_URL')

if TMDB_API_KEY is None:
    raise EnvironmentError("TMDB_API_KEY not found! Check your .env file.")

# --- Fetching title lists ---
def fetch_tmdb_results(search_key, api_key=TMDB_API_KEY, page=1, language=DEFAULT_LANGUAGE):
    """
    Fetches a list of titles from TMDB based on user's query

    Args:
        search_key (str): User search query
        api_key (str): TMDb API authentication key
        page(int): Page number of results (default 1)
        language(str): language code for results (default en-US)
    Returns:
        data (list): A list of dictionaries with results data
                    Or an empty list if the request fails
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
    except requests.RequestException:
        print("\n⚠️  Could not connect to TMDb. Please try again later.")
        return []

def fetch_trending_titles(api_key=TMDB_API_KEY, page=1, language=DEFAULT_LANGUAGE):
    """
    Fetches a list of  popular movies from TMDb API 
    
    Args:
        api_key (str): authentication API key. Defaults to TMDB_API_KEY
        page (int, optional): number of response pages. Defaults to 1
        language (str, optional): response language. Defaults to DEFAULT_LANGUAGE
        
    Returns:
        data (list): A list of dictionaries with results data
              Or an empty list if the request fails
    """
    url = f'{TMDB_URL}/trending/all/week'
    params = {
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
    except requests.RequestException:
        print("\n⚠️  Could not connect to TMDb. Please try again later.")
        return []

def fetch_title_base_recommendation(
    media_type,
    title_id,
    api_key=TMDB_API_KEY,
    page=1,
    language=DEFAULT_LANGUAGE
    ):
    """
    Fetches title-based recommendations from TMDB
    
    Args:
        api_key (str): authentication API key. Defaults to TMDB_API_KEY
        page (int, optional): number of response pages. Defaults to 1
        language (str, optional): response language. Defaults to DEFAULT_LANGUAGE
        
    Returns:
        data (list): A list of dictionaries with results data
              Or an empty list if the request fails
    """
    url = f'{TMDB_URL}/{media_type}/{title_id}/recommendations'
    params = {
        'api_key': api_key,
        'language': language,
        'page': page,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.RequestException:
        print("\n⚠️  Could not connect to TMDb. Please try again later.")
        return []

# def fetch_titles_by_genre(
#     media_type,
#     genres,
#     api_key=TMDB_API_KEY,
#     page=1,
#     language=DEFAULT_LANGUAGE
#     ):
#     """
#     Fetches titles that matches genre and media type on TMDB

#     Args:
#         media_type (str): identifier of media type ('movie', 'tv')
#         genres (str, optional): list of genre_ids
#         api_key (str, optional): authentication API key. Defaults to TMDB_API_KEY.
#         page (int, optional): number of response pages. Defaults to 1
#         language (str, optional): response language. Defaults to DEFAULT_LANGUAGE

#     Returns:
#         _type_: _description_
#     """

#     url = f'{TMDB_URL}/discover/{media_type}'

#     params = {
#         "api_key": api_key,
#         'language': language,
#         'page': page,
#         # 'with_genres': genres
#     }
#     try:
#         print(f"🔎 Fetching fallback titles from: {url} |"
#               f" genre_id={genres} | media_type={media_type}")

#         response = requests.get(url, params=params, timeout=10)
#         print("Full URL:", response.url)
#         response.raise_for_status()
#         data = response.json()
#         return data.get('results', [])
#     except requests.RequestException as e:
#         print(f"\n⚠️  Could not connect to TMDb: {e}")
#         return []

# --- Genre Mapping---

def get_genre_mapping(media_type, api_key):
    """
    Request genre name from API 

    Args:
        media_type (str): media_type of title
        api_key (str): TMDb API authentication key
        
    Returns:
        genre_mapping (dict): list of dictionaries with genre mapping 
    """
    url = f'{TMDB_URL}/genre/{media_type}/list'
    params = {
        'api_key': api_key,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('genres', [])
    except requests.RequestException:
        print("⚠️  Could not connect to TMDb. Please try again later.")
        return []
