"""
    Utility functions for filtering, formatting, sorting data and display helpers
"""
import math
from datetime import datetime
from title import Title

# --- Formatting ---
def extract_year(date):
    """
    Use datetime to extract year from string

    Args:
        date (str): YYYY-MM-DD format
    """
    d = datetime.strptime(date, '%Y-%m-%d')
    year_string = d.strftime("%Y")
    return year_string

def get_current_timestamp():
    """
    Give current timestamp

    Returns:
        _str_: YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# --- Popularity ---
def get_popularity(item):
    """
    Cheks if item is dict or object
    

    Args:
        item (dict / obj): title metadata

    Returns:
        popularity (float): popularity score
    """
    if isinstance(item, dict):
        return item.get('weighted_popularity') or item.get('popularity', 0)
    # Fall back to .popularity (which is a string in Title)
    raw_value = getattr(item, 'weighted_popularity', None)
    if raw_value is None:
        raw_value = getattr(item, 'popularity', '0')
    try:
        return float(raw_value)
    except (ValueError, TypeError):
        return 0

def calculate_weighted_popularity(item):
    """
    Calculates weighted popularity based on popularity * log10 vote_count

    Args:
        item (dict): TMDb item dictionary

    Returns:
        float: Weighted popularity score
    """
    popularity = item.get('popularity', 0)
    vote_count = item.get('vote_count', 0)
    # Apply logarithms weighting vote_count to prevent extreme dominance
    weighted_popularity = popularity * math.log(vote_count + 1, 10)

    return weighted_popularity

def sort_items_by_popularity(items):
    """
    Sorts a list of items (dicts or objects) by 'weighted_popularity' if available

    Args:
        items (list): List of dicts or objects

    Returns:
        list: Sorted list by descending popularity
    """
    return sorted(items, key=get_popularity, reverse=True)

# --- Display ---
def display_title_entries(title_objects, mode, max_results=None):
    """
    Display a list of Title objects in a table format based on context.
    
    Args:
        title_objects (list): _description_
        mode (str): _description_
        max_results (int, optional): _description_. Defaults to None.
    Returns:
        (list[Title]): Title objects list slice [:max_results]
    """
    headers = {
        'search': 'Search results',
        'watchlist': 'Your watchlist',
        'watched': 'Your watched titles',
        'trending': 'Trending titles',
        'recommendation': 'Recommended titles',
    }

    print(f"\n{headers.get(mode, 'Titles')}:\n")
    is_watched = mode == 'watched'
    for index, title in enumerate(title_objects[:max_results], start=1):
        title_str = title.title
        if len(title_str) > 30:
            title_str = title_str[:27].rstrip() + "..."
        media_type = title.media_type
        release = title.release_date
        rating = title.user_data.rating
        overview = title.overview
        popularity = title.popularity
        line = f"{index:>2} | {title_str:<30} | {media_type:<6} | {release:<4}"
        line += f" | Popularity: {popularity:<4}"
        if is_watched:
            line += f" | Rating: {rating:<4}"
        print(line)
        if not is_watched:
            if len(overview) > 100:
                overview = overview[:97].rstrip() + "..."
            print(f'     {overview}')
            print()
    return title_objects[:max_results]

# --- API Result Transformation ---
def prepare_title_objects_from_tmdb(api_results):
    """
    Filters, sorts, and converts TMDB api results into Title objects

    Args:
        api_results (list): Raw results from TMDB API

    Returns:
        list[Title]: List of Title objects ready to display
    """
    filtered_results = filter_results_by_media_type(api_results)
    if not filtered_results:
        return []
    for result in filtered_results:
        weighted_popularity = calculate_weighted_popularity(result)
        result['weighted_popularity'] = weighted_popularity
    sorted_results = sort_items_by_popularity(filtered_results)
    title_objects = [Title(result) for result in sorted_results]
    return title_objects

def filter_results_by_media_type(result_list, allowed_media_types=('movie', 'tv')):
    """
    Filters the TMDB results by media_type
    Args:
        result_list (list): list of dictionaries from API
        allowed_media_types(tuple): Types used for filtering   
    Returns: 
        list: Filtered list limited to allowed media types
    """
    return [
        result for result in result_list
        if result.get("media_type") in allowed_media_types
        ]
