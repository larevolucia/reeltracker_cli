"""
Displays title data in a formatted, user-friendly layout.

Used for showing search results, lists, and recommendations.
"""


def display_title_entries(title_objects, mode, max_results=None):
    """
    Display a list of Title objects in a table format based on context.

    Args:
        title_objects (list): _description_
        mode (str): _description_
        max_results (int, optional): _description_. Defaults to None.
    Returns:
        (list[Title]): Title objects list slice [:max_results]
    """
    headers = {
        'search': 'Search results',
        'watchlist': 'Your watchlist',
        'watched': 'Your watched titles',
        'recommendation': 'Recommended titles',
        'trending': '🔥 Trending titles',
    }

    print(f"\n{headers.get(mode, 'Titles')}:\n")
    is_watched = mode == 'watched'
    for index, title in enumerate(title_objects[:max_results], start=1):
        if not hasattr(title, "metadata"):
            print(f"⚠️  Skipping item without metadata: {title}")
            continue  # Skip invalid entry
        title_str = title.metadata.title
        if len(str(title_str)) > 30:
            title_str = title_str[:27].rstrip() + "..."
        media_type = title.metadata.media_type
        release = title.metadata.release_date
        rating = title.user_data.rating
        overview = title.metadata.overview
        line = f"{index:>2} | {title_str:<30} | {media_type:<6} | {release:<4}"
        if is_watched:
            line += f" | Rating: {rating:<4}"
        print(line)
        if not is_watched:
            if len(overview) > 100:
                overview = overview[:97].rstrip() + "..."
            print(f'     {overview}')
            print()
    return title_objects[:max_results]
