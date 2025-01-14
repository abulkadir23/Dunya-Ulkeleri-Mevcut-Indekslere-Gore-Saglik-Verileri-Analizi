from typing import List, Optional
from django.contrib.auth.models import User
from ..models import Favorite

class FavoriteRepository:
    @staticmethod
    def get_user_favorites(user: User) -> List[Favorite]:
        return Favorite.objects.filter(user=user).order_by('-created_at')
    
    @staticmethod
    def get_favorite(user: User, country_name: str, data_type: str) -> Optional[Favorite]:
        try:
            return Favorite.objects.get(
                user=user,
                country_name=country_name,
                data_type=data_type
            )
        except Favorite.DoesNotExist:
            return None
    
    @staticmethod
    def create_favorite(user: User, country_name: str, data_type: str, value: str) -> Favorite:
        return Favorite.objects.create(
            user=user,
            country_name=country_name,
            data_type=data_type,
            value=value
        )
    
    @staticmethod
    def delete_favorite(favorite: Favorite) -> None:
        favorite.delete()
    
    @staticmethod
    def delete_all_user_favorites(user: User) -> None:
        Favorite.objects.filter(user=user).delete() 