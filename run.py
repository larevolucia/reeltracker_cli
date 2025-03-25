"""
CLI Reel tracker orchestration
"""
# import json

from title import Title
from tmdb import fetch_tmdb_results, TMDB_API_KEY
from sheets import (
    initialize_google_sheets,
    save_item_to_list,
    check_for_duplicate,
    get_titles_by_watch_status
    )
from utils import filter_results_by_media_type, sort_items_by_popularity

def display_main_menu():
    """
    Display the main menu and prompt the user to choose an option

    Returns:
        str: The user's choice ('search', 'watchlist', 'watched', or 'exit')
    """
    print("\n🎬 ReelTracker Menu\n")
    print("1. Search a new title")
    print("2. Manage watchlist titles")
    print("3. Manage watched titles")
    print("4. Exit")
    while True:
        choice = input("\nChoose an option (1-4). ").strip()
        if choice == '1':
            return 'search'
        elif choice == '2':
            return 'watchlist'
        elif choice == '3':
            return "watched"
        elif choice == '4':
            return 'exit'
        else:
            print('Invalid choice. Please select 1, 2, 3 or 4.')

def get_user_search_input(prompt="\nSearch a title to get started: "):
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
        print('\nSearch query cannot be emtpy. Please try again.\n')

def display_title_entries(title_objects, mode, max_results=None):
    """
    Display a list of Title objects with formatting base on context 
    
    Args:
        title_objects (list): list of Title objects
        max_results (int): Maximum number of results to display
        mode (str): context hint
    Returns:
        (list[Title]): Title objects list slice [:max_results]
    """
    headers = {
        'search' : 'Search results',
        'watchlist': 'Your watchlist',
        'watched': 'Your watched titles'
    }
    print(f"\n{headers.get(mode, 'Titles')}:\n" + "-"*60)
    for index, title in enumerate(title_objects[:max_results], start=1):
        print(f"\n{index}. {title.title} ({title.release_date}) - {title.media_type}")
        print(f'\nPopularity Score: {title.popularity}')
        if mode == 'watched':
            print(f'Your rating: {title.rating}')
        print(f"\nSynopsis: {title.overview}")
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
        user_input = input(
            f"\nSelect an item (1-{len(title_list)}) to save it, "
            f"type 'n' for a new search or 'm' to return to main menu: "
        ).strip().lower()

        if user_input == 'n':
            return None  # New search

        elif user_input == 'm':
            return 'main'  # Go back to main menu
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
            print(f"\nInvalid input: {e}. Please enter a number, 'm' or 'n'.")

def get_watch_status(title_obj):
    """
    Promps user to inform if item has already been watched
    and updates object using mark_watched method
    
    Args:
        title_obj (Title): The Title object to save
    Returns:
        bool: True (watched), False (not watched)
    """
    while True:
        choice = input(f'\nHave you already watched {title_obj.title}? (y/n): ').strip().lower()
        if choice == 'y':
            title_obj.mark_watched()
            return True
        elif choice == 'n':
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
        user_input = input(
            f'\nHow would you rate {title_obj.title}? '
            f'Select a number from 1-10: ').strip()
        if not user_input.isdigit():
            print("\nInvalid input: Please enter a whole number.")
            continue

        rating = int(user_input)
        try:
            title_obj.set_rating(rating)
            return
        except ValueError as e:
            print(f"\nInvalid input: {e}")

def handle_list_interaction(title_list, list_type):
    """
     Display the menu with CRUD actions for 
    """
    valid_actions = {'r', 'd', 'w'}
    while True:
        print("\nAvailable commands:")
        print("r <num> → rate title")
        if list_type == "watchlist":
            print("w <num> → mark as watched")
        print("d <num> → delete title")
        print("m → return to main menu")
        command = input("\n> ").strip().lower()
        if command == 'm':
            break

        try:
            # split command into action and title index
            action, idx_str = command.split(maxsplit=1)
        except ValueError:
            print("Invalid command format. Try something like 'r 1' or 'd 2'.")
            continue
        if action not in valid_actions:
            print(f'Invalid action: {action}. Valid actions are:{','.join(valid_actions)}')
            continue
        if not idx_str.isdigit():
            print(f'Invalid index: {idx_str}. Please provide a valid number.')
            continue
        index = int(idx_str) - 1
        if index < 0 or index >= len(title_list):
            print(f'Invalid title {index}. Select a number between 1 and {len(title_list)}')
            continue  
        title = title_list[index]
        
        #call applicable function
        if action == 'r':
            print(f'You want to change the rating of {title.title}')
        elif action == 'd':
            print(f'You want to delete {title.title}')
        elif action == 'w':
            print(f'You want to mark {title.title} as watched')
            
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
                title_objects = [Title(result) for result in sorted_results]
                displayed_titles = display_title_entries(title_objects, 'search', 5)
                # 7. Select result, back to main menu or new search
                selected_item = select_item_from_results(displayed_titles)
                if selected_item == 'main':
                    print("\nReturning to main menu...")
                    break # Go back to main menu
                if selected_item is None:
                    print("\nStarting a new search...")
                    continue # Go back to search (1)
                # 8. Valid item (int) is selected
                print(f"\nYou've selected {selected_item.title} ({selected_item.release_date})")
                # 9. Check for item duplicate before saving
                if not check_for_duplicate(selected_item, google_sheet):
                    if get_watch_status(selected_item):
                        get_title_rating(selected_item)
                    else:
                        selected_item.watched = False
                    print(f"\nAdding {selected_item.title} to your list...")
                    save_item_to_list(google_sheet, selected_item)
                    break
                break
        if user_choice in ['watched', 'watchlist']:
            # Set watch_flag to True is choice is watched
            watched_flag = user_choice == 'watched'
            your_titles = get_titles_by_watch_status(google_sheet, watched_flag)
            if not your_titles:
                print(f"\nNo {user_choice} title found.")
                continue
            your_titles_obj = [Title.from_sheet_row(row) for row in your_titles]
            display_title_entries(your_titles_obj, user_choice)
            handle_list_interaction(your_titles_obj, user_choice)
            continue

if __name__ == "__main__":
    main()
