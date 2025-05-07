"""
Initializes the recommendation module by exposing main handler functions.

Enables external modules to access core recommendation features directly.
"""
from .display import display_and_select_title
from .filters import (
    get_top_rated_titles,
    get_preferred_media_type_and_genre_ids,
    filter_list_by_genre,
    partition_list_by_media_type
)
from .genre_analysis import (
    get_preferred_genre,
    calculate_genre_similarity
)
from .handlers import (
    handle_no_watchlist_items,
    handle_no_items,
    handle_no_watched_items,
    handle_watched_and_watchlist
)
from .recs import handle_recommendations
from .smart_recs import (
    get_top_title_by_preferred_genre,
    generate_recommendations_from_history,
    handle_no_top_rated,
    get_personalized_recommendations,
    reorder_titles_by_media_type
)
from .trending import show_trending_titles
from .utils import (
    get_top_title,
    sort_titles_by_relevance
)

__all__ = [
    "display_and_select_title",
    "get_top_rated_titles",
    "get_preferred_media_type_and_genre_ids",
    "filter_list_by_genre",
    "partition_list_by_media_type",
    "get_preferred_genre",
    "calculate_genre_similarity",
    "handle_no_watchlist_items",
    "handle_no_items",
    "handle_no_watched_items",
    "handle_watched_and_watchlist",
    "handle_recommendations",
    "get_top_title_by_preferred_genre",
    "generate_recommendations_from_history",
    "handle_no_top_rated",
    "get_personalized_recommendations",
    "reorder_titles_by_media_type",
    "show_trending_titles",
    "get_top_title",
    "sort_titles_by_relevance",
]
