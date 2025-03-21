"""
CLI Movie tracker
"""
import os
import math
import json
import requests
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from rich import print_json

# Constants
TMDB_URL ='https://api.themoviedb.org/3'
DEFAULT_LANGUAGE ='language=en-US'

# Load environment variables from .env file
load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

if TMDB_API_KEY is None:
    raise EnvironmentError("TMDB_API_KEY not found! Check your .env file.")

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

def get_user_search_input(prompt="Search a title to get started: "):
    """
    Prompts user input for searching a title. Ensures non-empty input
    
    Args:
        prompt (str): Prompt message presented before input
    
    Returns:
        str: User input string
    """
    while True:
        user_query = input(prompt)
        if user_query:
            return user_query
        print('Search query cannot be emtpy. Please try again.\n')

def fetch_tmdb_results(search_key, api_key, page=1, language=DEFAULT_LANGUAGE):
    """
    Fetches a list of titles from TMDB based on user's query

    Args:
        search_key (str): User search query
        api_key (str): TMDb API authentication key
        page(int): Page number of results
        language(str): language code for results
    Returns:
        list: A list of dictionaries with results data
    """
    url = f'{TMDB_URL}/search/multi'
    params = {
        'query': search_key,
        'api_key': api_key,
        'language': language,
        'page': page,
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

def filter_results_by_media_type(result_list, allowed_media_types=('movie', 'tv')):
    """
    Filters the TMDB results by media_type
    Args:
        result_list (list): list of dictionaries from API
        allowed_media_types(tuple): Types used for filtering
        
    Return: Filtered list limited to allowed media types
    """
    return [
        result for result in result_list
        if result.get("media_type") in allowed_media_types
        ]

def calculate_weighted_popularity(item):
    """
    Calculates weighted popularity based on popularity and vote_count

    Args:
        item (dict): TMDb item dictionary

    Returns:
        float: Weighted popularity score
    """
    popularity = item.get('popularity', 0)
    vote_count = item.get('vote_count', 0)
    # Apply logarithms weighting vote_count to prevent extreme dominance
    weighted_popularity = popularity * math.log(vote_count + 1, 10)

    return weighted_popularity

def sort_items_by_popularity(items):
    """
    Sorts a list of TMDb items by popularity

    Args:
        items (list): List of TMDb items dictionaries

    Returns:
        list: Sorted list by descending popularity
    """
    for item in items:
        weighted_popularity = calculate_weighted_popularity(item)
        item['weighted_popularity'] = weighted_popularity

    # for each x(item) in my list, sort by weighted_popularity
    return sorted(items, key=lambda x: x['weighted_popularity'], reverse=True)

def format_result_entry(result):
    """
    Formats a single result entry to display to the user and save to Google Sheet

    Args:
        result (dict): Dictionary containing individual result data

    Returns:
        dict: Reduce dictionary data and format its values
    """
    title_id = result.get("id")
    title = result.get("title") or result.get("name") or "No title available"
    date = result.get("release_date") or result.get("first_air_date") or "No release date available"
    media_type = result.get("media_type", "Unknown media type")
    # TO-DO: GENRE ID MAPPING
    genre_ids = result.get("genre_ids", [])
    weighted_popularity = round(result.get("weighted_popularity", 0), 2)
    overview = result.get("overview", "No overview available")
    if len(overview) > 150:
        overview = overview[:150].rstrip() + "..."
    # Formatted dictionary
    structured_data = {
        "id": title_id,
        "Title": title,
        "Media Type": media_type,
        "Release Date": date,
        "Genres": genre_ids,
        "Weighted Popularity": weighted_popularity,
        "Overview": overview,
    }
    return structured_data

def display_search_results(results, max_results=5):
    """
    Display formatted TMDB search results
    
    Arg:
        results (list): Filtered list of results
        max_results (int): Maximum number of results to display
    """
    print("\nSearch Results:\n" + "-"*60)
    formatted_entries = []
    # https://stackoverflow.com/questions/522563/how-to-access-the-index-value-in-a-for-loop
    for index, result in enumerate(results[:max_results], start=1):
        entry = format_result_entry(result)
        formatted_entries.append(entry)
        print(f"{index}. {entry['Title']} ({entry['Release Date']})")
        print(f"   Type: {entry['Media Type']} | Popularity: {entry['Weighted Popularity']}")
        print(f"   Overview: {entry['Overview']}\n")
    return formatted_entries

def main():
    """
    Main execution function for the CLI Reel Tracker.
    """

    search_query = get_user_search_input()

    search_results = fetch_tmdb_results(search_query, TMDB_API_KEY)
    filtered_results = filter_results_by_media_type(search_results)
    sorted_results = sort_items_by_popularity(filtered_results)
    print_json(json.dumps(sorted_results))
    formatted_results = display_search_results(sorted_results)


    # display_search_results(filtered_results)
    # google_sheet = initialize_google_sheets('reeltracker_cli')


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
#     url = f'{TMDB_URL}/movie/popular?api_key={api_key}&{DEFAULT_LANGUAGE}&page=1'
#     response = requests.get(url,timeout=10)
#     if response.status_code == 200:
#         data = response.json()
#         return data['results']
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return []
