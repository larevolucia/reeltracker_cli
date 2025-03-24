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
from title import Title
from datetime import datetime


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

def display_search_results(title_objects, max_results=5):
    """
    Display formatted TMDB search results
    
    Arg:
        results (list): Filtered list of results
        max_results (int): Maximum number of results to display
    """
    print("\nSearch Results:\n" + "-"*60)
    for index, title in enumerate(title_objects[:max_results], start=1):
        print(f"{index}. {title.title} ({title.release_date})")
        print(f"   Type: {title.media_type} | Popularity: {title.popularity}")
        print(f"   Overview: {title.overview}\n")
    return title_objects[:max_results]

def select_item_from_results(title_list):
    """
    Allows user to select an item from previously displayed results
    
    Arg:
        title_list (list[Title]): List of Title objects
    Return:
        dictionary object: selected item from list
    """
    while True:
        user_input = input(
            f"Select an item (1-{len(title_list)}) to save it "
            f"or type 'n' for a new search: "
        ).strip().lower()

        if user_input == 'n':
            return None  # Indicates the user wants to perform a new search

        try:
            selection = int(user_input)
            if not 1 <= selection <= len(title_list):
                raise ValueError(
                    f'Number out of range. You must choose between 1 and '
                    f'{len(title_list)}'
                )

            chosen_item = title_list[selection - 1]

            return chosen_item

        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a number or 'n'.")

def save_item_to_list(sheet, title_obj):
    """Saves an item to worksheet 

    Args:
        sheet (str): Google sheet name 
        title_obj (Title): The Title object to save
    """
    print_json(data=title_obj.to_dict())

    try:
        worksheet = sheet.worksheet('My_List')
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title='My_List', rows='100', cols='20')
        # Create headers if worksheet is new
        headers = [
            "id", "Title", "Media Type", "Release Date",
            "Genres", "Weighted Popularity", "Overview",
            "Watched", "Timestamp", "Rating"
        ]
        worksheet.append_row(headers)
    
    # Prepare row
    worksheet.append_row(title_obj.to_sheet_row())
    print("Title successfully written to the sheet.")

def get_watch_status(title_obj):
    """
    Promps user to inform if item has already been watched
    
    Args:
        title_obj (Title): The Title object to save
    Returns:
        bool: True, False
    """
    while True:
        choice = input(f'Have you already watched {title_obj.title}? (y/n): ').strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        print("Invalid input. Please type 'y' for yes or 'n' for no.")

def get_title_rating(title_obj):
    """
    Prompts user to provide movie rating 1-10

    Args:
        title_obj(Title): The Title object to save

    """
    while True:
        user_input = input(
            f'How would you rate {title_obj.title}? ' 
            f'Select a number from 1-10: ').strip()
            
        if not user_input.isdigit():
            print("Invalid input: Please enter a number.")
            continue

        rating = int(user_input)
        try:
            title_obj.set_rating(rating)
            return 
        except ValueError as e:
            print(f"Invalid input: {e}")

def check_for_duplicate(title_obj, sheet):
    """
    Checks if the given Title object is already in the Google Sheet.


    Args:
        title_obj (Title): The Title instance to check
        sheet (str): initialized google sheet
    """
    try:
        worksheet = sheet.worksheet('My_List')
        all_values = worksheet.get_all_values()
        # Get headers and indexes
        headers = all_values[0]
        id_index = headers.index("id")
        type_index = headers.index("Media Type")

        for row in all_values[1:]:  
            if len(row) > max(id_index, type_index):
                if row[id_index] == str(title_obj.id) and row[type_index] == title_obj.media_type:
                    print("Item already in List.")
                    return True

        return False
    except gspread.exceptions.WorksheetNotFound:
        return False

def main():
    """
    Main execution function for the CLI Reel Tracker.
    """
    while True:
        # 1. Prompt user to enter a search query
        search_query = get_user_search_input()
        # 2. Use the query to fetch API results
        search_results = fetch_tmdb_results(search_query, TMDB_API_KEY)
        # 3. Filter out non-movie/TV results
        filtered_results = filter_results_by_media_type(search_results)
        # 4. Handle case where no valid results are found
        if not filtered_results:
            print("No results found. Try another search.\n")
            continue # Go back to search (1)
        # 5. Sort results by custom weighted popularity
        sorted_results = sort_items_by_popularity(filtered_results)
        # 6. Display top results
        title_objects = [Title(result) for result in sorted_results]
        displayed_titles = display_search_results(title_objects)
        # 7. Let user select result or go back to search
        selected_item = select_item_from_results(displayed_titles)
        # 8. If user types 'n', goes back to search (1)
        if selected_item is None:
            print("\nStarting a new search\n")
            continue # Go back to search (1)
        # 9. Valid item (int) is selected
        print(f"You've selected {selected_item.title} ({selected_item.release_date})\n")
        # 10. Check if item is already in the list
        google_sheet = initialize_google_sheets('reeltracker_cli')
        if not check_for_duplicate(selected_item, google_sheet):
            if get_watch_status(selected_item):
                get_title_rating(selected_item)
                selected_item.mark_watched()
            else:
                selected_item.watched = False
            save_item_to_list(google_sheet, selected_item)
        break

if __name__ == "__main__":
    main()


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
