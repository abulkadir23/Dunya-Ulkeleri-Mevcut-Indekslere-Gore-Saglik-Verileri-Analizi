from django.contrib.auth.models import User
from ..models import Favorite
import logging

logger = logging.getLogger(__name__)

def log_favorite_added(user: User, favorite: Favorite) -> None:
    logger.info(f"User {user.username} added favorite: {favorite.country_name} - {favorite.data_type}")

def log_favorite_removed(user: User, favorite: Favorite) -> None:
    logger.info(f"User {user.username} removed favorite: {favorite.country_name} - {favorite.data_type}")

# Event handler'ları kaydet
from .dispatcher import EventDispatcher
EventDispatcher.register('favorite_added', log_favorite_added)
EventDispatcher.register('favorite_removed', log_favorite_removed) 