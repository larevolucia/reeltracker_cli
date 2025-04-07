"""
Functions that handle user input
"""
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
        print(f'\nHave you already watched {title_obj.title}? (y/n):')
        command = input("> ").strip().lower()
        if command == 'y':
            title_obj.toggle_watched()
            print(f'\n🔄 Marking {title_obj.title} as watched...')
            return True
        if command == 'n':
            print(f'\n🔄 Marking {title_obj.title} as not watched...')
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
            f'\nHow would you rate {title_obj.title}? '
            f'Select a number from 1-5: ')
        command = input("> ").strip()
        if not command.isdigit():
            print("\n⚠️ Invalid input: Please enter a whole number.")
            continue

        rating = int(command)
        try:
            title_obj.set_rating(rating)
            print(f"\n🔄 Saving {title_obj.title} rating...")
            return title_obj
        except ValueError as e:
            print(f"\n⚠️ Invalid input: {e}")

def select_item_from_results(title_list, mode):
    """
    Allows user to select an item from previously displayed results
    
    Args:
        title_list (list[Title]): List of Title objects
         mode (str): Mode of interaction ('search' or 'recommendation')
    Returns:
        Title object | None | str: Selected item, None (for new search), or 'main' to return
    """
    valid_commands = []
    prompt = ""
    if mode == 'search':
        valid_commands = ['n', 'm']
        prompt = (
            f"\nSelect an item (1-{len(title_list)}) to save it, "
            f"type 'n' for a new search or 'm' to return to main menu: "
        )
    elif mode == 'recommendation':
        valid_commands = ['m']
        prompt = (
            f"\nSelect an item (1-{len(title_list)}) to save it "
            f"or 'm' to return to main menu: "
        )
    else:
        print("⚠️  Unknown mode. Please use 'search' or 'recommendation'.")
        return None
    while True:
        print(prompt)
        command = input("> ").strip().lower()
        if command == 'm':
            return 'main'
        if command == 'n' and mode == 'search':
            return None
        try:
            selection = int(command)
            if not 1 <= selection <= len(title_list):
                raise ValueError(
                    f'Number out of range. You must choose between 1 and '
                    f'{len(title_list)}'
                )

            chosen_item = title_list[selection - 1]

            return chosen_item

        except ValueError as e:
            print(f"\n⚠️  Invalid input: {e}. Please enter a number, or"
                  f" {', '.join(valid_commands)}.")
