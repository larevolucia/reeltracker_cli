"""
Handles all user input for search, selection, watch status, and ratings.

Ensures valid, interactive prompts for various workflows.
"""
from ui.menus import display_menu, handle_action_with_index

def get_user_search_input(prompt="\nSearch a title to get started: "):
    """
    Prompts user input for searching a title. Ensures non-empty input
    
    Args:
        prompt (str): Prompt message presented before input
    
    Returns:
        str: User input string
    """
    while True:
        print(prompt)
        user_query = input("> ").strip()
        if user_query:
            return user_query
        print('\n⚠️  Search cannot be emtpy. Please try again.\n')

def get_watch_status(title_obj):
    """
    Promps user to inform if item has already been watched
    and updates object using toggle_watched method
    
    Args:
        title_obj (Title): The Title object to save
    Returns:
        bool: True (watched), False (not watched)
    """
    while True:
        print(f'\nHave you already watched {title_obj.metadata.title}? (y/n):')
        command = input("> ").strip().lower()
        if command == 'y':
            title_obj.toggle_watched()
            print(f'\n🔄 Marking {title_obj.metadata.title} as watched...')
            return True
        if command == 'n':
            print(f'\n🔄 Marking {title_obj.metadata.title} as not watched...')
            return False
        print("\n⚠️  Invalid input. Please type 'y' for yes or 'n' for no.")

def get_title_rating(title_obj):
    """
    Prompts user to provide movie rating 1-5
    updates object using set_rating method
    Args:
        title_obj(Title): The Title object to save
    """
    while True:
        print(
            f'\nHow would you rate {title_obj.metadata.title}? '
            f'Select a number from 1-5: ')
        command = input("> ").strip()
        if not command.isdigit():
            print("\n⚠️ Invalid input: Please enter a whole number.")
            continue

        rating = int(command)
        try:
            title_obj.set_rating(rating)
            print(f"\n🔄 Saving {title_obj.metadata.title} rating...")
            return title_obj
        except ValueError as e:
            print(f"\n⚠️ Invalid input: {e}")

def select_item_from_results(title_list, mode):
    """
    Allows user to select a title or view more info from the results list
    Consistent with 'watchlist' and 'watched' command formats.

    Args:
        title_list (list[Title]): List of Title objects
        mode (str): 'search' or 'recommendation'
    Returns:
        Title object | None | 'main': Selected item, request new search, or return to main
    """
    menu_key =  mode
    valid_actions = {'i'}
    while True:
        display_menu(menu_key)
        print("\nEnter a command like '1', 'i 2', or 'm'")
        if mode == "search":
            print("You can also type 'n' to start a new search.")

        command = input("> ").strip().lower()

        if command == 'm':
            return 'main'
        if command == 'n' and mode == 'search':
            return None

        # Handle commands like 'i 2'
        if ' ' in command:
            action, index, error = handle_action_with_index(command, valid_actions, len(title_list))
            if error:
                print(error)
                continue
            if action == 'i':
                item = title_list[index]
                print(f"\nAbout {item.metadata.title} ({item.metadata.release_date}):\n")
                print(f"   - Type: {item.metadata.media_type}")
                print(f"   - Genres: {', '.join(item.metadata.genres)}")
                print(f"   - Popularity: {item.metadata.popularity}")
                print(f"   - Overview: {item.metadata.overview}")
            continue  # Go back to selection after info

        # Handle single-number selection
        try:
            selection = int(command)
            if 1 <= selection <= len(title_list):
                return title_list[selection - 1]
            else:
                print(f"\n⚠️  Number out of range. Choose between 1 and {len(title_list)}.")
        except ValueError:
            print("\n⚠️  Invalid input. Try a number, 'i <number>', 'n', or 'm'.")

def confirm_action(prompt="\nAre you sure you want to proceed? (y/n): "):
    """
    Request user action confirmation

    Args:
        prompt (str, optional): Prompts user for action confirmation. 
            Defaults to "\nAre you sure you want to proceed? (y/n): ".

    Returns:
        (bool): True (confirms) / False 
    """
    while True:
        response = input(prompt).strip().lower()
        if response in ('y', 'yes'):
            return True
        if response in ('n', 'no'):
            return False
        print("⚠️  Please enter 'y' for yes or 'n' for no.")
