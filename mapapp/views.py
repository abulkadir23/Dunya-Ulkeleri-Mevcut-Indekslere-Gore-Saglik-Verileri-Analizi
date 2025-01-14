from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from .models import Favorite
from .services.favorite_service import FavoriteService
import json
from django.shortcuts import render
from .models import CountryData
from django.db.models import Q
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend

from .map_singleton import WorldMapSingleton 
from .auth_handlers import (
    EmptyFieldHandler, UserExistenceHandler, PasswordVerificationHandler,
    RegistrationFieldHandler, PasswordMatchHandler, EmailValidationHandler,
    UniqueUserHandler
)

logger = logging.getLogger(__name__)

favorite_service = FavoriteService()

def map_view(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM son_veriler
                WHERE "Country" = 'Turkey'
            """)
            
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            
            if row:
                country_data = dict(zip(columns, row))
                context = {
                    'country_data': {
                        'City': country_data['City'],
                        'rank_x': country_data['Rank_x'],
                        'sunshine_hours': country_data['Sunshine hours(City)'],
                        'life_expectancy': country_data['Life expectancy(years) (Country)'],
                        'pollution_index': country_data['Pollution(Index score) (City)'],
                        'happiness_levels': country_data['Happiness levels(Country)'],
                        'outdoor_activities': country_data['Outdoor activities(City)'],
                        'takeout_places': country_data['Number of take out places(City)'],
                        'cost_living_index': country_data['Cost of Living Index'],
                        'rent_index': country_data['Rent Index'],
                        'cost_living_rent_index': country_data['Cost of Living Plus Rent Index'],
                        'groceries_index': country_data['Groceries Index'],
                        'restaurant_price_index': country_data['Restaurant Price Index'],
                        'local_purchasing_power': country_data['Local Purchasing Power Index'],
                        'rank_y': country_data['Rank_y'],
                        'obesity_levels': country_data['Obesity levels(Country)'],
                        'annual_hours_worked': country_data['Annual avg. hours worked'],
                        'gym_membership_cost': country_data['Cost of a monthly gym membership(City)'],
                        'water_bottle_cost': country_data['Cost of a bottle of water(City)']
                    }
                }
            else:
                context = {'country_data': {}}
    except Exception as e:
        print(f"Hata: {str(e)}")
        context = {'country_data': {}}
    
    if request.user.is_authenticated:
        return redirect('user_map')
    return render(request, 'map.html', context)

@login_required
def user_map_view(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM son_veriler
                WHERE "Country" = 'Turkey'
            """)
            
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            
            if row:
                country_data = dict(zip(columns, row))
                context = {
                    'country_data': {
                        'City': country_data['City'],
                        'rank_x': country_data['Rank_x'],
                        'sunshine_hours': country_data['Sunshine hours(City)'],
                        'life_expectancy': country_data['Life expectancy(years) (Country)'],
                        'pollution_index': country_data['Pollution(Index score) (City)'],
                        'happiness_levels': country_data['Happiness levels(Country)'],
                        'outdoor_activities': country_data['Outdoor activities(City)'],
                        'takeout_places': country_data['Number of take out places(City)'],
                        'cost_living_index': country_data['Cost of Living Index'],
                        'rent_index': country_data['Rent Index'],
                        'cost_living_rent_index': country_data['Cost of Living Plus Rent Index'],
                        'groceries_index': country_data['Groceries Index'],
                        'restaurant_price_index': country_data['Restaurant Price Index'],
                        'local_purchasing_power': country_data['Local Purchasing Power Index'],
                        'rank_y': country_data['Rank_y'],
                        'obesity_levels': country_data['Obesity levels(Country)'],
                        'annual_hours_worked': country_data['Annual avg. hours worked'],
                        'gym_membership_cost': country_data['Cost of a monthly gym membership(City)'],
                        'water_bottle_cost': country_data['Cost of a bottle of water(City)']
                    }
                }
            else:
                context = {'country_data': {}}
    except Exception as e:
        print(f"Hata: {str(e)}")
        context = {'country_data': {}}
    
    return render(request, 'user_map.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Chain of Responsibility pattern'i uygula
        field_handler = RegistrationFieldHandler()
        password_match_handler = PasswordMatchHandler()
        email_handler = EmailValidationHandler()
        unique_handler = UniqueUserHandler()
        
        # Handler'ları zincirle
        field_handler.set_next(password_match_handler)\
            .set_next(email_handler)\
            .set_next(unique_handler)
        
        # İşlemi başlat
        result = field_handler.handle(request,
            username=username,
            email=email,
            password=password,
            password2=password2
        )
        
        if result['success']:
            try:
                with connection.cursor() as cursor:
                    hashed_password = make_password(password)
                    cursor.execute("""
                        INSERT INTO users (username, email, password)
                        VALUES (%s, %s, %s)
                    """, [username, email, hashed_password])
                    connection.commit()
                    
                messages.success(request, 'Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
                return redirect('login')
            except Exception as e:
                messages.error(request, 'Kayıt sırasında bir hata oluştu!')
                return redirect('register')
        else:
            messages.error(request, result['message'])
            
    return render(request, 'registration/register.html')

@csrf_exempt
def toggle_favorite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            country_name = data.get('country_name')
            
            logger.info(f"Favori toggle isteği: Kullanıcı {user_id}, Ülke {country_name}")
            
            with connection.cursor() as cursor:
                # Önce favorilerde var mı kontrol et
                cursor.execute("""
                    SELECT id FROM favorite_countries 
                    WHERE user_id = %s AND country_name = %s
                """, [user_id, country_name])
                
                existing = cursor.fetchone()
                
                if existing:
                    cursor.execute("""
                        DELETE FROM favorite_countries 
                        WHERE user_id = %s AND country_name = %s
                    """, [user_id, country_name])
                    action = "removed"
                else:
                    cursor.execute("""
                        INSERT INTO favorite_countries (user_id, country_name)
                        VALUES (%s, %s)
                    """, [user_id, country_name])
                    action = "added"
                
                connection.commit()
                
                return JsonResponse({
                    'status': 'success',
                    'action': action,
                    'message': f"Ülke favorilerden {'kaldırıldı' if action == 'removed' else 'eklendi'}"
                })
                
        except Exception as e:
            logger.error(f"Favori işlemi hatası: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def get_favorites(request, user_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT country_name FROM favorite_countries 
                WHERE user_id = %s
                ORDER BY added_at DESC
            """, [user_id])
            
            favorites = [row[0] for row in cursor.fetchall()]
            
            return JsonResponse({
                'status': 'success',
                'favorites': favorites
            })
            
    except Exception as e:
        logger.error(f"Favori listesi hatası: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def clean_numeric_value(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    # Stringse ve % işareti içeriyorsa
    if isinstance(value, str):
        # % işaretini kaldır ve float'a çevir
        value = value.replace('%', '').strip()
        try:
            return float(value)
        except ValueError:
            return None
    return None

@csrf_exempt
def get_country_data(request, country_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM son_veriler
                WHERE "Country" = %s
            """, [country_name])
            
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            
            if row:
                country_data = dict(zip(columns, row))
                data = {
                    'City': country_data['City'],
                    'rank_x': country_data['Rank_x'],
                    'sunshine_hours': country_data['Sunshine hours(City)'],
                    'life_expectancy': country_data['Life expectancy(years) (Country)'],
                    'pollution_index': country_data['Pollution(Index score) (City)'],
                    'happiness_levels': country_data['Happiness levels(Country)'],
                    'outdoor_activities': country_data['Outdoor activities(City)'],
                    'takeout_places': country_data['Number of take out places(City)'],
                    'cost_living_index': country_data['Cost of Living Index'],
                    'rent_index': country_data['Rent Index'],
                    'cost_living_rent_index': country_data['Cost of Living Plus Rent Index'],
                    'groceries_index': country_data['Groceries Index'],
                    'restaurant_price_index': country_data['Restaurant Price Index'],
                    'local_purchasing_power': country_data['Local Purchasing Power Index'],
                    'rank_y': country_data['Rank_y'],
                    'obesity_levels': country_data['Obesity levels(Country)'],
                    'annual_hours_worked': country_data['Annual avg. hours worked'],
                    'gym_membership_cost': country_data['Cost of a monthly gym membership(City)'],
                    'water_bottle_cost': country_data['Cost of a bottle of water(City)']
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Country not found'}, status=404)
                
    except Exception as e:
        print(f"Ülke verisi getirme hatası: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def search_countries(request):
    search_term = request.GET.get('term', '')
    if search_term:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT "Country"
                    FROM son_veriler
                    WHERE "Country" ILIKE %s
                    LIMIT 10
                """, [f'%{search_term}%'])
                
                countries = [row[0] for row in cursor.fetchall()]
                return JsonResponse(countries, safe=False)
                
        except Exception as e:
            print(f"Ülke arama hatası: {str(e)}")
            return JsonResponse([], safe=False)
            
    return JsonResponse([], safe=False)

@login_required
def favorites_view(request):
    try:
        user_id = request.user.id
        favorites_data = []
        
        with connection.cursor() as cursor:
            # Önce favori ülkeleri al
            cursor.execute("""
                SELECT fc.country_name, fc.added_at, cd.*
                FROM favorite_countries fc
                LEFT JOIN son_veriler cd ON fc.country_name = cd."Country"
                WHERE fc.user_id = %s
                ORDER BY fc.added_at DESC
            """, [user_id])
            
            columns = [col[0] for col in cursor.description]
            favorite_countries = cursor.fetchall()
            
            for row in favorite_countries:
                country_data = dict(zip(columns, row))
                favorites_data.append({
                    'country_name': country_data['country_name'],
                    'data': {
                        'City': country_data['City'],
                        'rank_x': country_data['Rank_x'],
                        'sunshine_hours': country_data['Sunshine hours(City)'],  # Sütun adını düzelttik
                        'life_expectancy': country_data['Life expectancy(years) (Country)'],
                        'pollution_index': country_data['Pollution(Index score) (City)'],
                        'happiness_levels': country_data['Happiness levels(Country)'],
                        'outdoor_activities': country_data['Outdoor activities(City)'],
                        'takeout_places': country_data['Number of take out places(City)'],
                        'cost_living_index': country_data['Cost of Living Index'],
                        'rent_index': country_data['Rent Index'],
                        'cost_living_rent_index': country_data['Cost of Living Plus Rent Index'],
                        'groceries_index': country_data['Groceries Index'],
                        'restaurant_price_index': country_data['Restaurant Price Index'],
                        'local_purchasing_power': country_data['Local Purchasing Power Index'],
                        'rank_y': country_data['Rank_y'],
                        'obesity_levels': country_data['Obesity levels(Country)'],
                        'annual_hours_worked': country_data['Annual avg. hours worked'],
                        'gym_membership_cost': country_data['Cost of a monthly gym membership(City)'],
                        'water_bottle_cost': country_data['Cost of a bottle of water(City)']
                    }
                })
        
        context = {
            'favorites': favorites_data,
            'user': request.user
        }
        
        return render(request, 'favorites.html', context)
        
    except Exception as e:
        print(f"Kritik hata: {str(e)}")
        print(f"Hata türü: {type(e)}")
        import traceback
        print(f"Hata detayı:\n{traceback.format_exc()}")
        messages.error(request, f'Favoriler yüklenirken bir hata oluştu: {str(e)}')
        return redirect('user_map')

def save_favorites(request):
    if request.method == 'POST':
        try:
            # Favori kaydetme işlemleri
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# Özel authentication backend oluşturalım
class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, username, password 
                    FROM users 
                    WHERE username = %s
                """, [username])
                user_data = cursor.fetchone()
                
                if user_data and check_password(password, user_data[2]):
                    try:
                        user = User.objects.get(username=username)
                    except User.DoesNotExist:
                        user = User(
                            id=user_data[0],
                            username=user_data[1],
                            is_active=True
                        )
                        user.save()
                    return user
        except Exception as e:
            print(f"Authentication hatası: {str(e)}")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Chain of Responsibility pattern'i uygula
        empty_handler = EmptyFieldHandler()
        existence_handler = UserExistenceHandler()
        password_handler = PasswordVerificationHandler()
        
        # Handler'ları zincirle
        empty_handler.set_next(existence_handler).set_next(password_handler)
        
        # İşlemi başlat
        result = empty_handler.handle(request, 
            username=username, 
            password=password
        )
        
        if result['success']:
            # CustomAuthBackend örneği oluştur
            auth_backend = CustomAuthBackend()
            user = auth_backend.authenticate(request, username=username, password=password)
            
            if user:
                auth_login(request, user, backend='mapapp.views.CustomAuthBackend')
                return redirect('user_map')
        else:
            messages.error(request, result['message'])
            
    return render(request, 'registration/login.html')

@csrf_exempt
@login_required
def add_to_favorites(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            country_name = data.get('country_name')
            
            if not country_name:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Ülke adı gerekli!'
                }, status=400)

            user_id = request.user.id
            
            with connection.cursor() as cursor:
                # Önce bu ülkenin favorilerde olup olmadığını kontrol et
                cursor.execute("""
                    SELECT id FROM favorite_countries 
                    WHERE user_id = %s AND country_name = %s
                """, [user_id, country_name])
                
                existing = cursor.fetchone()
                
                if existing:
                    # Favorilerden kaldır
                    cursor.execute("""
                        DELETE FROM favorite_countries 
                        WHERE user_id = %s AND country_name = %s
                    """, [user_id, country_name])
                    
                    connection.commit()
                    
                    # Kalan aktif favori sayısını hesapla
                    cursor.execute("""
                        SELECT COUNT(*) FROM favorite_countries 
                        WHERE user_id = %s
                    """, [user_id])
                    current_count = cursor.fetchone()[0]
                    remaining_slots = 5 - current_count
                    
                    return JsonResponse({
                        'status': 'removed',
                        'message': f'Ülke favorilerden kaldırıldı. {remaining_slots} favori hakkınız var.',
                        'remaining_favorites': remaining_slots
                    })
                else:
                    # Mevcut favori sayısını kontrol et
                    cursor.execute("""
                        SELECT COUNT(*) FROM favorite_countries 
                        WHERE user_id = %s
                    """, [user_id])
                    current_count = cursor.fetchone()[0]
                    
                    if current_count >= 5:
                        return JsonResponse({
                            'status': 'error',
                            'message': 'En fazla 5 aktif favoriniz olabilir. Önce bazı favorileri kaldırın.'
                        }, status=400)
                    
                    # Favorilere ekle
                    cursor.execute("""
                        INSERT INTO favorite_countries (user_id, country_name, added_at)
                        VALUES (%s, %s, CURRENT_TIMESTAMP)
                    """, [user_id, country_name])
                    
                    connection.commit()
                    
                    # Kalan favori hakkını hesapla
                    remaining_slots = 4 - current_count  # Yeni eklenen dahil
                    
                    return JsonResponse({
                        'status': 'success',
                        'message': f'Ülke favorilere eklendi! {remaining_slots} favori hakkınız kaldı.',
                        'remaining_favorites': remaining_slots
                    })
                
        except json.JSONDecodeError as e:
            print(f"JSON decode hatası: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Geçersiz JSON verisi'
            }, status=400)
        except Exception as e:
            print(f"Genel hata: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Geçersiz istek metodu'
    }, status=400)

@csrf_exempt
@login_required
def check_favorite_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            country_name = data.get('country_name')
            user_id = request.user.id

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS(
                        SELECT 1 FROM favorite_countries 
                        WHERE user_id = %s AND country_name = %s
                    )
                """, [user_id, country_name])
                
                is_favorite = cursor.fetchone()[0]
                
                return JsonResponse({
                    'is_favorite': is_favorite
                })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Geçersiz istek metodu'
    }, status=400)

@login_required
@require_http_methods(["GET"])
def get_map_data(request):
    map_instance = WorldMapSingleton()
    return JsonResponse(map_instance.get_all_visited_countries())

@login_required
@require_http_methods(["POST"])
def update_country_visit(request):
    country_code = request.POST.get('country_code')
    visit_data = {
        'country_name': request.POST.get('country_name'),
        'visited': request.POST.get('visited', False),
        'notes': request.POST.get('notes', ''),
        'visit_date': request.POST.get('visit_date')
    }
    
    map_instance = WorldMapSingleton()
    map_instance.update_country_data(country_code, visit_data)
    
    return JsonResponse({'status': 'success'})