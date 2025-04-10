"""
Recommendation handlers
"""
from tmdb.tmdb import (
    TMDB_API_KEY,
    fetch_trending_titles,
    fetch_title_base_recommendation
    )
from sheets.sheets import (
    get_titles_by_watch_status
    )
from utils.utils import sort_items_by_popularity
from ui.ui_helpers import (
    prepare_title_objects_from_tmdb
)
from ui.display import display_title_entries
from .display import display_and_select_title
from .utils import (
    build_title_objects_from_sheet,
    get_top_title_by_preferred_genre,
    get_personalized_recommendations
    )


def handle_no_items(google_sheet, mode):
    print("\nYour list is looking a little empty.")
    print("Check out what’s trending and find something that sparks your interest!")
    trending_results = fetch_trending_titles(TMDB_API_KEY)
    trending_title_objects = prepare_title_objects_from_tmdb(trending_results)
    display_and_select_title(trending_title_objects, mode, google_sheet)

def handle_no_watched_items(google_sheet):
    print("\nYou haven't watched anything yet, but your watchlist has some great options.")
    print("\nHere are the most popular ones to get you started.")
    watchlist_titles = get_titles_by_watch_status(google_sheet, False)
    title_objects = build_title_objects_from_sheet(watchlist_titles)
    sorted_titles = sort_items_by_popularity(title_objects)
    display_title_entries(sorted_titles, 'recommendation', 6)

def handle_no_watchlist_items(google_sheet, mode):
    print("\nYou haven't got any titles on your watchlist yet!")
    watched_titles = get_titles_by_watch_status(google_sheet, True)
    title_objects = build_title_objects_from_sheet(watched_titles)
    top_title = get_top_title_by_preferred_genre(title_objects)

    print(f"\nYou've recently liked {top_title.metadata.title}. "
          "Here are some titles you might also like...")

    recommended_titles = fetch_title_base_recommendation(
        top_title.metadata.media_type,
        top_title.metadata.id,
        TMDB_API_KEY
        )
    recommended_titles_object = prepare_title_objects_from_tmdb(recommended_titles)
    display_and_select_title(recommended_titles_object, mode, google_sheet)

def handle_watched_and_watchlist(google_sheet, mode):
    print("\n🔄 Analyzing viewing history...")
    watched_titles = get_titles_by_watch_status(google_sheet, True)
    watched_titles_objects = build_title_objects_from_sheet(watched_titles)
    watchlist_titles = get_titles_by_watch_status(google_sheet,False)
    watchlist_titles_objects = build_title_objects_from_sheet(watchlist_titles)
    recommendation_list = get_personalized_recommendations(
        watched_titles_objects,
        watchlist_titles_objects
        )
    display_title_entries(recommendation_list, mode, 6)
