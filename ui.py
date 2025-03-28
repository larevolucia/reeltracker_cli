"""
User prompts, rating input, search input, etc.
"""
from tabulate import tabulate
from title import Title
from tmdb import fetch_tmdb_results, TMDB_API_KEY
from menus import handle_list_menu
from utils import filter_results_by_media_type, sort_items_by_popularity
from sheets import (
    save_item_to_list,
    check_for_duplicate,
    update_item_in_list,
    get_titles_by_watch_status,
    delete_item_in_list
    )

def get_user_search_input(prompt="\nSearch a title to get started: "):
    """
    Prompts user input for searching a title. Ensures non-empty input
    
    Args:
        prompt (str): Prompt message presented before input
    
    Returns:
        str: User input string
    """
    while True:
        print(prompt)
        user_query = input("> ").strip()
        if user_query:
            return user_query
        print('\nSearch cannot be emtpy. Please try again.\n')

def display_title_entries(title_objects, mode, max_results=None):
    """
    Display a list of Title objects in a table format based on context.
    
    Args:
        title_objects (list): _description_
        mode (str): _description_
        max_results (int, optional): _description_. Defaults to None.
    Returns:
        (list[Title]): Title objects list slice [:max_results]
    """
    headers = {
        'search': 'Search results',
        'watchlist': 'Your watchlist',
        'watched': 'Your watched titles'
    }

    print(f"\n{headers.get(mode, 'Titles')}:\n")
    is_watched = mode == 'watched'
    col_headers = ["#", "Title", "Type", "Release"]
    if is_watched:
        col_headers.append("Rating")
    else:
        col_headers.append("Overview")
    table_data = []
    for index, title in enumerate(title_objects[:max_results], start=1):
        title_str = title.title
        if len(title_str) > 34:
            title_str = title_str[:34].rstrip() + "..."
        row = [
            index,
            title_str,
            title.media_type,
            title.release_date,
        ]
        if is_watched:
            row.append(title.rating)
        else:
            overview = title.overview
            if len(overview) > 80:
                overview = overview[:80].rstrip() + "..."
            row.append(overview)
        table_data.append(row)
    print(tabulate(
        table_data,
        headers=col_headers,
        tablefmt="rounded_grid",
        maxcolwidths=[None]*len(col_headers)
        ))
    return title_objects[:max_results]

def select_item_from_results(title_list):
    """
    Allows user to select an item from previously displayed results
    
    Args:
        title_list (list[Title]): List of Title objects
    Returns:
        Title object: selected item from list
    """
    while True:
        print(
            f"\nSelect an item (1-{len(title_list)}) to save it, "
            f"type 'n' for a new search or 'm' to return to main menu: "
        )
        command = input("> ").strip().lower()

        if command == 'n':
            return None  # New search

        if command == 'm':
            return 'main'  # Go back to main menu
        try:
            selection = int(command)
            if not 1 <= selection <= len(title_list):
                raise ValueError(
                    f'Number out of range. You must choose between 1 and '
                    f'{len(title_list)}'
                )

            chosen_item = title_list[selection - 1]

            return chosen_item

        except ValueError as e:
            print(f"\nInvalid input: {e}. Please enter a number, 'm' or 'n'.")

def get_watch_status(title_obj):
    """
    Promps user to inform if item has already been watched
    and updates object using toggle_watched method
    
    Args:
        title_obj (Title): The Title object to save
    Returns:
        bool: True (watched), False (not watched)
    """
    while True:
        print(f'\nHave you already watched {title_obj.title}? (y/n):')
        command = input("> ").strip().lower()
        if command == 'y':
            title_obj.toggle_watched()
            print(f'\nMarking {title_obj.title} as watched...')
            return True
        if command == 'n':
            print(f'\nMarking {title_obj.title} as not watched...')
            return False
        print("\nInvalid input. Please type 'y' for yes or 'n' for no.")

def get_title_rating(title_obj):
    """
    Prompts user to provide movie rating 1-10
    updates object using set_rating method
    Args:
        title_obj(Title): The Title object to save
    """
    while True:
        print(
            f'\nHow would you rate {title_obj.title}? '
            f'Select a number from 1-10: ')
        command = input("> ").strip()
        if not command.isdigit():
            print("\nInvalid input: Please enter a whole number.")
            continue

        rating = int(command)
        try:
            title_obj.set_rating(rating)
            print(f"\nSaving {title_obj.title} rating...")
            return title_obj
        except ValueError as e:
            print(f"\nInvalid input: {e}")

