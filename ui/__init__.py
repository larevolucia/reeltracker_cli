"""
UI package initializer


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
from .ui_helpers import (
    prepare_title_objects_from_tmdb,
    filter_results_by_media_type
    )
from .display import display_title_entries
