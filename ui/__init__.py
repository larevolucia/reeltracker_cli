"""
Initializes the UI layer by exposing menus, input handlers, and display logic.

Combines user interaction features from various modules for easy import.
"""

from .display import display_title_entries
from .handlers import (
    handle_search,
    handle_title_selection,
    handle_watchlist_or_watched,
    handle_toggle_watched,
    handle_change_rating,
    handle_delete
)
from .user_input import (
    get_user_search_input,
    get_watch_status,
    get_title_rating,
    select_item_from_results,
    confirm_action
)
from .menus import (
    display_main_menu,
    display_menu,
    handle_list_menu,
    handle_action_with_index,
    get_menu_choice
)

__all__ = [
    "display_title_entries",
    "handle_search",
    "handle_title_selection",
    "handle_watchlist_or_watched",
    "handle_toggle_watched",
    "handle_change_rating",
    "handle_delete",
    "get_user_search_input",
    "get_watch_status",
    "get_title_rating",
    "select_item_from_results",
    "confirm_action",
    "display_main_menu",
    "display_menu",
    "handle_list_menu",
    "handle_action_with_index",
    "get_menu_choice",
]
