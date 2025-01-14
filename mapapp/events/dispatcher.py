from typing import Dict, Any, List, Callable
from django.contrib.auth.models import User
from ..models import Favorite

class EventDispatcher:
    _handlers: Dict[str, List[Callable]] = {
        'favorite_added': [],
        'favorite_removed': []
    }

    @classmethod
    def register(cls, event_type: str, handler: Callable) -> None:
        if event_type not in cls._handlers:
            cls._handlers[event_type] = []
        cls._handlers[event_type].append(handler)

    @classmethod
    def dispatch(cls, event_type: str, **kwargs) -> None:
        if event_type in cls._handlers:
            for handler in cls._handlers[event_type]:
                handler(**kwargs) 