"""
Handles displaying titles and user selection for recommendations.
"""
from ui.display import display_title_entries
from ui.user_input import select_item_from_results
from ui.action_handlers import handle_title_selection

def display_and_select_title(titles, mode, google_sheet):
    """
    Display a list of recommended titles, prompt for selection, and handle it

    Shows a subset of titles based on the given mode, lets the user select one,
    and processes the selected item. If the user cancels or returns to the main
    menu, it exits without further action. Otherwise, it handles the selection.

    Args:
        titles (list): list of title objects to display and choose from
        mode (str): current interaction mode (e.g., 'search', 'recommendation')
        google_sheet: Google Sheets object used to log or track the selection

    Returns:
        None
    """
    displayed_titles = display_title_entries(titles, mode, 6)
    selected = select_item_from_results(displayed_titles, mode)
    if selected == 'main' or selected is None:
        print('\nReturning to main menu...')
    else:
        print(f"\n📥 You've selected {selected.metadata.title} ({selected.metadata.release_date})")
        handle_title_selection(selected, google_sheet)
