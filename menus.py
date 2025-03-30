"""
Menu logic and config
"""
menus = {
    "main": {
        "title": "🎬 ReelTracker Menu",
        "options": {
            "1": "Search and add new title",
            "2": "Manage watchlist titles",
            "3": "Manage watched titles",
            "e": "Exit"
        },
        "valid_choices": {
            "1": "search",
            "2": "watchlist",
            "3": "watched",
            "e": "exit"
        }
    },
    "watchlist": {
        "title": "Manage Watchlist",
        "options": {
            "w": "Mark as watched and rate",
            "d": "Delete title",
            "m": "Return to main menu"
        }
    },
    "watched": {
        "title": "Manage Watched Titles",
        "options": {
            "r": "Change rating",
            "w": "Move to watchlist",
            "d": "Delete title",
            "m": "Return to main menu"
        }
    }
}
def display_menu(menu_key):
    """
    Dynamically display menu data from menu.py based on given menu_key
    """
    menu = menus[menu_key]
    print(f"\n{menu['title']}")
    for key, label in menu["options"].items():
        print(f"{key} → {label}")

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
        command = input("> ").strip().lower()

        if command == 'm':
            return None, None
        action, index, error = handle_action_with_index(command, valid_actions, len(title_list))
        if error:
            print(error)
            continue
        return action, index

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
        return None, None, ("\nInvalid command format. Try something like 'r 1' or 'd 2'.")
    if action not in valid_actions:
        return None, None, f"\nInvalid action '{action}'."
    if not idx_str.isdigit():
        return None, None, f"\nInvalid index '{idx_str}'. Use a number."
    index = int(idx_str) - 1
    if index < 0 or index >= list_length:
        return None, None, f"\nIndex out of range. Choose between 1 and {list_length}."
    return action, index, None
