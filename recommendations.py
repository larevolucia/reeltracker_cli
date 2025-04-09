"""
Recommendation logic
"""
from collections import defaultdict
from tmdb import (
    TMDB_API_KEY,
    fetch_trending_titles,
    fetch_title_base_recommendation)
from sheets import (
    has_items,
    has_watched,
    has_watchlist,
    get_titles_by_watch_status
    )
from ui_actions import (
    prepare_title_objects_from_tmdb,
    select_item_from_results,
    handle_title_selection,
    display_title_entries
    )
from title import Title
from utils import (
    sort_items_by_popularity
    )

def handle_recommendations(mode, google_sheet):
    """
    Recommends titles to the user based on the state of their list
        - If no titles at all: show trending
        - If no watchlist: show similar to watched items
        - If no watched items: show watchlist by popularity
        - If watched and watchlist: selects from watched item

    Args:
        google_sheet (_type_): _description_
    """
    items = has_items(google_sheet)
    watched_items = has_watched(google_sheet)
    watchlist_items = has_watchlist(google_sheet)
    if not items:
        handle_no_items(google_sheet, mode)
    elif not watched_items:
        handle_no_watched_items(google_sheet)
    elif not watchlist_items:
        handle_no_watchlist_items(google_sheet, mode)
    else:
        print("You have watched items and watchlist items")
        watched_titles = get_titles_by_watch_status(google_sheet, True)
        watched_titles_objects = [Title.from_sheet_row(row) for row in watched_titles]
        watchlist_titles = get_titles_by_watch_status(google_sheet,False)
        watchlist_titles_objects = [Title.from_sheet_row(row) for row in watchlist_titles]
        top_rated_titles = get_top_rated_titles(watched_titles_objects)
        preferred_genre = get_preferred_genre(top_rated_titles)
        titles_in_genre = filter_list_by_genre(top_rated_titles, preferred_genre)
        top_title = get_top_title(titles_in_genre)
        title_str = top_title.title
        genres = top_title.genres
        rating = top_title.user_data.rating
        watched_date = top_title.user_data.watched_date
        top_title_media_type = top_title.media_type
        print(f'{title_str} - {genres} - {rating} - {watched_date}')
        top_title_media_type = top_title.media_type
        titles_matching_genre = filter_list_by_genre(watchlist_titles_objects, preferred_genre)
        relevance_sorted_titles = sort_titles_by_relevance(
            titles_matching_genre, "watchlist", top_title)
        match_media_type_titles, non_match_media_type_titles = partition_list_by_media_type(
            relevance_sorted_titles,
            top_title_media_type
            )
        for index, title in enumerate(match_media_type_titles, start=1):
            title_str = title.title
            genres = title.genres
            popularity = title.popularity
            watched_date = title.user_data.watched_date
            similarity_score = calculate_genre_similarity(title, top_title)
            print(f'({index}) {title_str} - {genres} - {popularity} - {similarity_score}')
        for index, title in enumerate(non_match_media_type_titles, start=1):
            title_str = title.title
            genres = title.genres
            popularity = title.popularity
            watched_date = title.user_data.watched_date
            similarity_score = calculate_genre_similarity(title, top_title)
            print(f'({index}) {title_str} - {genres} - {popularity} - {similarity_score}')


def handle_no_items(google_sheet, mode):
    print("\nYour list is looking a little empty.")
    print("Check out what’s trending and find something that sparks your interest!")
    trending_results = fetch_trending_titles(TMDB_API_KEY)
    trending_title_objects = prepare_title_objects_from_tmdb(trending_results)
    display_and_select_title(trending_title_objects, mode, google_sheet)

def handle_no_watched_items(google_sheet):
    print("\nYou haven't watched anything yet, but your watchlist has some great options.")
    print("\nHere are the most popular ones to get you started.")
    watchlist_titles = get_titles_by_watch_status(google_sheet, False)
    title_objects = build_title_objects_from_sheet(watchlist_titles)
    sorted_titles = sort_items_by_popularity(title_objects)
    display_title_entries(sorted_titles, 'recommendation', 6)

