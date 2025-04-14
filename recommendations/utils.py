"""
Provides utilities for filtering and ranking recommended titles.

Includes logic for genre detection, similarity scoring, and sorting by
relevance or popularity.
"""
from collections import defaultdict
# from .trending import show_trending_titles
# --- Filtering ---
def get_top_rated_titles(title_list):
    """
    Return titles with a user rating of 3 or higher

    Args:
        titles_list (list): list of Title objects

    Returns:
        list: filtered list of top-rated Title objects
    """
    top_rated_titles = [title for title in title_list if title.user_data.rating >= 3]

    return top_rated_titles

def get_preferred_media_type_and_genre_ids(title_list):
    """
    Determine the user's preferred media_type, genre pair based on frequency

    Args:
        title_list (list): List of Title objects

    Returns:
        tuple [str, str]: (preferred_media_type, preferred_genre_name)
    """
    media_type_genre_count = defaultdict(int)

    for title in title_list:
        metadata = getattr(title, 'metadata', None)
        if not metadata:
            continue
        media_type =  getattr(metadata, 'media_type', None)
        genre_ids =  getattr(metadata, 'genre_ids', None)
        if media_type and genre_ids:
            for genre_id in genre_ids:
                media_type_genre_count[(media_type, genre_id)] += 1
    if not media_type_genre_count:
        print("⚠️ No media types / genre_ids paris found.")
        return None

    preferred_pair = max(media_type_genre_count, key=media_type_genre_count.get)

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
    titles_in_genre = [title for title in title_list if genre in title.metadata.genres]
    if not titles_in_genre:
        print(f'\nNo title in your watchlist matches your preferred genre: {genre}')
        print('\n🔄 Generating recommendations based on sub-genre similiraty and popularity...')
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

# --- Genre Analysis ---
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
        genres =  getattr(getattr(title, 'metadata', None), 'genres', None)
        if genres:
            for genre in genres:
                genres_count[genre] +=1
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
    similarity_score = len(set(title_1.metadata.genres) & set(title_2.metadata.genres))
    return similarity_score

# --- Sorting ---
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

# --- Smart Recommendations ---
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

# def get_personalized_recommendations(watched_titles, watchlist_titles):
#     """
#     Generate personalized recommendations from watchlist

#     Uses the user's top-rated watched titles to determine a preferred genre,
#     then sorts watchlist titles by genre and media type matches

#     Args:
#         watched_titles (list): titles marked as watched
#         watchlist_titles (list): titles marked as watchlist

#     Returns:
#         list: personalized and sorted recommendation list
#     """
#     top_rated_titles = get_top_rated_titles(watched_titles)
#     if not top_rated_titles:
#         print("\nNo title rated above 2...")
#         media_type, genre_id = get_preferred_media_type_and_genre_ids(watched_titles)
#         discover_results = fetch_titles_by_genre(media_type, genre_id)
#         discover_titles_objects = prepare_title_objects_from_tmdb(discover_results, True)
#         return discover_titles_objects
#     preferred_genre = get_preferred_genre(top_rated_titles)
#     top_title = get_top_title_by_preferred_genre(top_rated_titles)
#     if not top_title or not hasattr(top_title, "metadata"):
#         print("\n⚠️  Unable to generate personalized recommendations.")
#         return []
#     print(f"\nYou've been watching {preferred_genre} titles, such as {top_title.metadata.title}!")
#     print("\n🔄 Generating recommendations based on viewing history...")
#     top_title_media_type = top_title.metadata.media_type
#     titles_matching_genre = filter_list_by_genre(watchlist_titles, preferred_genre)
#     relevance_sorted_titles = sort_titles_by_relevance(
#         titles_matching_genre, "watchlist", top_title)
#     match_media_type_titles, non_match_media_type_titles = partition_list_by_media_type(
#         relevance_sorted_titles,
#         top_title_media_type
#         )
#     concatenated_titles = match_media_type_titles + non_match_media_type_titles
#     return concatenated_titles


def get_personalized_recommendations(watched_titles, watchlist_titles):
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
    top_rated_titles = get_top_rated_titles(watched_titles)

    # if not top_rated_titles:
    #    return handle_no_top_rated(watched_titles)

    return generate_recommendations_from_history(top_rated_titles, watchlist_titles)

# def handle_no_top_rated(watched_titles):
#     print("\nNo title rated above 2...")
    # media_type, genre_id = get_preferred_media_type_and_genre_ids(watched_titles)
    # discover_results = fetch_titles_by_genre(media_type, genre_id)
    # if not discover_results:
    #     print("Couldn't connect to TMDB for recommendations")
    #     return None
    # return prepare_title_objects_from_tmdb(discover_results, True)


def generate_recommendations_from_history(top_rated_titles, watchlist_titles):
    preferred_genre = get_preferred_genre(top_rated_titles)
    top_title = get_top_title_by_preferred_genre(top_rated_titles)

    if not top_title or not hasattr(top_title, "metadata"):
        print("\n⚠️  Unable to generate personalized recommendations.")
        return []

    print(f"\nYou've been watching {preferred_genre} titles, such as {top_title.metadata.title}!")
    print("\n🔄 Generating recommendations based on viewing history...")

    top_title_media_type = top_title.metadata.media_type
    filtered_titles = filter_list_by_genre(watchlist_titles, preferred_genre)
    if not filtered_titles:
        relevance_sorted = sort_titles_by_relevance(watchlist_titles, "watchlist", top_title)
    else:
        relevance_sorted = sort_titles_by_relevance(filtered_titles, "watchlist", top_title)

    return reorder_titles_by_media_type(relevance_sorted, top_title_media_type)


def reorder_titles_by_media_type(titles, preferred_media_type):
    match, non_match = partition_list_by_media_type(titles, preferred_media_type)
    return match + non_match
