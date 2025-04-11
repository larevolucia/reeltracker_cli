"""
Controls the logic for fetchign and displayin trending title recommendations


"""
from tmdb.tmdb import fetch_trending_titles, TMDB_API_KEY
from models.title import (
    prepare_title_objects_from_tmdb
)
from .display import display_and_select_title

def show_trending_titles(mode, google_sheet):
    """
    Fetch trending titles from TMDB and allow the user to explore or save one.

    Args:
        google_sheet: Google Sheet object
        mode (str): 'search' or 'recommendation' depending on where it's called from

    Returns:
        None
    """
    trending_results = fetch_trending_titles(TMDB_API_KEY)
    if not trending_results:
        print("\n⚠️  Unable to fetch trending titles. Please try again later.")
        return
    trending_title_objects = prepare_title_objects_from_tmdb(trending_results)
    display_and_select_title(trending_title_objects, mode, google_sheet)
