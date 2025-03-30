"""
CLI Reel tracker orchestration
"""
from sheets import initialize_google_sheets
from menus import display_main_menu
from ui import (
    handle_search,
    handle_watchlist_or_watched
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
            print('\n👋 Goodbye!')
            break
        if user_choice == 'search':
            handle_search(google_sheet)
            continue
        if user_choice in ['watched', 'watchlist']:
            handle_watchlist_or_watched(user_choice, google_sheet)
            continue

if __name__ == "__main__":
    main()
