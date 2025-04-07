"""
Recommendation logic
"""
from tmdb import TMDB_API_KEY, fetch_trending_titles
from sheets import (
    has_items,
    has_watched,
    has_watchlist,
    get_titles_by_watch_status
    )
from ui_actions import (
    prepare_title_objects_from_tmdb,
    select_item_from_results,
    handle_title_selection,
    display_title_entries
    )
from title import Title
from utils import (
    sort_items_by_popularity
    )

def handle_recommendations(mode, google_sheet):
    """
    Recommends titles to the user based on the state of their list
        - If no titles at all: show trending
        - If no watchlist: show similar to watched items
        - If no watched items: show watchlist by popularity
        - If watched and watchlist: selects from watched item

    Args:
        google_sheet (_type_): _description_
    """
    items = has_items(google_sheet)
    watched_items = has_watched(google_sheet)
    watchlist_items = has_watchlist(google_sheet)
    if not items:
        trending_results = fetch_trending_titles(TMDB_API_KEY)
        trending_title_objects = prepare_title_objects_from_tmdb(trending_results)
        print("\nYour list is looking a little empty.")
        print("Check out what’s trending and find something that sparks your interest!")
        displayed_titles = display_title_entries(trending_title_objects, 'trending', 6)
        results_selected_title = select_item_from_results(displayed_titles, mode)
        if results_selected_title == 'main' or results_selected_title is None:
            print('\nReturning to main menu...')
        else:
            print(f"\n📥 You've selected {results_selected_title.title}"
                  f"({results_selected_title.release_date})")
        handle_title_selection(results_selected_title, google_sheet)
    elif not watched_items:
        print("\nYou haven’t watched anything yet, but your watchlist has some great options.")
        print("\nHere are the most popular ones to get you started.")
        watchlist_titles = get_titles_by_watch_status(google_sheet, False)
        title_objects = [Title.from_sheet_row(row) for row in watchlist_titles]
        sorted_titles = sort_items_by_popularity(title_objects)
        displayed_titles = display_title_entries(sorted_titles, 'recommendation', 6)
    # elif not watchlist_items:
    #     print("You have no watchlist items, but you have some watched items!")
    # else:
    #     print("You have watched items and watchlist items")
