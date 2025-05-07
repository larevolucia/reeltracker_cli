"""
Provides utilities for sorting titles.

Supports sorting by user ratings, recency, genre similarity,
and media type preference to enhance recommendation relevance
"""
from .genre_analysis import calculate_genre_similarity


def get_top_title(title_list):
    """
    Return the top title based on rating and recency

    Args:
        title_list (list): list of Title objects

    Returns:
        Title: most relevant title
    """
    sorted_titles = sort_titles_by_relevance(title_list, 'watched', None)
    if not sorted_titles:
        return None
    top_title = sorted_titles[0]
    return top_title


def sort_titles_by_relevance(title_list, mode='watched', reference_title=None):
    """
    Sort titles by rating and recency, or by genre similarity and popularity

    Args:
        title_list (list): List of Title objects
        mode (str): 'watched' or 'watchlist'
        reference_title (Title, optional): Title to compare for similarity

    Returns:
        list: Sorted list of Title objects.
    """
    if mode == "watched":
        return sorted(
            title_list, key=lambda title: (
                title.user_data.rating, title.user_data.watched_date
                ),
            reverse=True
            )
    if mode == "watchlist" and reference_title:
        return sorted(
            title_list,
            key=lambda title: (
                calculate_genre_similarity(title, reference_title),
                title.metadata.popularity
                ),
            reverse=True
            )
    else:
        print("Couldn't sort titles by relevance")
        return []
