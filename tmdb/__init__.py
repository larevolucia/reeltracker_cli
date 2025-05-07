"""
Exposes TMDb-related functions for use throughout the app.

Includes search, recommendation, and genre utilities.
"""

from .tmdb_api import (
    fetch_tmdb_results,
    fetch_trending_titles,
    fetch_title_base_recommendation,
    discover_titles_by_genre,
    get_genre_mapping
)
from .utils import (
    get_genre_names_from_ids,
    filter_results_by_media_type
)

__all__ = [
    "fetch_tmdb_results",
    "fetch_trending_titles",
    "fetch_title_base_recommendation",
    "discover_titles_by_genre",
    "get_genre_mapping",
    "get_genre_names_from_ids",
    "filter_results_by_media_type",
]
