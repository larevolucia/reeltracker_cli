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
    update_item_in_list,
    get_titles_by_watch_status
    )
from utils import filter_results_by_media_type, sort_items_by_popularity
from menus import display_main_menu, handle_list_menu
from ui import (
    get_user_search_input,
    display_title_entries,
    select_item_from_results,
    get_watch_status,
    get_title_rating,
    handle_search
)


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
            handle_search(google_sheet)
            continue
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
                # Toggle watched flag
                selected_title_obj.toggle_watched()
                if selected_title_obj.watched:
                    # get rating if watched True
                    updated_title_obj = get_title_rating(selected_title_obj)
                    title_rating = updated_title_obj.rating
                    print(f'\nMarking {selected_title_obj.title} as watched '
                          f'and rating it {title_rating}')
                else:
                    updated_title_obj = selected_title_obj
                    print(f'\nMoving {selected_title_obj.title} to your watchlist')
                # Update item in list
                update_item_in_list(google_sheet, updated_title_obj)
                continue
            if action == 'r':
                # get new rating value
                updated_title_obj = get_title_rating(selected_title_obj)
                title_rating = updated_title_obj.rating
                # Update item in list
                update_item_in_list(google_sheet, updated_title_obj)
                print(f'\nYou changed {selected_title_obj.title} rating to {title_rating}')
            if action == 'd':
                print(f'\nYou removed {selected_title_obj.title} from your list.')
                continue

if __name__ == "__main__":
    main()
