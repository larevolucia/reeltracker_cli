"""
Formatting helper
"""
from models import Title

def build_title_objects_from_sheet(sheet_rows):
    return [Title.from_sheet_row(row) for row in sheet_rows]
