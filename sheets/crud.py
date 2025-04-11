"""
Provides functions for saving, updating, and deleting rows in a Google Sheet.

Handles low-level data manipulation for title objects in the user's list.
"""
import gspread
from ui.user_input import confirm_action
from .query import find_existing_row_info

def save_item_to_list(sheet, title_obj):
    """Saves an item to worksheet 

    Args:
        sheet (gspread.Spreadsheet): Google sheet name 
        title_obj (Title): The Title object to save
    """
    # print_json(data=title_obj.to_sheet_row())
    if not confirm_action(f"\nDo you want to save '{title_obj.metadata.title}'"
                          f" to your list? (y/n): "):
        print("\n❌ Action cancelled.")
        return

    try:
        worksheet = sheet.worksheet('My_List')
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title='My_List', rows='100', cols='20')
        # Create headers if worksheet is new
        headers = [
            "id", "title", "media_type", "release_date",
            "genre_ids", "genres", "weighted_popularity", "overview",
            "is_watched", "added_date", "watched_date", "rating"
        ]
        worksheet.append_row(headers)
    # Prepare row
    worksheet.append_row(title_obj.to_sheet_row())
    print(f"\n✅ {title_obj.metadata.title} successfully written to the sheet.")

def delete_item_in_list(sheet, title_obj):
    """
    Finds existing row and delete it from sheet

    Args:
        sheet (gspread.Spreadsheet): Initialized Google Sheet
        title_obj (obj): Selected Title object
    """
    if not confirm_action(f"\nAre you sure you want to delete '{title_obj.metadata.title}'"
                          f" from your list? (y/n): "):
        print("\n❌ Deletion cancelled.")
        return False
    found, row_index, _ = find_existing_row_info(title_obj, sheet)
    worksheet = sheet.worksheet('My_List')
    if found:
        worksheet.delete_rows(row_index)
        return True
    return False

def update_item_in_list(sheet, title_obj):
    """
    Finds title in Google Sheet 
    and replace cells with updated values

    Args:
        sheet (gspread.Spreadsheet): Initialized Google Sheet
        title_obj (obj): Selected title
    """
    if not confirm_action(f"\nDo you want to update '{title_obj.metadata.title}'? (y/n): "):
        print("\n❌ Update cancelled.")
        return 'skipped'
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
            print(f'\n❌  No updates found for {title_obj.metadata.title}.')
            return 'skipped'

        print(f'\n🔄 Updating {title_obj.metadata.title}...')
        for cell, value in updates:
            worksheet.update(cell, [[value]])

        print(f"\n✅ {title_obj.metadata.title} updated successfully.")
        return 'updated'

    # If not found, just add it
    save_item_to_list(sheet, title_obj)
    return 'added'
