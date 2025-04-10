"""
Title class module

Defines the `Title` class, which combines media metadata (fetched from TMDb) with
user-generated data such as watch status and ratings

The class supports integration with Google Sheets for persistent storage,
and includes methods for data transformation from and to spreadsheet rows.
"""

from utils.utils import extract_year
from tmdb.utils import get_genre_names_from_ids
from .user_data import UserTitleData
from .title_metadata import TitleMetadata

class Title:
    """
    Represents a media title (movie or TV show) with both metadata and user-specific data

    Stores user-generated attributes (watched, rating, etc.)
        metadata (TitleMetadata): Contains static data like title, genre, release date, etc
        user_data (UserTitleData): Stores user-generated attributes (watched, rating, etc.)
    """
    def __init__(self, data):
        """
        Initializes a Title object from TMDb API data

        Args:
            data (dict): Dictionary containing TMDb API response fields
        """
        release_date = data.get('release_date') or data.get('first_air_date') or 'Unknown'
        self.release_date = (
            extract_year(release_date)
            if release_date != 'Unknown'
            else release_date
            )
        genre_ids = data.get('genre_ids', [])
        self.metadata = TitleMetadata(
            id=data.get('id'),
            title=str(data.get('title') or data.get('name') or 'No title available'),
            media_type=data.get('media_type', 'Unknown'),
            release_date=self.release_date,
            genres=get_genre_names_from_ids(
                genre_ids, data.get('media_type', 'Unknown'))
                if genre_ids
                else [],
            popularity=round(data.get('weighted_popularity', 0), 2),
            overview=data.get('overview', 'No overview available').replace('\n', '')
        )
        self.user_data = UserTitleData()

    def toggle_watched(self, rating=None):
        """
        Toggles watch status of a title
        
        If toggled to "watched", also updates the watched date and optionally sets a rating

        Args:
            rating (int, optional): Rating to assign if marking as watched
        """
        self.user_data.toggle_watched(rating)
    def set_rating(self, rating):
        """
        Set rating for this title
        
        Args:
            rating (int): A rating between 1 and 5.

        Raises:
            ValueError: If the rating is outside the valid range
        """
        self.user_data.set_rating(rating)

    def to_sheet_row(self):
        """
        Converts title object into list format format suitable for Google Sheets

        Returns:
            lists: title metadata and user data as lists
        """
        values = [
            str(self.metadata.id),
            self.metadata.title,
            self.metadata.media_type,
            str(self.metadata.release_date),
            ', '.join(map(str, self.metadata.genres)),
            str(self.metadata.popularity),
            self.metadata.overview,
            str(self.user_data.watched),
            self.user_data.added_date,
            self.user_data.watched_date,
            str(self.user_data.rating)
        ]
        return values

    @classmethod
    def from_sheet_row(cls, row):
        """
        Creates a Title object (including user data) from Google Sheet row
        
        This method reconstructs both metadata and user data, bypassing __init__

        Args:
            row (dict): dictionary representing a row from Google Sheets 
        Returns:
            obj: reconstructed Title object
        """
        metadata = TitleMetadata(
            id=row.get('id'),
            title=row.get('title'),
            media_type=row.get('media_type'),
            release_date=row.get('release_date'),
            genres=[
                g.strip() for g in row.get('genres', '').split(',')
                ] if row.get('genres')
                else [],
            popularity=float(row.get('weighted_popularity', 0)),
            overview=row.get('overview', 'No overview available')
        )

        user_data = UserTitleData.from_dict(row)

        obj = cls.__new__(cls) # Bypass __init__
        obj.metadata = metadata
        obj.user_data = user_data
        return obj
