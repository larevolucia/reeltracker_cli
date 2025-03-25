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
        sheet (str): Google sheet name 
        title_obj (Title): The Title object to save
    """
    # print_json(data=title_obj.to_dict())

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
    print("\nTitle successfully written to the sheet.")

def check_for_duplicate(title_obj, sheet):
    """
    Checks if the given Title object is already in the Google Sheet
    by searching combination of id and media_type match

    Args:
        title_obj (Title): The Title instance to check
        sheet (str): initialized google sheet
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

        for row in all_values[1:]:
            if len(row) > max(id_index, type_index):
                if row[id_index] == str(title_obj.id) and row[type_index] == title_obj.media_type:
                    print("\nItem already in List.")
                    return True

        return False
    except gspread.exceptions.WorksheetNotFound:
        return False

def get_titles_by_watch_status(sheet, watched):
    """
    Returns a list of rows filtered by watched status

    Args:
        sheet (str): Google Sheet
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
        print("\nNo data found. Select 'search' to add your first title.")
        return []
