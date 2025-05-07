"""
Genre analysis tools for user preference detection

Provides logic to detect preferred genres, calculate similarity
between titles based on genre overlap, and analyze media type trends.
"""
from collections import defaultdict


def get_preferred_genre(title_list):
    """
    Determine the user's preferred genre based on frequency

    Args:
        title_list (list): List of Title objects

    Returns:
        str: Genre with the highest occurrence
    """
    genres_count = defaultdict(int)
    for title in title_list:
        genres = getattr(getattr(title, 'metadata', None), 'genres', None)
        rating = getattr(getattr(title, 'user_data', None), 'rating', 0)
        if genres and rating:
            for genre in genres:
                genres_count[genre] += rating
    if not genres_count:
        return None

    preferred_genre = max(genres_count, key=genres_count.get)

    return preferred_genre


def calculate_genre_similarity(title_1, title_2):
    """
    Calculate genre similarity score between two titles

    Args:
        title_1 (Title): 1st title
        title_2 (Title): 2nd title

    Returns:
        int: number of shared genres
    """
    similarity_score = (
        len(set(title_1.metadata.genres) & set(title_2.metadata.genres))
        )
    return similarity_score
