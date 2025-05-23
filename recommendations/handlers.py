"""
Handles different recommendation scenarios based on user activity.

Each handler manages a unique user state: no data, no watched items, no
watchlist, or full history.
"""
from tmdb.tmdb_api import (
    TMDB_API_KEY,
    fetch_title_base_recommendation
    )
from models.title import (
    prepare_title_objects_from_tmdb
)
from sheets.query import (
    get_titles_by_watch_status
    )
from sheets.utils import build_title_objects_from_sheet
from utils.utils import sort_items_by_popularity
from ui.display import display_title_entries
from .smart_recs import (
    get_top_title_by_preferred_genre,
    get_personalized_recommendations
)
from .trending import show_trending_titles
from .display import display_and_select_title


def handle_no_items(google_sheet):
    """
    Handle case when the user has no titles in their list

    Fetches trending titles from TMDB, prepares them for display, and lets
    the user select one to explore or add to their list

    Args:
        google_sheet: Google Sheet object to read/write user data

    Returns:
        None
    """
    print("\nYour list is looking a little empty.")
    print(
        "Find something that sparks your interest on the trending list!"
        )
    show_trending_titles("trending", google_sheet)


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
    print(
        "\nYou haven't watched anything yet, "
        "but your watchlist has some great options."
        )
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
        mode (str): 'search', 'recommendations'

    Returns:
        None
    """
    print("\nYou haven't got any titles on your watchlist yet!")
    print("\n🔄  Analyzing viewing history...")
    watched_titles = get_titles_by_watch_status(google_sheet, True)
    if not watched_titles:
        print("\n⚠️  Your viewing history is empty.")
        return
    title_objects = build_title_objects_from_sheet(watched_titles)
    top_title = get_top_title_by_preferred_genre(title_objects)
    if not top_title or not hasattr(top_title, "metadata"):
        print(
            "\n⚠️  No favorite title found for recommendations."
            )
        print("\nMaybe you need some inspiration...")
        show_trending_titles('trending', google_sheet)
        return
    print(f"\nYou've recently liked '{top_title.metadata.title}'. "
          "Here are some titles you might also like...")

    recommended_titles = fetch_title_base_recommendation(
        top_title.metadata.media_type,
        top_title.metadata.id,
        TMDB_API_KEY
        )
    if not recommended_titles:
        print("\n⚠️  No similar titles found.")
        return
    recommended_titles_object = prepare_title_objects_from_tmdb(
        recommended_titles
        )
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
    print("\n🔄  Analyzing viewing history...")
    watched_titles = get_titles_by_watch_status(google_sheet, True)
    if not watched_titles:
        print("\n⚠️  Your viewing history is empty.")
        return
    watched_titles_objects = build_title_objects_from_sheet(watched_titles)
    watchlist_titles = get_titles_by_watch_status(google_sheet, False)
    if not watchlist_titles:
        print("\n⚠️  Your watchlist is empty.")
        return
    watchlist_titles_objects = build_title_objects_from_sheet(watchlist_titles)
    recommendation_list = get_personalized_recommendations(
        watched_titles_objects,
        watchlist_titles_objects,
        google_sheet
        )
    if recommendation_list:
        display_title_entries(recommendation_list, mode, 6)
