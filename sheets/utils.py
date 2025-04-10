"""
Converts raw Google Sheet data into Title objects.

Provides a utility to format sheet rows into usable model instances.
"""

from models import Title

def build_title_objects_from_sheet(sheet_rows):
    """
    Takes raw rows from a Google Sheet and transforms each into a Title
    instance using the `from_sheet_row` class method

    Args:
        sheet_rows (list): list of rows from the Google Sheet

    Returns:
        list: list of Title objects
    """
    return [Title.from_sheet_row(row) for row in sheet_rows]
