"""
Handles different recommendation scenarios based on user activity.

Each handler manages a unique user state: no data, no watched items, no
watchlist, or full history.
"""
from tmdb.tmdb import (
    TMDB_API_KEY,
    fetch_trending_titles,
    fetch_title_base_recommendation
    )
from tmdb.utils import (
    prepare_title_objects_from_tmdb
)
from sheets.sheets import (
    get_titles_by_watch_status
    )
from sheets.utils import build_title_objects_from_sheet
from utils.utils import sort_items_by_popularity
from ui.display import display_title_entries
from .display import display_and_select_title
from .utils import (
    get_top_title_by_preferred_genre,
    get_personalized_recommendations
    )


def handle_no_items(google_sheet, mode):
    """
    Handle case when the user has no titles in their list

    Fetches trending titles from TMDB, prepares them for display, and lets
    the user select one to explore or add to their list

    Args:
        google_sheet: Google Sheet object to read/write user data
        mode (str): Current interaction mode (e.g. 'search', 'recommendations')

    Returns:
        None
    """
    print("\nYour list is looking a little empty.")
    print("Check out what's trending and find something that sparks your interest!")
    trending_results = fetch_trending_titles(TMDB_API_KEY)
    if not trending_results:
        print("\n⚠️  Unable to fetch trending titles. Please try again later.")
        return
    trending_title_objects = prepare_title_objects_from_tmdb(trending_results)
    display_and_select_title(trending_title_objects, mode, google_sheet)

def handle_no_watched_items(google_sheet):
    """
    Handle case when user has a watchlist but hasn't watched anything

    Retrieves titles from the user's watchlist, sorts them by popularity,
    and displays the top recommendations to get started

    Args:
        google_sheet: Google Sheet object to read user watchlist data

    Returns:
        None
    """
    print("\nYou haven't watched anything yet, but your watchlist has some great options.")
    print("\nHere are the most popular ones to get you started.")
    watchlist_titles = get_titles_by_watch_status(google_sheet, False)
    if not watchlist_titles:
        print("\n⚠️  Your watchlist is empty.")
        return
    title_objects = build_title_objects_from_sheet(watchlist_titles)
    sorted_titles = sort_items_by_popularity(title_objects)
    display_title_entries(sorted_titles, 'recommendation', 6)

def handle_no_watchlist_items(google_sheet, mode):
    """
    Handle case when the user has watched titles but no watchlist

    Picks a top title the user liked, fetches similar ones from TMDB,
    and displays them for selection

    Args:
        google_sheet: Google Sheet object to read watched titles
        mode (str): Current interaction mode (e.g. 'search', 'recommendations').

    Returns:
        None
    """
    print("\nYou haven't got any titles on your watchlist yet!")
    watched_titles = get_titles_by_watch_status(google_sheet, True)
    if not watched_titles:
        print("\n⚠️  Your viewing history is empty.")
        return
    title_objects = build_title_objects_from_sheet(watched_titles)
    top_title = get_top_title_by_preferred_genre(title_objects)
    if not top_title or not hasattr(top_title, "metadata"):
        print("\n⚠️  Couldn't determine a favorite title to base recommendations on.")
        return
    print(f"\nYou've recently liked {top_title.metadata.title}. "
          "Here are some titles you might also like...")

    recommended_titles = fetch_title_base_recommendation(
        top_title.metadata.media_type,
        top_title.metadata.id,
        TMDB_API_KEY
        )
    if not recommended_titles:
        print("\n⚠️  No similar titles found.")
        return
    recommended_titles_object = prepare_title_objects_from_tmdb(recommended_titles)
    display_and_select_title(recommended_titles_object, mode, google_sheet)

def handle_watched_and_watchlist(google_sheet, mode):
    """
    Handle recommendation flow when user has both watched and watchlist items

    Uses watched history and watchlist to generate personalized
    recommendations, then displays them

    Args:
        google_sheet: Google Sheet object to access user data
        mode (str): Current interaction mode (e.g. 'search', 'recommendations')

    Returns:
        None
    """
    print("\n🔄 Analyzing viewing history...")
    watched_titles = get_titles_by_watch_status(google_sheet, True)
    if not watched_titles:
        print("\n⚠️  Your viewing history is empty.")
        return
    watched_titles_objects = build_title_objects_from_sheet(watched_titles)
    watchlist_titles = get_titles_by_watch_status(google_sheet,False)
    if not watchlist_titles:
        print("\n⚠️  Your watchlist is empty.")
        return
    watchlist_titles_objects = build_title_objects_from_sheet(watchlist_titles)
    recommendation_list = get_personalized_recommendations(
        watched_titles_objects,
        watchlist_titles_objects
        )
    display_title_entries(recommendation_list, mode, 6)
