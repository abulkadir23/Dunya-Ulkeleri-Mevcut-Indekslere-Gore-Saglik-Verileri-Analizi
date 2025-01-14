from typing import List, Dict, Any
from django.contrib.auth.models import User
from ..repositories.favorite_repository import FavoriteRepository
from ..events.dispatcher import EventDispatcher
from ..models import Favorite

class FavoriteService:
    def __init__(self):
        self.repository = FavoriteRepository()
        self.event_dispatcher = EventDispatcher()

    def get_user_favorites(self, user: User) -> List[Dict[str, Any]]:
        favorites = self.repository.get_user_favorites(user)
        return [self._format_favorite(favorite) for favorite in favorites]

    def toggle_favorite(self, user: User, country_name: str, data_type: str, value: str) -> Dict[str, str]:
        favorite = self.repository.get_favorite(user, country_name, data_type)
        
        if favorite:
            self.repository.delete_favorite(favorite)
            self.event_dispatcher.dispatch('favorite_removed', user=user, favorite=favorite)
            return {'status': 'removed'}
        else:
            new_favorite = self.repository.create_favorite(user, country_name, data_type, value)
            self.event_dispatcher.dispatch('favorite_added', user=user, favorite=new_favorite)
            return {'status': 'added'}

    def _format_favorite(self, favorite: Favorite) -> Dict[str, Any]:
        return {
            'country_name': favorite.country_name,
            'data_type': favorite.data_type,
            'value': favorite.value,
            'created_at': favorite.created_at
        } 

    def save_favorites(self, user: User, favorites_data: List[Dict]) -> Dict[str, str]:
        try:
            # Önce kullanıcının tüm favorilerini temizle
            self.repository.delete_all_user_favorites(user)
            
            # Yeni favorileri ekle
            for fav in favorites_data:
                self.repository.create_favorite(
                    user=user,
                    country_name=fav['country_name'],
                    data_type=fav['data_type'],
                    value=fav['value']
                )
            
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)} 