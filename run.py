"""
CLI Reel tracker orchestration
"""
from ui.menus import display_main_menu
from ui.handlers import (
    handle_search,
    handle_watchlist_or_watched,
)
from sheets.auth import initialize_google_sheets
from recommendations.recs import handle_recommendations
from recommendations.trending import show_trending_titles


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
        if user_choice == 'trending':
            show_trending_titles(user_choice, google_sheet)


if __name__ == "__main__":
    main()
