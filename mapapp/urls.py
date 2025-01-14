from django.urls import path
from . import views

urlpatterns = [
    path('api/map-data/', views.get_map_data, name='map_data'),
    path('api/update-country/', views.update_country_visit, name='update_country'),
    path('', views.map_view, name='map'),
    path('kayitol/', views.kayitol, name='kayitol'),
    path('register/', views.register, name='register'),
    path('table/', views.country_table, name='country_table'),
]
