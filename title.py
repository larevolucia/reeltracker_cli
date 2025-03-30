"""
Title class module
"""
from utils import extract_year
from tmdb import get_genre_names_from_ids
from user_data import UserTitleData


class Title:
    """
    Class to contain Title information and methods
    """
    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title') or data.get('name') or 'No title available'
        self.media_type = data.get('media_type', 'Unknown')
        release_date = data.get('release_date') or data.get('first_air_date') or 'Unknown'
        self.release_date = (
            extract_year(release_date)
            if release_date != 'Unknown'
            else release_date
            )
        genres_ids = data.get('genre_ids', [])
        self.genres = (
            get_genre_names_from_ids(genres_ids, self.media_type)
            if genres_ids
            else genres_ids
            )
        self.popularity = round(data.get('weighted_popularity', 0), 2)
        overview = data.get('overview', 'No overview available').replace('\n', '')
        self.overview = overview
        self.user_data = UserTitleData()

    def toggle_watched(self, rating=None):
        """
        Toggles watch status
        """
        self.user_data.toggle_watched(rating)
    def set_rating(self, rating):
        """
        Edits title rating
        """
        self.user_data.set_rating(rating)

    def to_sheet_row(self):
        """Converts metadata to list format

        Returns:
            lists: title metadata as lists
        """
        values = [
            str(self.id),
            self.title,
            self.media_type,
            str(self.release_date),
            ', '.join(map(str, self.genres)),
            str(self.popularity),
            self.overview,
            str(self.user_data.watched),
            self.user_data.added_date,
            self.user_data.watched_date,
            str(self.user_data.rating)
        ]
        return values

    @classmethod
    def from_sheet_row(cls, row):
        """creates a Title object (including user data) from Google Sheet row

        Args:
            row (dict): each row is a dictionary 
        Returns:
            obj: Title object including user data
        """
        # create Title instance from main data
        obj = cls({
            "id": row.get('id'),
            "title": row.get('title'),
            "media_type": row.get('media_type'),
            "overview": row.get('overview'),
            'weighted_popularity': float(row.get('weighted_popularity', 0))
        })
        # Set non-init data
        obj.release_date = row.get('release_date')
        genres_str = row.get('genres', '')
        obj.genres = [g.strip() for g in genres_str.split(',')] if genres_str else []
        # Rebuild user-related data from sheet row
        obj.user_data = UserTitleData.from_dict(row)
        return obj
