"""
Smart recommendation logic based on user history and preferences

Implements end-to-end recommendation generation using filtering,
genre analysis, and TMDb discovery fallback mechanisms when necessary
"""
from tmdb.tmdb import discover_titles_by_genre
from models.title import (
    prepare_title_objects_from_tmdb
)
from .display import display_and_select_title
from .utils import (
    get_top_title,
    sort_titles_by_relevance
)
from .filters import (
    get_top_rated_titles,
    get_preferred_media_type_and_genre_ids,
    partition_list_by_media_type,
    filter_list_by_genre
)
from .genre_analysis import get_preferred_genre

def get_top_title_by_preferred_genre(title_objects):
    """
    Get the most relevant top-rated title in the preferred genre

    Args:
        title_objects (list): List of Title objects

    Returns:
        Title or None: Top title in the preferred genre, or None if unavailable
    """
    top_rated_titles = get_top_rated_titles(title_objects)
    if not top_rated_titles:
        return None

    preferred_genre = get_preferred_genre(top_rated_titles)
    titles_in_genre = filter_list_by_genre(top_rated_titles, preferred_genre)

    if not titles_in_genre:
        return None

    return get_top_title(titles_in_genre)

def get_personalized_recommendations(watched_titles, watchlist_titles, google_sheet):
    """
    Generate personalized recommendations from watchlist

    Uses the user's top-rated watched titles to determine a preferred genre,
    then sorts watchlist titles by genre and media type matches

    Args:
        watched_titles (list): titles marked as watched
        watchlist_titles (list): titles marked as watchlist

    Returns:
        list: personalized and sorted recommendation list
    """
    if len(watched_titles) <= 3:
        print("\n⚠️  Your viewing history is still quite limited.")
        print("   The more you watch and rate, the better the recommendations!")
    if len(watchlist_titles) <= 3:
        print("\n⚠️  You only have a few titles in your watchlist.")
        print("   Recommendations may be limited. Consider adding more!")
    top_rated_titles = get_top_rated_titles(watched_titles)

    if not top_rated_titles:
        title_list = watched_titles + watchlist_titles
        return handle_no_top_rated(title_list, google_sheet)
    else:
        return generate_recommendations_from_history(top_rated_titles, watchlist_titles)

def handle_no_top_rated(title_list, google_sheet):
    """
    Fallback recommendations when no top-rated titles exists
    
    Analyze all titles in list to determine media_type and genre preference,
    then uses discover API to fetch recommendations

    Args:
        title_list (list): Combined list of watched an watchlist
        google_sheet (obj): Initialized Google Sheet

    Returns:
        list: Recommended list based on preferences
    """
    print("\nIt seems like you didn't find any title you liked yet.")
    print("\n🔄 Analyzing all titles in your list...")
    media_type, genre_id = get_preferred_media_type_and_genre_ids(title_list)
    print(f"\n🔄 Fetching discover titles based on {media_type} preference...")
    discover_results = discover_titles_by_genre(media_type, genre_id)
    if not discover_results:
        print("\n⚠️  Unable to fetch discover titles. Please try again later.")
        return []
    discover_titles_objects = prepare_title_objects_from_tmdb(discover_results, True, media_type)
    return display_and_select_title(discover_titles_objects, 'recommendation', google_sheet)

def generate_recommendations_from_history(top_rated_titles, watchlist_titles):
    """
    Recommed titles based on user's viewing history
    
    Determine prgenre and preference and filters/sorts watchlist
    based on similarity to user's top-rated content

    Args:
        top_rated_titles (list): Titles user rated 3 or above
        watchlist_titles (list): titles in user's watchlist

    Returns:
        list: Sorted list of recommended titles based on viewing history
    """
    preferred_genre = get_preferred_genre(top_rated_titles)
    top_title = get_top_title_by_preferred_genre(top_rated_titles)

    if not top_title or not hasattr(top_title, "metadata"):
        print("\n⚠️  Unable to generate personalized recommendations.")
        return []

    print(f"\nYou've been watching {preferred_genre.lower()} titles, "
          f"such as '{top_title.metadata.title}'!")
    print("\n🔄 Generating recommendations based on genre similarity...")

    top_title_media_type = top_title.metadata.media_type
    filtered_titles = filter_list_by_genre(watchlist_titles, preferred_genre)
    if not filtered_titles:
        relevance_sorted = sort_titles_by_relevance(watchlist_titles, "watchlist", top_title)
    else:
        relevance_sorted = sort_titles_by_relevance(filtered_titles, "watchlist", top_title)

    return reorder_titles_by_media_type(relevance_sorted, top_title_media_type)

def reorder_titles_by_media_type(titles, preferred_media_type):
    """
    Reorder titles by prioritizing the preferred_media_type

    Args:
        titles (list): List of title objects to order
        preferred_media_type (str): preferred media type ('movie' or 'tv')

    Returns:
        list: Reordered list of titles with preferred media_type first
    """
    match, non_match = partition_list_by_media_type(titles, preferred_media_type)
    return match + non_match
