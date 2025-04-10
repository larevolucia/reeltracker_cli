"""
Helpers
"""
from models import Title
from utils.utils import calculate_weighted_popularity, sort_items_by_popularity

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