def handle_no_watchlist_items(google_sheet, mode):
    print("\nYou haven't got any titles on your watchlist yet!")
    watched_titles = get_titles_by_watch_status(google_sheet, True)
    title_objects = build_title_objects_from_sheet(watched_titles)
    top_title = get_top_title_by_preferred_genre(title_objects)

    top_title_media_type = top_title.media_type
    top_title_id = top_title.id
    title_str = top_title.title
    top_title_media_type = top_title.media_type

    print(f"\nYou've recently liked {title_str}. "
          "Here are some titles you might also like...")

    recommended_titles = fetch_title_base_recommendation(
        top_title_media_type,
        top_title_id,
        TMDB_API_KEY
        )
    
    recommended_titles_object = prepare_title_objects_from_tmdb(recommended_titles)
    display_and_select_title(recommended_titles_object, mode, google_sheet)

def get_top_rated_titles(titles_list):
    """
    Extracts top rated items from list
    """
    top_rated_titles = [title for title in titles_list if title.user_data.rating >= 3]

    return top_rated_titles

def get_preferred_genre(title_list):
    """
    Analyse list and provides preferred genre
    """
    genres_count = defaultdict(int)
    for title in title_list:
        for genre in title.genres:
            genres_count[genre] +=1
    preferred_genre = max(genres_count, key=genres_count.get)

    return preferred_genre

def filter_list_by_genre(title_list, genre):
    """
    Filters a list by a given genre
    """
    return [title for title in title_list if genre in title.genres]

def sort_titles_by_relevance(title_list, mode='watched', reference_title=None):
    """
    Sort titles by highest rating and recent view
    """
    if mode == "watched":
        return sorted(
            title_list, key=lambda title: (
                title.user_data.rating, title.user_data.watched_date
                ),
            reverse=True
            )
    elif mode == "watchlist" and reference_title:
        return sorted(
            title_list,
            key=lambda title: (
                calculate_genre_similarity(title, reference_title),
                title.popularity
                ),
            reverse=True
            )
    else:
        print("Couldn't sort titles by relevance")
        return []

def get_top_title(title_list):
    """
    Returns most relevant title
    """
    sorted_titles = sort_titles_by_relevance(title_list, 'watched', None)
    return sorted_titles[0]

def partition_list_by_media_type(title_list, target_media_type):
    """
    Splits a single list into two
    using media_type as criteria

    Args:
        title_list (_type_): _description_
    """
    match_media_type = []
    non_match_media_type = []
    for title in title_list:
        if title.media_type == target_media_type:
            match_media_type.append(title)
        else:
            non_match_media_type.append(title)
    return match_media_type, non_match_media_type

def calculate_genre_similarity(title_1, title_2):
    """
    Score titles acording to subgenre similarity

    Args:
        title_list (_type_): _description_
        top_title (_type_): _description_
    """
    similarity_score = len(set(title_1.genres) & set(title_2.genres))
    return similarity_score

def display_and_select_title(titles, mode, google_sheet):
    displayed_titles = display_title_entries(titles, mode, 6)
    selected = select_item_from_results(displayed_titles, mode)
    if selected == 'main' or selected is None:
        print('\nReturning to main menu...')
    else:
        print(f"\n📥 You've selected {selected.title} ({selected.release_date})")
        handle_title_selection(selected, google_sheet)

def build_title_objects_from_sheet(sheet_rows):
    return [Title.from_sheet_row(row) for row in sheet_rows]

def get_top_title_by_preferred_genre(title_objects):
    """
    Filters top-rated titles by user's preferred genre and returns
    the most relevant title.

    Args:
        title_objects (list[Title]): List of Title objects

    Returns:
        Title: Most relevant title in preferred genre
    """
    top_rated_titles = get_top_rated_titles(title_objects)
    if not top_rated_titles:
        return None

    preferred_genre = get_preferred_genre(top_rated_titles)
    titles_in_genre = filter_list_by_genre(top_rated_titles, preferred_genre)

    if not titles_in_genre:
        return None

    return get_top_title(titles_in_genre)
