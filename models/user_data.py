"""
User data module

This module contains the UserTitleData class,
which tracks user-specific metadata
for media titles such as watch status, dates, and rating
"""
from utils.utils import get_current_timestamp


class UserTitleData:
    """
    Stores user-generated attributes (watched, rating, etc.)
    associated with a specific title

    Attributes:
        added_date (str): Timestamp of when the title was added
        watched (bool): Identifies if title has been watched
        watched_date (str): Timestamp of when the title was watched
        rating ([int, str]): User's rating for the title (1-5) or 'N/A'
    """
    def __init__(
        self, watched=False,
        added_date=None,
        watched_date='',
        rating='N/A'
    ):
        """
        Initializes a new UserTitleData instance

        Args:
            watched (bool, optional): Initial watched status defaults to False
            added_date (str, optional): added action timestamp
            watched_date (str, optional): watched action timestamp
            rating ([int, str], optional): User's title rating (1-5) or 'N/A'
        """
        self.added_date = added_date or get_current_timestamp()
        self.watched = watched
        self.watched_date = watched_date
        self.rating = rating

    def toggle_watched(self, rating=None):
        """
        Toggles watch status of a title
        If toggled to "watched",
        also updates the watched date
        and optionally sets a rating

        Args:
            rating (int, optional): Rating to assign if marking as watched
        """
        self.watched = not self.watched  # toggle value
        if self.watched:
            self.watched_date = get_current_timestamp()
            if rating:
                self.set_rating(rating)
        else:
            # reset on toggle to False
            self.watched_date = ""
            self.rating = ""

    def set_rating(self, rating):
        """
        Set rating for this title
        Args:
            rating (int): A rating between 1 and 5.

        Raises:
            ValueError: If the rating is outside the valid range
        """
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        self.rating = rating

    def to_dict(self):
        """
        Converts the user title data to a dictionary format

        Returns:
            dict: dictionary with user title metadata
        """
        return {
            'watched': self.watched,
            'added_date': self.added_date,
            'watched_date': self.watched_date,
            'rating': self.rating
        }

    @classmethod
    def from_dict(cls, data):
        """
        Instantiates a UserTitleData object from Google Sheet row

        Args:
            data (dict): dictionary representing a row from Google Sheets

        Returns:
            UserTitleData: opulated UserTitleData instance
        """
        return cls(
            watched=str(data.get('is_watched', 'False')).lower() == 'true',
            added_date=data.get('added_date'),
            watched_date=data.get('watched_date'),
            rating=data.get('rating', 'N/A')
        )
