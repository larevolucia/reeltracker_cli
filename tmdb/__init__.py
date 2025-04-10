"""
Exposes TMDb-related functions for use throughout the app.

Includes search, recommendation, and genre utilities.
"""

from .tmdb import (
    fetch_tmdb_results,
    get_genre_mapping,
    get_genre_names_from_ids,
    fetch_trending_titles,
    fetch_title_base_recommendation
)
