"""
Handles Google sheets CRUD 
"""
import gspread
from google.oauth2.service_account import Credentials
# from rich import print_json

# Google API authentication
GOOGLE_SHEETS_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

def initialize_google_sheets(sheet_name='reeltracker_cli', credentials_file='creds.json'):
    """
    Initializes and returns a Google Sheets

    Args:
        sheet_name (str): Name of the Google Sheet to open
        credentials_file (str): Path to credentials JSON file

    Returns:
        gspread.Spreadsheet: An authorized Google Sheets object
    """
    creds = Credentials.from_service_account_file(credentials_file)
    scoped_creds = creds.with_scopes(GOOGLE_SHEETS_SCOPE)
    client = gspread.authorize(scoped_creds)
    return client.open(sheet_name)

def save_item_to_list(sheet, title_obj):
    """Saves an item to worksheet 

    Args:
        sheet (gspread.Spreadsheet): Google sheet name 
        title_obj (Title): The Title object to save
    """
    # print_json(data=title_obj.to_sheet_row())

    try:
        worksheet = sheet.worksheet('My_List')
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title='My_List', rows='100', cols='20')
        # Create headers if worksheet is new
        headers = [
            "id", "title", "media_type", "release_date",
            "genres", "weighted_popularity", "overview",
            "is_watched", "added_date", "watched_date", "rating"
        ]
        worksheet.append_row(headers)
    # Prepare row
    worksheet.append_row(title_obj.to_sheet_row())
    print(f"\n{title_obj.title} successfully written to the sheet.")

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
                if row[id_index] == str(title_obj.id) and row[type_index] == title_obj.media_type:
                    watch_status = 'watched' if row[watched_index] == "True" else 'watchlist'
                    print(f"\n{title_obj.title} already in list, marked as {watch_status}.")
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

        filtered = [row for row in all_values
                    if str(row.get("is_watched", "")).lower() == str(watched).lower()
                    ]
        return filtered
    except gspread.exceptions.WorksheetNotFound:
        print("\nNo data found. Select 1 to search and add your first title.")
        return []

def update_item_in_list(sheet, title_obj):
    """
    Finds title in Google Sheet 
    and replace cells with updated values

    Args:
        sheet (gspread.Spreadsheet): Initialized Google Sheet
        title_obj (obj): Selected title
    """
    found, row_index, existing_row = find_existing_row_info(title_obj, sheet)
    new_row = title_obj.to_sheet_row()
    worksheet = sheet.worksheet('My_List')
    headers = worksheet.row_values(1)
    timestamp_fields = ["added_date"]

    if found:
        existing_row = existing_row + [""] * (len(new_row) - len(existing_row))
        updates = []
        for col_index, header in enumerate(headers):
            if header in timestamp_fields:
                continue
            old_value = existing_row[col_index]
            new_value = new_row[col_index]
            if old_value != new_value:
                cell = gspread.utils.rowcol_to_a1(row_index, col_index + 1)
                updates.append((cell, new_value))
        if not updates:
            print(f'\nNo updates found for {title_obj.title}.')
            return 'skipped'

        print(f'\nUpdating {title_obj.title}...')
        for cell, value in updates:
            worksheet.update(cell, [[value]])

        print(f"\n{title_obj.title} updated successfully ({len(updates)} changes).")
        return 'updated'

    # If not found, just add it
    save_item_to_list(sheet, title_obj)
    return 'added'

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
    print(f"\nLooking for {title_obj.title} in sheet...")
    try:
        worksheet = sheet.worksheet('My_List')
        all_values = worksheet.get_all_values()
        # Get headers and indexes
        headers = all_values[0]
        id_index = headers.index("id")
        type_index = headers.index("media_type")

        for i, row in enumerate(all_values[1:], start=2):
            if len(row) > max(id_index, type_index):
                if row[id_index] == str(title_obj.id) and row[type_index] == title_obj.media_type:
                    return True, i, row
        print(f"\n{title_obj.title} not found in sheet.")
        return False, None, None
    except gspread.exceptions.WorksheetNotFound:
        return False, None, None

def delete_item_in_list(sheet, title_obj):
    """
    Finds existing row and delete it from sheet

    Args:
        sheet (gspread.Spreadsheet): Initialized Google Sheet
        title_obj (obj): Selected Title object
    """
    found, row_index, _ = find_existing_row_info(title_obj, sheet)
    worksheet = sheet.worksheet('My_List')
    if found:
        worksheet.delete_rows(row_index)
        return True
    return False
