"""
Exposes sheet-related functions and constants for external use.

Includes CRUD utilities and sheet initialization helpers.
"""

from .auth import initialize_google_sheets
from .crud import (
    get_or_create_worksheet,
    save_item_to_list,
    delete_item_in_list,
    update_item_in_list
)
from .query import (
    check_for_duplicate,
    get_titles_by_watch_status,
    find_existing_row_info,
    has_items,
    has_watched,
    has_watchlist
)
from .utils import build_title_objects_from_sheet

__all__ = [
    "initialize_google_sheets",
    "get_or_create_worksheet",
    "save_item_to_list",
    "delete_item_in_list",
    "update_item_in_list",
    "check_for_duplicate",
    "get_titles_by_watch_status",
    "find_existing_row_info",
    "has_items",
    "has_watched",
    "has_watchlist",
    "build_title_objects_from_sheet",
]
