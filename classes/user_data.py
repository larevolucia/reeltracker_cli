"""
User data module
"""
from utils import get_current_timestamp

class UserTitleData:
    """
    Class to contain user-generated data related to a Title
    """
    def __init__(self, watched=False, added_date=None, watched_date='', rating='N/A'):
        self.watched = watched
        self.added_date = added_date or get_current_timestamp()
        self.watched_date = watched_date
        self.rating = rating
    def toggle_watched(self, rating=None):
        """Allow user to mark title as watched

        Args:
            rating (int, optional): User rating. Defaults to None
        """
        self.watched = not self.watched # toggle value
        if self.watched:
            self.watched_date = get_current_timestamp()
            if rating:
                self.set_rating(rating)
        else:
            # reset on toggle to False
            self.watched_date = ""
            self.rating = ""
    def set_rating(self, rating):
        """Allow user to rate watched item

        Args:
            rating (int): User rating

        Raises:
            ValueError: Notify if rating is not valid
        """
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        self.rating = rating

    def to_dict(self):
        """Converts metadata to dictionary format

        Returns:
            dict: user's title consumption dictionary metadata 
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
        Creates a user's title data object from Google Sheet row
        """
        return cls(
            watched=str(data.get('is_watched', 'False')).lower() == 'true',
            added_date=data.get('added_date'),
            watched_date=data.get('watched_date'),
            rating=data.get('rating', 'N/A')
        )
