"""
Defines and displays user-facing menus for the CLI interface.

Supports navigation, command parsing, and action selection.
"""

menus = {
    "main": {
        "title": "🎬 ReelTracker Menu",
        "options": {
            "1": "Search and add new title",
            "2": "Manage watchlist titles",
            "3": "Manage watched titles",
            "4": "Get recommendation",
            "5": "See what's trending",
            "e": "Exit"
        },
        "valid_choices": {
            "1": "search",
            "2": "watchlist",
            "3": "watched",
            "4": "recommendation",
            "5": "trending",
            "e": "exit"
        }
    },
    "search": {
        "title": "Search results options:",
        "options": {
            "i <number>": "View more info",
            "<number>": "Select to save",
            "n": "New search",
            "m": "Return to main menu"
        }
    },
    "watchlist": {
        "title": "Manage Watchlist:",
        "options": {
            "w <number>": "Mark as watched and rate",
            "d <number>": "Delete title",
            "m": "Return to main menu"
        }
    },
    "watched": {
        "title": "Manage Watched Titles:",
        "options": {
            "r <number>": "Change rating",
            "w <number>": "Move to watchlist",
            "d <number>": "Delete title",
            "m": "Return to main menu"
        }
    },
    "recommendation": {
        "title": "Recommended Titles options:",
        "options": {
            "i <number>": "View more info",
            "<number>": "Select a title to save",
            "m": "Return to main menu"
        }
    },
    "trending": {
        "title": "Trending Titles options:",
        "options": {
            "i <number>": "View more info",
            "<number>": "Select a title to save",
            "m": "Return to main menu"
        }
     },
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
    valid_actions = {
        key.split()[0] for key in menus[list_type]['options'].keys()
        if key != 'm'
    }

    while True:
        display_menu(list_type)
        print("\nEnter a command like 'd 2' or 'w 1'")
        print("You can also type 'm' to go back to main menu.")
        command = input("> ").strip().lower()

        if command == 'm':
            return None, None
        action, index, error = handle_action_with_index(
            command,
            valid_actions,
            len(title_list)
            )
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
        print("\n⚠️  Invalid option. Please try again.")


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
        return None, None, ("\n⚠️  Invalid command format. "
                            "Try something like 'r 1' or 'd 2'.")
    if action not in valid_actions:
        return None, None, f"\n⚠️  Invalid action '{action}'."
    if not idx_str.isdigit():
        return None, None, f"\n⚠️  Invalid index '{idx_str}'. Use a number."
    index = int(idx_str) - 1
    # if index < 0 or index >= list_length:
    #     return None, None, (f"\n⚠️   Index out of range. "
    #                         f"Choose between 1 and {list_length}.")
    if index < 0 or index >= list_length:
        if list_length == 1:
            return None, None, (
                "\n⚠️  Invalid index. Only one item is available. "
                "Use '1' as the index."
            )
        return None, None, (
                "\n⚠️  Index out of range. "
                f"Choose between 1 and {list_length}."
            )
    return action, index, None
