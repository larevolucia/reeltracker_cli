"""
Initializes the UI layer by exposing menus, input handlers, and display logic.

Combines user interaction features from various modules for easy import.
"""

from .menus import (
    menus,
    display_menu,
    handle_list_menu,
    get_menu_choice,
    display_main_menu,
    handle_action_with_index
    )
from .action_handlers import (
    handle_search,
    handle_title_selection,
    handle_watchlist_or_watched,
    handle_toggle_watched,
    handle_change_rating,
    handle_delete
    )
from .user_input import (
    get_user_search_input
    )
from .display import display_title_entries
