"""
Filtering utilities for recommendation logic.

Includes functions to filter and partition Title objects
based on user ratings, genres, and media types.
"""
from collections import defaultdict


def get_top_rated_titles(title_list):
    """
    Return titles with a user rating of 3 or higher

    Args:
        titles_list (list): list of Title objects

    Returns:
        list: filtered list of top-rated Title objects
    """
    top_rated_titles = [
        title for title in title_list
        if isinstance(title.user_data.rating, (int, float))
        and title.user_data.rating >= 3
    ]

    return top_rated_titles


def get_preferred_media_type_and_genre_ids(title_list):
    """
    Determine the user's preferred media_type, genre pair based on frequency

    Args:
        title_list (list): List of Title objects

    Returns:
        tuple [str, str]: (preferred_media_type, preferred_genre_ic)
    """
    media_type_genre_count = defaultdict(int)

    for title in title_list:
        metadata = getattr(title, 'metadata', None)
        if not metadata:
            continue
        media_type = getattr(metadata, 'media_type', None)
        genre_ids = getattr(metadata, 'genre_ids', None)
        if media_type and genre_ids:
            for genre_id in genre_ids:
                media_type_genre_count[(media_type, genre_id)] += 1
    if not media_type_genre_count:
        print("⚠️ No media types / genre_ids pairs found.")
        return None

    preferred_pair = (
        max(media_type_genre_count, key=media_type_genre_count.get)
    )

    return preferred_pair


def filter_list_by_genre(title_list, genre):
    """
    Filter titles by a specific genre

    Args:
        title_list (list): list of Title objects
        genre (str): genre to filter by

    Returns:
        list: Titles that include the given genre
    """
    titles_in_genre = [
        title for title in title_list if genre in title.metadata.genres
        ]
    if not titles_in_genre:
        print(f'\nNo title in your watchlist matching {genre.lower()} genre.')
        print('\n🔄  Recommending titles by popularity...')
        return None
    return titles_in_genre


def partition_list_by_media_type(title_list, target_media_type):
    """
    Split titles into matching and non-matching media types

    Args:
        title_list (list): list of Title objects
        target_media_type (str): media type to filter by

    Returns:
        tuple: (matching titles, non-matching titles)
    """
    match_media_type = []
    non_match_media_type = []
    for title in title_list:
        if title.metadata.media_type == target_media_type:
            match_media_type.append(title)
        else:
            non_match_media_type.append(title)
    return match_media_type, non_match_media_type
