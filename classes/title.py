"""
Title class module
"""
from dataclasses import dataclass
from typing import List
from utils import extract_year
from tmdb import get_genre_names_from_ids
from classes.user_data import UserTitleData


@dataclass
class TitleMetadata:
    id: str
    title: str
    media_type: str
    release_date: str
    genres: List[str]
    popularity: float
    overview: str

class Title:
    """
    Class to contain Title information and methods
    """
    def __init__(self, data):
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
        """creates a Title object (including user data) from Google Sheet row

        Args:
            row (dict): each row is a dictionary 
        Returns:
            obj: Title object including user data
        """
        # create Title instance from main data
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

        # Bypass __init__ to avoid recomputing metadata
        obj = cls.__new__(cls)
        obj.metadata = metadata
        obj.user_data = user_data
        return obj
