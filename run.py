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
    # if len(overview) > 150:
    #     overview = overview[:150].rstrip() + "..."
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


def select_item_from_results(formatted_entries):
    """
    Allows user to select an item from previously displayed results
    
    Arg:
        formatted_entries(list): List of formatted dictionaries
    Return:
        dictionary object: selected item from list
    """
    while True:
        user_input = input(
            f"Select an item (1-{len(formatted_entries)}) to save it "
            f"or type 'n' for a new search: "
        )

        if user_input.lower() == 'n':
            return None  # Indicates the user wants to perform a new search

        try:
            selection = int(user_input)
            if not 1 <= selection <= len(formatted_entries):
                raise ValueError(
                    f'Number out of range. You must choose between 1 and '
                    f'{len(formatted_entries)}'
                )

            chosen_item = formatted_entries[selection - 1]

            return chosen_item

        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a number or 'n'.")

def convert_dict_to_list(item: dict):
    """Converts single item dictionary into a list of headers and values
    compatible to gspread use

    Args:
        item (dict): API formatted dict item
    Returns:
        List converted to comma-separated strings
    """
    # Save dict keys into list with header entries
    headers = list(item.keys())
    # Loop through value in dictionary and save to variable
    values = []
    
    for value in item.values():
        if isinstance(value, list):
        # if value is a list
        # convert each to joined str
            values.append(', '.join(map(str, value)))
        else:
            values.append(str(value))

    return headers, values

def save_item_to_list(sheet, item, is_watched, rating="N/A"):
    """Saves an item to worksheet with current watch status

    Args:
        sheet (str): Google sheet name 
        item (dict): dictionary with title information
        isWatched (bool): watch status of the item
    """
    print_json(data=item)

    try:
        worksheet = sheet.worksheet('My_List')
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title='My_List', rows='100', cols='20')
        # Create headers if worksheet is new
        headers, _ = convert_dict_to_list(item)
        headers.extend(['Watched', 'Timestamp', 'Rating'])
        worksheet.append_row(headers)
    
    # Prepare row
    _, values = convert_dict_to_list(item)
    values.extend([is_watched, datetime.timestamp(datetime.now()), rating])
    worksheet.append_row(values)
    print("Data successfully written to the sheet.")

def get_watch_status(item):
    """
    Promps user to inform if item has already been watched
    
    Args:
        item (dict): API data of title
    Returns:
        bool: True, False
    """
    while True:
        choice = input(f'Have you already watched {item['Title']}? (y/n): ').strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        print("Invalid input. Please type 'y' for yes or 'n' for no.")

def get_title_rating(item):
    """
    Prompts user to provide movie rating 1-10

    Args:
        item (dict): API data of title
    Returns:
        int: User rating 1-10 
    """
    while True:
        user_input = input(
            f'How would you rate {item['Title']}?' 
            f'Select a number from 1-10: ').strip()
            
        if not user_input.isdigit():
            print("Invalid input: Please enter a number.")
            continue

        rating = int(user_input)
        if 1 <= rating <= 10:
            return rating

        print("Invalid input: Rating must be between 1 and 10.")

def check_for_duplicate(item, sheet):
    """_summary_

    Args:
        item (dict): API data of title
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
                if row[id_index] == str(item['id']) and row[type_index] == item['Media Type']:
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
        display_search_results(title_objects)

        # # 7. Let user select result or go back to search
        # selected_item = select_item_from_results(formatted_results)
        # # 8. If user types 'n', goes back to search (1)
        # if selected_item is None:
        #     print("\nStarting a new search\n")
        #     continue # Go back to search (1)
        # # 9. Valid item (int) is selected
        # print(
        #     f"You've selected {selected_item['Title']} "
        #     f"({selected_item['Release Date']})\n"
        #     )
        # # 10. Check if item is already in the list
        # google_sheet = initialize_google_sheets('reeltracker_cli')
        # already_in_list = check_for_duplicate(selected_item, google_sheet)
        # if already_in_list is False:
        #     # 11. Check if item is watched
        #     watched_status = get_watch_status(selected_item)
        #     # 12. If item is watched, get user rating
        #     title_rating = "N/A"
        #     if watched_status is True:
        #         title_rating = get_title_rating(selected_item)
        #     # print_json(data=selected_item)
        #     # 13. Save item
        #     save_item_to_list(google_sheet, selected_item, watched_status, title_rating)
            
        break # Exit the loop

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
