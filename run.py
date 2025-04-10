"""
CLI Reel tracker orchestration
"""
from ui.menus import display_main_menu
from ui.action_handlers import (
    handle_search,
    handle_watchlist_or_watched,
)
from .sheets.sheets import initialize_google_sheets
from .recommendations.recommendations import handle_recommendations


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
            handle_search(user_choice, google_sheet)
            continue
        if user_choice in ['watched', 'watchlist']:
            handle_watchlist_or_watched(user_choice, google_sheet)
            continue
        if user_choice == 'recommendation':
            handle_recommendations(user_choice, google_sheet)

if __name__ == "__main__":
    main()
