"""
Title class module
"""
from datetime import datetime
from utils import extract_year

# current dateTime
now = datetime.now()

# convert to string
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")


class Title:
    """
    Class to contain Title information and methods
    """
    def __init__(self, data):
        # print("Incoming data:", data)
        self.id = data.get('id')
        self.title = data.get('title') or data.get('name') or 'No title available'
        self.media_type = data.get('media_type', 'Unknown')
        release_date = data.get('release_date') or data.get('first_air_date') or 'Unknown'
        if release_date != 'Unknown':
            self.release_date = extract_year(release_date)
        self.genres = data.get('genre_ids', [])
        self.popularity = round(data.get('weighted_popularity', 0), 2)
        self.overview = data.get('overview', 'No overview available')
        self.watched = False
        self.added_date = date_time_str
        self.watched_date = None
        self.rating = None
    def mark_watched(self, rating=None):
        """Allow user to mark title as watched

        Args:
            rating (int, optional): User rating. Defaults to None
        """
        self.watched = True
        self.watched_date = date_time_str
        if rating:
            self.set_rating(rating)
    def set_rating(self, rating):
        """Allow user to rate watched item

        Args:
            rating (int): User rating

        Raises:
            ValueError: Notify if rating is not valid
        """
        if not 1 <= rating <= 10:
            raise ValueError("Rating must be between 1 and 10.")
        self.rating = rating
    def to_dict(self):
        """Converts metadata to dictionary format

        Returns:
            dict: title metadata as dictionary
        """
        return {
            "id": self.id,
            "title": self.title,
            "media_type": self.media_type,
            "release_date": self.release_date,
            "genres": self.genres,
            "weighted_popularity": self.popularity,
            "overview": self.overview,
            "is_watched": self.watched,
            "added_date": self.added_date,
            "watched_date":self.watched_date,
            "rating": self.rating
        }

    def to_sheet_row(self):
        """Converts metadata to list format

        Returns:
            lists: title metadata as lists
        """
        values = [
            self.id,
            self.title,
            self.media_type,
            self.release_date,
            ', '.join(map(str, self.genres)),
            str(self.popularity),
            self.overview,
            str(self.watched),
            self.added_date,
            self.watched_date,
            str(self.rating)
        ]
        return values
