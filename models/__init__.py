"""
Classes package initializer.

This module exposes core data models
used throughout the ReelTracker CLI application,
including `Title` for media entries
and `UserTitleData` for user-specific metadata
"""
from .title import Title
from .user_data import UserTitleData

__all__ = ['Title', 'UserTitleData']