def handle_search(google_sheet):
    """Handles user interaction with search functionality

    Args:
        google_sheet (gspread.Spreadsheet): Initialized google sheets
    """
    while True:
        print('\nStarting a new search...')
        # 1. Prompt user to enter a search query
        search_query = get_user_search_input()
        print(f'\nSearching for {search_query}...')
        # 2. Use the query to fetch API results
        search_results = fetch_tmdb_results(search_query, TMDB_API_KEY)
        # 3. Filter out non-movie/TV results
        filtered_results = filter_results_by_media_type(search_results)
        # 4. Handle case where no valid results are found
        if not filtered_results:
            print("\nNo results found. Try another search.")
            continue # Go back to search (1)
        # 5. Sort results by custom weighted popularity
        sorted_results = sort_items_by_popularity(filtered_results)
        # 6. Display top results as Title objects
        results_title_objects = [Title(result) for result in sorted_results]
        displayed_titles = display_title_entries(results_title_objects, 'search')
        # 7. Select result, back to main menu or new search
        results_selected_title = select_item_from_results(displayed_titles)
        if results_selected_title == 'main':
            print("\nReturning to main menu...")
            break # Go back to main menu
        if results_selected_title is None:
            continue # Go back to search (1)
        # 8. Valid item (int) is selected
        print(f"\nYou've selected {results_selected_title.title}"
              f"({results_selected_title.release_date})")
        # 9. Check for item duplicate before saving
        handle_title_selection(results_selected_title, google_sheet)
        break

def handle_title_selection(selected_title, google_sheet):
    """
    Check for duplicates, verify if item is_watched,
    get rating, if applicable
    and save item to Google Sheets

    Args:
        selected_title (obj): selected Title object
        google_sheet (gspread.Spreadsheet): Initialized google sheet
    """
    is_duplicate, _ = check_for_duplicate(selected_title, google_sheet)
    if is_duplicate:
        return
    if get_watch_status(selected_title):
        get_title_rating(selected_title)
    else:
        selected_title.watched = False
    save_item_to_list(google_sheet, selected_title)

def handle_watchlist_or_watched(list_type, google_sheet):
    """
    Handle manage list action options

    Args:
        list_type (_str_): list of items to be managed (watched/watchlist)
        google_sheet (gspread.Spreadsheet) : Initialized Google Sheet
    """
    print(f'\nLoading {list_type} menu...')
    # Set watch_flag to True if choice is watched
    watched_flag = list_type == 'watched'
    # Get titles from Google Sheets
    titles_data = get_titles_by_watch_status(google_sheet, watched_flag)
    if not titles_data:
        print(f"\nNo {list_type} title found.")
        return
    # Transform list of rows into list of objects
    titles = [Title.from_sheet_row(row) for row in titles_data]
    display_title_entries(titles, list_type)
    # Unpack command and Title object
    action, index = handle_list_menu(titles, list_type)
    if action is None:
        return
    selected_title = titles[index]
    if action == 'w':
        handle_toggle_watched(selected_title, google_sheet)
    elif action == 'r':
        handle_change_rating(selected_title, google_sheet)
    elif action == 'd':
        is_deleted = delete_item_in_list(google_sheet, selected_title)
        if is_deleted:
            print(f'\nYou removed {selected_title.title} from your list.')
        else:
            print(f"\nCouldn't find {selected_title.title} in your list.")

def handle_toggle_watched(title, google_sheet):
    """
    Toggle watch flag of selected object

    Args:
        title (obj): selected title
        google_sheet (gspread.Spreadsheet): Initialized Google Sheet
    """
    # Toggle watched flag
    title.toggle_watched()
    if title.watched:
    # get rating if watched True
        updated_title = get_title_rating(title)
        title_rating = updated_title.rating
        print(f'\nMarking {title.title} as watched '
              f'and rating it {title_rating}...')
    else:
        updated_title = title
        print(f'\nMoving {title.title} to your watchlist')
    # Update item in list
    update_item_in_list(google_sheet, updated_title)

def handle_change_rating(title, google_sheet):
    """
    Replace current rating value with new value

    Args:
        title (obj): selected title object
        google_sheet (gspread.Spreadsheet): Initialized Google Sheets
    """
    # get new rating value
    updated_title = get_title_rating(title)
    # Update item in list
    update_item_in_list(google_sheet, updated_title)
