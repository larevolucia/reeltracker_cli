"""
Controls the logic for generating title recommendations.

Selects the appropriate handler based on what content the user has added
or watched.
"""
from sheets.query import (
    has_items,
    has_watched,
    has_watchlist,
    )
from recommendations.handlers import (
    handle_no_items,
    handle_no_watched_items,
    handle_no_watchlist_items,
    handle_watched_and_watchlist
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
        handle_no_items(google_sheet)
    elif not watched_items:
        handle_no_watched_items(google_sheet)
    elif not watchlist_items:
        handle_no_watchlist_items(google_sheet, mode)
    else:
        handle_watched_and_watchlist(google_sheet, mode)
