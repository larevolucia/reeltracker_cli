"""
    Utility functions for filtering, formatting, sorting data and display helpers
"""
import math
from datetime import datetime

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
