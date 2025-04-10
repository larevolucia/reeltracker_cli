"""
Initializes the recommendation module
"""
from .recommendations import handle_recommendations
from .handlers import (
    handle_no_items,
    handle_no_watched_items,
    handle_no_watchlist_items,
    handle_watched_and_watchlist
)
