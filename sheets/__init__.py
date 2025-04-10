"""
Exposes sheet-related functions and constants for external use.

Includes CRUD utilities and sheet initialization helpers.
"""

from .query import (
    has_watched,
    has_watchlist,
    has_items,
    find_existing_row_info,
    get_titles_by_watch_status,
    check_for_duplicate
)
from .crud import (
    delete_item_in_list,
    update_item_in_list,
    save_item_to_list
)
from .auth import (
    initialize_google_sheets,
    GOOGLE_SHEETS_SCOPE,
    CREDS
    )
from .utils import build_title_objects_from_sheet
