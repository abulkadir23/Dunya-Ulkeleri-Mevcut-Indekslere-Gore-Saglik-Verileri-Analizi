from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/countries/', views.get_country_data, name='get_country_data'),
    path('api/add_country_favorite/', views.add_country_favorite, name='add_country_favorite'),
] 