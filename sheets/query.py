"""
Provides lookup and filtering functions for titles in the Google Sheet.

Includes utilities to detect duplicates and retrieve rows by watch status.
"""
import gspread


# --- Content ---
def check_for_duplicate(title_obj, sheet):
    """
    Checks if the given Title object is already in the Google Sheet
    by searching combination of id and media_type match

    Args:
        title_obj (Title): The Title instance to check
        sheet (gspread.Spreadsheet): initialized google sheet
    Returns:
        (bool): True (already in list) / False (new item)
    """
    try:
        worksheet = sheet.worksheet('My_List')
        all_values = worksheet.get_all_values()

        # Get headers and indexes
        headers = all_values[0]
        id_index = headers.index("id")
        type_index = headers.index("media_type")
        watched_index = headers.index("is_watched")

        for row in all_values[1:]:
            if len(row) > max(id_index, type_index):
                if (
                    row[id_index] == str(title_obj.metadata.id) and
                    row[type_index] == title_obj.metadata.media_type
                ):
                    is_watched = row[watched_index] == "True"
                    watch_status = 'watched' if is_watched else 'watchlist'
                    print(f"\n{title_obj.metadata.title} already in list, "
                          f"marked as {watch_status}.")
                    return True, watch_status
        return False, False
    except gspread.exceptions.WorksheetNotFound:
        return False, False


def get_titles_by_watch_status(sheet, watched):
    """
    Returns a list of rows filtered by watched status

    Args:
        sheet (gspread.Spreadsheet): Google Sheet
        watched (bool): filter for watched titles or not
    Returns:
        list[dict]: filtered title rows as dict
    """
    try:
        worksheet = sheet.worksheet('My_List')
        all_values = worksheet.get_all_records()

        filtered = [
            row for row in all_values
            if str(row.get("is_watched", "")).lower() == str(watched).lower()
        ]
        return filtered
    except gspread.exceptions.WorksheetNotFound:
        print(
            "\n❌ No data found. Select 1 to search and add your first title."
            )
        return []


def find_existing_row_info(title_obj, sheet):
    """
    Finds an existing row in the sheet matching the Title by id and media_type.

    Args:
        title_obj (Title): The Title instance to search for
        sheet (gspread.Spreadsheet): The initialized Google Sheet

    Returns:
        found (bol): True/False - item found in list
        index (int): row index number
        row (list): row list data
    """
    print(f"\n🔎 Looking for {title_obj.metadata.title} in sheet...")
    try:
        worksheet = sheet.worksheet('My_List')
        all_values = worksheet.get_all_values()
        # Get headers and indexes
        headers = all_values[0]
        id_index = headers.index("id")
        type_index = headers.index("media_type")

        for i, row in enumerate(all_values[1:], start=2):
            if len(row) > max(id_index, type_index):
                if (
                    row[id_index] == str(title_obj.metadata.id) and
                    row[type_index] == title_obj.metadata.media_type
                ):
                    return True, i, row
        print(f"\n❌ {title_obj.metadata.title} not found in sheet.")
        return False, None, None
    except gspread.exceptions.WorksheetNotFound:
        print(
            "\n❌ No data found. Select 1 to search and add your first title."
            )
        return False, None, None


# --- Status ---
def has_items(sheet):
    """
    Check that sheet has items

    Args:
        sheet (gspread.Spreadsheet): Initialized Google Sheet

    Returns:
        _bool_: True for list with items
    """
    try:
        worksheet = sheet.worksheet('My_List')
        all_values = worksheet.get_all_values()
        return len(all_values) > 1  # >1 because the first row is headers
    except gspread.exceptions.WorksheetNotFound:
        print(
            "\n❌ No data found. Select 1 to search and add your first title."
            )
        return False


def has_watchlist(sheet):
    """
    Uses get_title_by_watch_status to check
    if at least 1 title in watchlist exists

    Args:
        sheet (gspread.Spreadsheet): Initialized Google Sheet

    Returns:
        bool: True / False
    """
    return len(get_titles_by_watch_status(sheet, watched=False)) > 0


def has_watched(sheet):
    """
    Uses get_title_by_watch_status to check
    if at least 1 watched exists

    Args:
        sheet (gspread.Spreadsheet): Initialized Google Sheet

    Returns:
        bool: True / False
    """
    return len(get_titles_by_watch_status(sheet, watched=True)) > 0
