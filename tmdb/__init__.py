"""
Exposes TMDb-related functions for use throughout the app.

Includes search, recommendation, and genre utilities.
"""

from .tmdb import (
    fetch_tmdb_results,
    get_genre_mapping,
    fetch_trending_titles,
    fetch_title_base_recommendation
)
from .utils import (
    get_genre_names_from_ids,
    prepare_title_objects_from_tmdb,
    filter_results_by_media_type
    )
