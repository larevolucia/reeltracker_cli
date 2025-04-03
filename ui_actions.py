"""
User prompts, rating input, search input, etc.
"""
from title import Title
from tmdb import fetch_tmdb_results, TMDB_API_KEY
from menus import handle_list_menu
from utils import (
    display_title_entries,
    prepare_title_objects_from_tmdb
    )
from sheets import (
    save_item_to_list,
    check_for_duplicate,
    update_item_in_list,
    get_titles_by_watch_status,
    delete_item_in_list
    )
from user_input import (
    get_user_search_input,
    get_watch_status,
    get_title_rating,
    select_item_from_results
)


def handle_search(mode, google_sheet):
    """Handles user interaction with search functionality

    Args:
        google_sheet (gspread.Spreadsheet): Initialized google sheets
    """
    while True:
        print('\nStarting a new search...')
        # 1. Prompt user to enter a search query
        search_query = get_user_search_input()
        print(f'\n🔎 Searching for {search_query}...')
        # 2. Use the query to fetch API results
        search_results = fetch_tmdb_results(search_query, TMDB_API_KEY)
        # 3. Format TMDB titles
        results_title_objects = prepare_title_objects_from_tmdb(search_results)
        if not results_title_objects:
            print("\n❌  No results found. Try another search.")
            continue
        displayed_titles = display_title_entries(results_title_objects, 'search')
        # 4. Select result, back to main menu or new search
        results_selected_title = select_item_from_results(displayed_titles, mode)
        if results_selected_title == 'main':
            print("\nReturning to main menu...")
            break # Go back to main menu
        if results_selected_title is None:
            continue # Go back to search (1)
        # 5. Valid item (int) is selected
        print(f"\n📥 You've selected {results_selected_title.title}"
              f"({results_selected_title.release_date})")
        # 6. Check for item duplicate before saving
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
        selected_title.user_data.watched = False
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
        print(f"\n❌  No {list_type} title found.")
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
        handle_delete(selected_title, google_sheet)

def handle_toggle_watched(title, google_sheet):
    """
    Toggle watch flag of selected object

    Args:
        title (obj): selected title
        google_sheet (gspread.Spreadsheet): Initialized Google Sheet
    """
    # Toggle watched flag
    title.toggle_watched()
    if title.user_data.watched:
    # get rating if watched True
        print(f'\n🔄 Marking {title.title} as watched...')
        updated_title = get_title_rating(title)
    else:
        updated_title = title
        print(f'\n🔄 Moving {title.title} to your watchlist...')
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

def handle_delete(title, google_sheet):
    """
    Triggers deletion and messages user of success

    Args:
        title (obj): Seletect title
        google_sheet (gspread.Spreadsheet): Initialized Google Sheet
    """
    is_deleted = delete_item_in_list(google_sheet, title)
    if is_deleted:
        print(f'\n✅ {title.title} successfully removed from your list.')
