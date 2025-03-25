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
    print("\n🎬 ReelTracker Menu")
    print("1. Search a new title")
    print("2. See watchlist titles")
    print("3. See watched titles")
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

def display_search_results(title_objects, max_results=5):
    """
    Display TMDB search filtered and sorted results as Title objects
    
    Args:
        results (list): Filtered and sorted results list of Title objects
        max_results (int): Maximum number of results to display
    Returns:
        (list[Title]): Title objects list slice [:max_results]
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
    
    Args:
        title_list (list[Title]): List of Title objects
    Returns:
        Title object: selected item from list
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
        choice = input(f'Have you already watched {title_obj.title}? (y/n): ').strip().lower()
        if choice == 'y':
            title_obj.mark_watched()
            return True
        elif choice == 'n':
            return False
        print("Invalid input. Please type 'y' for yes or 'n' for no.")

def get_title_rating(title_obj):
    """
    Prompts user to provide movie rating 1-10
    updates object using set_rating method
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

def main():
    """
    Main execution function for the CLI Reel Tracker.
    """
    google_sheet = initialize_google_sheets('reeltracker_cli')
    while True:
        user_choice = display_main_menu()
        if user_choice == 'exit':
            print('Goodbye!')
            break
        elif user_choice == 'search':
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
            # 6. Display top results as Title objects
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
            # 10. Check for item duplicate before saving
            if not check_for_duplicate(selected_item, google_sheet):
                if get_watch_status(selected_item):
                    get_title_rating(selected_item)
                else:
                    selected_item.watched = False
                save_item_to_list(google_sheet, selected_item)
                break
        elif user_choice in ['watched', 'watchlist']:
            # Set watch_flag to True is choice is watched
            watched_flag = user_choice == 'watched'
            titles = get_titles_by_watch_status(google_sheet, watched_flag)
            if not titles:
                print("\nNo titles found.")
            else:
                print("\nYour Titles:\n" + "-"*60)
                for i, row in enumerate(titles, 1):
                    print(f'{i}. {row['title']} ({row['release_date']}) - Rated: {row['rating']}')
            break

if __name__ == "__main__":
    main()
