"""
CLI Reel tracker orchestration
"""
# import json
from tabulate import tabulate
from title import Title
from tmdb import fetch_tmdb_results, TMDB_API_KEY
from sheets import (
    initialize_google_sheets,
    save_item_to_list,
    check_for_duplicate,
    update_item_in_list,
    get_titles_by_watch_status
    )
from utils import filter_results_by_media_type, sort_items_by_popularity
from menus import menus

def display_menu(menu_key):
    """
    Dynamically display menu data from menu.py based on given menu_key
    """
    menu = menus[menu_key]
    print(f"\n{menu['title']}")
    for key, label in menu["options"].items():
        print(f"{key} → {label}")

def get_menu_choice(menu_key):
    """
    Request user command and returns it
    Args:
        menu_key (str): menu identifier

    Returns:
        command value (main menu) or command
    """
    menu = menus[menu_key]
    valid = menu.get("valid_choices", menu["options"])
    while True:
        print("\nSelect an option:")
        command = input("> ").strip().lower()
        if command in valid:
            # return command value for main menu
            return valid[command] if menu_key == "main" else command
        print("Invalid option. Please try again.")

def display_main_menu():
    """
    Display the main menu and prompt the user to choose an option
    """
    display_menu("main")
    return get_menu_choice("main")

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
            return True
        if command == 'n':
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
            print("\nSaving rating...")
            return title_obj
        except ValueError as e:
            print(f"\nInvalid input: {e}")

def handle_action_with_index(command, valid_actions, list_length):
    """
    Split command and index from user input
    Validates the user's command

    Args:
        command (str): user input
        valid_action (dict): data extracted from menus.py dict
        list_lenght (int): length of options list
    Returns:
        action (str): valid selected action
        index (str): index of selected title
        error (str): error message / None if action + index is valid
    """
    try:
        action, idx_str = command.split(maxsplit=1)
    except ValueError:
        return None, None, ("Invalid command format. Try something like 'r 1' or 'd 2'.")
    if action not in valid_actions:
        return None, None, f"Invalid action '{action}'."
    if not idx_str.isdigit():
        return None, None, f"Invalid index '{idx_str}'. Use a number."
    index = int(idx_str) - 1
    if index < 0 or index >= list_length:
        return None, None, f"Index out of range. Choose between 1 and {list_length}."
    return action, index, None

def handle_list_menu(title_list, list_type):
    """
     Display the menu with CRUD actions for watched / watchlist
     Args:
        title_list (list): list with title objects from Sheets
        list_type (str): identifier of list (watched/watchlist)
     Returns:
        command (str): user action
        title (obj): selected title, or None if user exits.
    """
    valid_actions = set(menus[list_type]['options'].keys()) - {'m'}

    while True:
        display_menu(list_type)
        print("\nEnter a command like 'd 2' or 'w 1':")
        command = input("\n> ").strip().lower()

        if command == 'm':
            return None, None
        action, index, error = handle_action_with_index(command, valid_actions, len(title_list))
        if error:
            print(error)
            continue
        return action, index

def main():
    """
    Main execution function for the CLI Reel Tracker.
    """
    print("\nInitiating ReelTracker...")
    google_sheet = initialize_google_sheets('reeltracker_cli')
    while True:
        user_choice = display_main_menu()
        if user_choice == 'exit':
            print('\nGoodbye!\n')
            break
        if user_choice == 'search':
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
                is_duplicate, _ = check_for_duplicate(results_selected_title, google_sheet)
                # 10. Ask watch status
                if not is_duplicate:
                    if get_watch_status(results_selected_title):
                        get_title_rating(results_selected_title)
                    else:
                        results_selected_title.watched = False
                    save_item_to_list(google_sheet, results_selected_title)
                break
        if user_choice in ['watched', 'watchlist']:
            print(f'\nLoading {user_choice} options...')
            # Set watch_flag to True if choice is watched
            watched_flag = user_choice == 'watched'
            # Get titles from Google Sheets
            your_titles = get_titles_by_watch_status(google_sheet, watched_flag)
            if not your_titles:
                print(f"\nNo {user_choice} title found.")
                continue
            # Transform list of rows into list of objects
            your_titles_obj = [Title.from_sheet_row(row) for row in your_titles]
            display_title_entries(your_titles_obj, user_choice)
            # Unpack command and Title object
            action, index = handle_list_menu(your_titles_obj, user_choice)
            if action is None:
                continue
            selected_title_obj = your_titles_obj[index]
            if action == 'w':
                selected_title_obj.toggle_watched()
                if selected_title_obj.watched:
                    updated_title_obj = get_title_rating(selected_title_obj)
                    title_rating = updated_title_obj.rating
                    print(f'\nMarking {selected_title_obj.title} as watched '
                          f'and rating it {title_rating}')
                else:
                    updated_title_obj = selected_title_obj
                    print(f'\nMoving {selected_title_obj.title} to your watchlist')
                update_item_in_list(google_sheet, updated_title_obj)
                continue
            if action == 'r':
                updated_title_obj = get_title_rating(selected_title_obj)
                title_rating = updated_title_obj.rating
                update_item_in_list(google_sheet, updated_title_obj)
                print(f'\nYou changed {selected_title_obj.title} rating to {title_rating}')
            if action == 'd':
                print(f'\nYou removed {selected_title_obj.title} from your list.')
                continue

if __name__ == "__main__":
    main()
