"""
Helper functions for processing and preparing TMDB API data.

Filters and formats API results into display-ready Title objects.
"""
from models import Title
from utils.utils import calculate_weighted_popularity, sort_items_by_popularity
from .tmdb import (
    TMDB_API_KEY,
    get_genre_mapping
    )

def get_genre_names_from_ids(genre_ids, media_type):
    """
    Fetch genre list of dictionaries, convert to dictionary
    and match with Title's genres_ids

    Args:
        genre_id (list): numeric genre identifier
        media_type (str): Media type of the Title (tv/movie)
    Returns:
        matched_names (list): list of genre names
    """
    genre_list = get_genre_mapping(media_type, TMDB_API_KEY)
    genre_dict = {genre['id']: genre['name'] for genre in genre_list}
    matched_genres = [genre_dict.get(genre_id) for genre_id in genre_ids if genre_id in genre_dict]
    return matched_genres

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
