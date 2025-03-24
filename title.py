"""
Title class module
"""
from datetime import datetime

class Title:
    """
    Class to contain Title information and methods
    """
    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title') or data.get('name') or 'No title available'
        self.media_type = data.get('media_type', 'Unknown')
        self.release_date = data.get('release_date') or data.get('first_air_date') or 'Unknown'
        self.genres = data.get('genre_ids', [])
        self.popularity = round(data.get('weighted_popularity', 0), 2)
        self.overview = data.get('overview', 'No overview available')
        self.watched = False
        self.rating = 'N/A'
    def mark_watched(self, rating=None):
        """Allow user to mark title as watched

        Args:
            rating (int, optional): User rating. Defaults to None
        """
        self.watched = True
        if rating:
            self.set_rating(rating)
    def set_rating(self, rating):
        """Allow user to rate watched item

        Args:
            rating (int): User rating

        Raises:
            ValueError: Notify if rating is not a digit
            ValueError: Notify if rating is outside range
        """
        if not rating.isdigit():
            raise ValueError("Invalid input: Please enter a number.")
        if 1 <= rating <= 10:
            raise ValueError("Rating must be between 1 and 10.")
        self.rating = rating
    def to_dict(self):
        """Converts metadata to dictionary format

        Returns:
            dict: title metadata as dictionary
        """
        return {
            "id": self.id,
            "Title": self.title,
            "Media Type": self.media_type,
            "Release Date": self.release_date,
            "Genres": self.genres,
            "Weighted Popularity": self.popularity,
            "Overview": self.overview,
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
            str(datetime.timestamp(datetime.now())),
            str(self.rating)
        ]
        return values
