from django.contrib import admin
from django.urls import path
from mapapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.map_view, name='map'),
    path('user/map/', views.user_map_view, name='user_map'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/country-data/<str:country_name>/', views.get_country_data, name='get_country_data'),
    path('search-countries/', views.search_countries, name='search_countries'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('check-favorite-status/', views.check_favorite_status, name='check_favorite_status'),
]

