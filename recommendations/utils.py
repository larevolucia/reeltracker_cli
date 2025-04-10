from collections import defaultdict

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
        for genre in title.metadata.genres:
            genres_count[genre] +=1
    preferred_genre = max(genres_count, key=genres_count.get)

    return preferred_genre

def filter_list_by_genre(title_list, genre):
    """
    Filters a list by a given genre
    """
    return [title for title in title_list if genre in title.metadata.genres]

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
                title.metadata.popularity
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
    top_title = sorted_titles[0]
    return top_title

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
        if title.metadata.media_type == target_media_type:
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
    similarity_score = len(set(title_1.metadata.genres) & set(title_2.metadata.genres))
    return similarity_score

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

def get_personalized_recommendations(watched_titles, watchlist_titles):
    top_rated_titles = get_top_rated_titles(watched_titles)
    preferred_genre = get_preferred_genre(top_rated_titles)
    top_title = get_top_title_by_preferred_genre(top_rated_titles)
    print(f"\nYou've been watching {preferred_genre} titles, such as {top_title.metadata.title}!")
    print("\n🔄 Generating recommendations based on viewing history...")
    top_title_media_type = top_title.metadata.media_type
    titles_matching_genre = filter_list_by_genre(watchlist_titles, preferred_genre)
    relevance_sorted_titles = sort_titles_by_relevance(
        titles_matching_genre, "watchlist", top_title)
    match_media_type_titles, non_match_media_type_titles = partition_list_by_media_type(
        relevance_sorted_titles,
        top_title_media_type
        )
    concatenated_titles = match_media_type_titles + non_match_media_type_titles
    return concatenated_titles
