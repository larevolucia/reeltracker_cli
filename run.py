"""
CLI Movie tracker
"""
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET =  GSPREAD_CLIENT.open('reeltracker_cli')

# Test to find a specific sheet
try:
    worksheet = SHEET.worksheet('TestSheet')
# Test to create a specific sheet if not found
except gspread.exceptions.WorksheetNotFound:
    worksheet = SHEET.add_worksheet(title='TestSheet', rows='100', cols='20')

# Test data to be added to sheet
test_data = [['Title', 'Year', 'Status'],
             ['Clueless', 1995, 'Watched'],
             ['A real pain', 2024, 'To Watch'],
             ['Dreams', 1900, 'Watched']]

worksheet.append_rows(test_data)

print("Data successfully written to the sheet.")

# Test to read the data from sheet
fetched_data = worksheet.get_all_values()

print("🔍 Fetched data from the sheet:")
for row in fetched_data:
    print(row)
