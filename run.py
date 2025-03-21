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

# Access to Google API and worksheet
GOOGLE_SHEETS_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# CREDS = Credentials.from_service_account_file('creds.json')
# SCOPED_CREDS = CREDS.with_scopes(GOOGLE_SHEETS_SCOPE)
# GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# SHEET =  GSPREAD_CLIENT.open('reeltracker_cli')

def initialize_google_sheets(sheet_name='reeltracker_cli', credentials_file='creds.json'):
    """
    Initializes and returns a Google Sheets object.

    Args:
        sheet_name (str): Name of the Google Sheet to open.
        credentials_file (str): Path to credentials JSON file.

    Returns:
        gspread.Spreadsheet: An authorized Google Sheets object.
    """
    creds = Credentials.from_service_account_file(credentials_file)
    scoped_creds = creds.with_scopes(GOOGLE_SHEETS_SCOPE)
    client = gspread.authorize(scoped_creds)
    return client.open(sheet_name)

def get_user_search_input():
    """
    Requests user input for searching API
    """
    while True:
        search = input("Search a title to get started: ")
        if search:
            return search
        print('Search query cannot be emtpy. Please try again.\n')

def fetch_tmdb_results(search_key, api_key, page=1, language="en-US"):
    """
    Fetches a list of movies matching users search term

    Args:
        search_key (str): User search input
        api_key (str): TMDb API key authenticates the request
        page(int): limits result pages on API responses
        language(str): ISO 639 language code
    Returns:
        list: A list with movie data
    """
    url = f'{TMDB_URL}/search/multi'
    params = {
        'query': search_key,
        'api_key': api_key,
        'language': language,
        'page': page,
        'sort_by': 'vote_average.desc',
        'include_adult': False  
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return []

def filter_results_by_media_type(result_list):
    """
    Filters the list to the scoped media_types
    Args:
        result_list (list): list of dictionaries from API
    Return: Filtered list limited to 
    """
    new_result_list = [
        result for result in result_list
        if result.get("media_type") in ["movie", "tv"]
        ]
    return new_result_list

def display_search_results(result_list):
    """_summary_
    """
    for result in result_list[:5]:
        title = result.get("title") or result.get("name")
        date = result.get("release_date") or result.get("first_air_date")
        if title and date:  # Print if both information exists
            print(f"{title} - {result["media_type"]} - Release Date: {date}")
        elif title:  # Print if only title exists"
            print(f"{title} - {result["media_type"]} - No release date found.")
        elif date:  # Print if only date exists
            print(f"No title found. - {result["media_type"]} - Release Date: {date}")
        else:  # Handle case where both are missing
            print("No title or name and no date found for this result.")

def main():
    """
    Main function currently used for testing purpose
    """

    search_query = get_user_search_input()

    search_results = fetch_tmdb_results(search_query, tmdb_api_key)
    print_json(json.dumps(search_results))
    filtered_results = filter_results_by_media_type(search_results)
    display_search_results(filtered_results)


if __name__ == "__main__":
    main()

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
# Test TMDB API by fetching popular titles
# def fetch_popular_movies(api_key):
#     """
#     Fetches a list of  popular movies from TMDb API.
#     Args:
#         api_key (str): TMDb API key authenticates the request.
#     Returns:
#         list: A list of dictionaries with movie data
#               Or an empty list if the request fails
#     """
#     url = f'{TMDB_URL}/movie/popular?api_key={api_key}&{LANGUAGE}&page=1'
#     response = requests.get(url,timeout=10)
#     if response.status_code == 200:
#         data = response.json()
#         return data['results']
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return []
