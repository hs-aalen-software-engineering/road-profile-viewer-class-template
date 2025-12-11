"""
Database Module for Road Profile Viewer
========================================
This module provides database connectivity, models, and CRUD operations
for persisting road profiles using SQLModel and SQLite.
"""

from road_profile_viewer.database.connection import create_db_and_tables, get_engine, get_session
from road_profile_viewer.database.crud import (
    create_profile,
    delete_profile,
    get_all_profiles,
    get_profile,
    get_profile_by_name,
    update_profile,
)
from road_profile_viewer.database.models import RoadProfileDB

__all__ = [
    "RoadProfileDB",
    "create_db_and_tables",
    "get_engine",
    "get_session",
    "create_profile",
    "get_profile",
    "get_profile_by_name",
    "get_all_profiles",
    "update_profile",
    "delete_profile",
]
