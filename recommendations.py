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
        trending_results = fetch_trending_titles(TMDB_API_KEY)
        trending_title_objects = prepare_title_objects_from_tmdb(trending_results)
        print("\nYour list is looking a little empty.")
        print("Check out what’s trending and find something that sparks your interest!")
        displayed_titles = display_title_entries(trending_title_objects, 'trending', 6)
        results_selected_title = select_item_from_results(displayed_titles, mode)
        if results_selected_title == 'main' or results_selected_title is None:
            print('\nReturning to main menu...')
        else:
            print(f"\n📥 You've selected {results_selected_title.title}"
                  f"({results_selected_title.release_date})")
        handle_title_selection(results_selected_title, google_sheet)
    elif not watched_items:
        print("\nYou haven’t watched anything yet, but your watchlist has some great options.")
        print("\nHere are the most popular ones to get you started.")
        watchlist_titles = get_titles_by_watch_status(google_sheet, False)
        title_objects = [Title.from_sheet_row(row) for row in watchlist_titles]
        sorted_titles = sort_items_by_popularity(title_objects)
        displayed_titles = display_title_entries(sorted_titles, 'recommendation', 6)
    elif not watchlist_items:
        print("You have no watchlist items, but you have some watched items!")
        watched_titles = get_titles_by_watch_status(google_sheet, True)
        watched_titles = get_titles_by_watch_status(google_sheet, True)
        title_objects = [Title.from_sheet_row(row) for row in watched_titles]
        top_rated_titles = get_top_rated_titles(title_objects)
        preferred_genre = get_preferred_genre(top_rated_titles)
        titles_in_genre = filter_list_by_genre(top_rated_titles, preferred_genre)
        for index, title in enumerate(titles_in_genre, start=1):
            title_str = title.title
            genres = title.genres
            rating = title.user_data.rating
            watched_date = title.user_data.watched_date
            print(f'({index}) {title_str} - {genres} - {rating} - {watched_date}')
        top_title = get_most_relevant_title(titles_in_genre)
        title_str = top_title.title
        genres = top_title.genres
        rating = top_title.user_data.rating
        watched_date = top_title.user_data.watched_date
        top_title_media_type = top_title.media_type
        top_title_id = top_title.id
        print(f'{title_str} - {genres} - {rating} - {watched_date}')
        recommended_titles = fetch_title_base_recommendation(
            top_title_media_type,
            top_title_id,
            TMDB_API_KEY
            )
        recommended_titles_object = prepare_title_objects_from_tmdb(recommended_titles)
        displayed_titles = display_title_entries(recommended_titles_object, 'recommendation', 6)
        results_selected_title = select_item_from_results(displayed_titles, mode)
        if results_selected_title == 'main' or results_selected_title is None:
            print('\nReturning to main menu...')
        else:
            print(f"\n📥 You've selected {results_selected_title.title}"
                  f"({results_selected_title.release_date})")
        handle_title_selection(results_selected_title, google_sheet)
    else:
        print("You have watched items and watchlist items")
        watched_titles = get_titles_by_watch_status(google_sheet, True)
        watched_titles_objects = [Title.from_sheet_row(row) for row in watched_titles]
        watchlist_titles = get_titles_by_watch_status(google_sheet,False)
        watchlist_titles_objects = [Title.from_sheet_row(row) for row in watchlist_titles]
        top_rated_titles = get_top_rated_titles(watched_titles_objects)
        preferred_genre = get_preferred_genre(top_rated_titles)
        titles_in_genre = filter_list_by_genre(top_rated_titles, preferred_genre)
        top_title = get_most_relevant_title(titles_in_genre)
        titles_matching_genre = filter_list_by_genre(watchlist_titles_objects, preferred_genre)
        for index, title in enumerate(titles_matching_genre, start=1):
            title_str = title.title
            genres = title.genres
            rating = title.user_data.rating
            watched_date = title.user_data.watched_date
            print(f'({index}) {title_str} - {genres} - {rating} - {watched_date}')


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
    preferred_genre_count = genres_count[preferred_genre]
    print(f'Your preferred genre: {preferred_genre}: {preferred_genre_count} views')
    return preferred_genre

def filter_list_by_genre(title_list, genre):
    """
    Filters a list by a given genre
    """
    return [title for title in title_list if genre in title.genres]

def sort_titles_by_relevance(title_list):
    """
    Sort titles by highest rating and recent view
    """
    return sorted(
        title_list, key=lambda title: (
            title.user_data.rating, title.user_data.watched_date
            ),
        reverse=True
        )

def get_most_relevant_title(title_list):
    """
    Returns most relevant title
    """
    sorted_titles = sort_titles_by_relevance(title_list)
    return sorted_titles[0]
