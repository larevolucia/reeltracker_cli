"""
Provides helper functions for formatting dates, scoring popularity, and sorting.

Supports both raw API data and custom objects for flexible handling.
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

# --- Sorting ---
def sort_items_by_popularity(items):
    """
    Sorts a list of items (dicts or objects) by 'weighted_popularity' if available

    Args:
        items (list): List of dicts or objects

    Returns:
        list: Sorted list by descending popularity
    """
    return sorted(items, key=get_popularity, reverse=True)

# --- Popularity ---
def get_popularity(item):
    """
    Cheks if item is dict or object
    

    Args:
        item (dict / obj): title metadata

    Returns:
        popularity (float): popularity score
    """
    # Handle dicts from TMDb or sheets
    if isinstance(item, dict):
        val = item.get('weighted_popularity') or item.get('popularity', 0)
    else:
        # Handle Title object with .metadata
        metadata = getattr(item, 'metadata', None)
        if metadata:
            val = getattr(metadata, 'weighted_popularity', None)
            if val is None:
                val = getattr(metadata, 'popularity', 0)
        else:
            val = getattr(item, 'weighted_popularity', None)
            if val is None:
                val = getattr(item, 'popularity', 0)

    try:
        return float(val)
    except (ValueError, TypeError):
        print(f"⚠️ Could not convert popularity value: {val}")
        return 0.0

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
