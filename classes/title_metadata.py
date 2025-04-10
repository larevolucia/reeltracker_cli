"""
Title metadata dataclass definition

This module defines the `TitleMetadata` dataclass, which stores the static metadata
about a movie or TV show (e.g., title, release year, genre, popularity)
It is used by the `Title` class to encapsulate media-specific attributes, 
separate from user-generated data
"""
from dataclasses import dataclass
from typing import List

@dataclass
class TitleMetadata:
    """
    Data structure to hold metadata for a media title (movie or TV show)

    Attributes:
        id (str): Unique identifier for the title (usually from TMDb)
        title (str): Human-readable title of the media
        media_type (str): Type of media ('movie' or 'tv')
        release_date (str): Year of release
        genres (List[str]): List of genre names associated with the title
        popularity (float): Weighted popularity score for sorting or ranking
        overview (str): Short description or synopsis of the title
    """
    id: str
    title: str
    media_type: str
    release_date: str
    genres: List[str]
    popularity: float
    overview: str
