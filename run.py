"""
CLI Movie tracker
"""
import os
import json
import requests
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from rich import print_json

# Load environment variables from .env file
load_dotenv()

# Access TMDB API key
TMDB_URL ='https://api.themoviedb.org/3'
LANGUAGE ='language=en-US'
tmdb_api_key = os.getenv('TMDB_API_KEY')

if tmdb_api_key is None:
    raise EnvironmentError("TMDB_API_KEY not found! Check your .env file.")

def fetch_popular_movies(api_key):
    """
    Fetches a list of  popular movies from TMDb API.

    Args:
        api_key (str): TMDb API key authenticates the request.

    Returns:
        list: A list of dictionaries with movie data
              Or an empty list if the request fails
    """
    url = f'{TMDB_URL}/movie/popular?api_key={api_key}&{LANGUAGE}&page=1'
    response = requests.get(url,timeout=10)
    if response.status_code == 200:
        data = response.json()
        print_json(json.dumps(data))
        return data['results']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

def main():
    """
    Main function currently used for testing purpose
    """
    movies = fetch_popular_movies(tmdb_api_key)
    # print(movies)
    print("Popular Movies from TMDB:\n")
    for movie in movies:
        print(f"{movie['title']} (Released: {movie['release_date']})")

if __name__ == "__main__":
    main()

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
# try:
#     worksheet = SHEET.worksheet('TestSheet')
# # Test to create a specific sheet if not found
# except gspread.exceptions.WorksheetNotFound:
#     worksheet = SHEET.add_worksheet(title='TestSheet', rows='100', cols='20')

# # Test data to be added to sheet
# test_data = [['Title', 'Year', 'Status'],
#              ['Clueless', 1995, 'Watched'],
#              ['A real pain', 2024, 'To Watch'],
#              ['Dreams', 1900, 'Watched']]

# worksheet.append_rows(test_data)

# print("Data successfully written to the sheet.")

# # Test to read the data from sheet
# fetched_data = worksheet.get_all_values()

# print("Fetched data from the sheet:")
# for row in fetched_data:
#     print(row)
