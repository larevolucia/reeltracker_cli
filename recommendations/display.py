"""Display recommendations
"""
from ui.display import display_title_entries
from ui.user_input import select_item_from_results
from ui.action_handlers import handle_title_selection

def display_and_select_title(titles, mode, google_sheet):
    displayed_titles = display_title_entries(titles, mode, 6)
    selected = select_item_from_results(displayed_titles, mode)
    if selected == 'main' or selected is None:
        print('\nReturning to main menu...')
    else:
        print(f"\n📥 You've selected {selected.metadata.title} ({selected.metadata.release_date})")
        handle_title_selection(selected, google_sheet)
