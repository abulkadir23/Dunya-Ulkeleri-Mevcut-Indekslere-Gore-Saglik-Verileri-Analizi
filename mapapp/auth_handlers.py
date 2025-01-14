from abc import ABC, abstractmethod
from django.contrib.auth.hashers import check_password
from django.db import connection
import re

class AuthHandler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request, **kwargs):
        if self._next_handler:
            return self._next_handler.handle(request, **kwargs)
        return None

# Giriş işlemleri için handler'lar
class EmptyFieldHandler(AuthHandler):
    def handle(self, request, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        
        if not username or not password:
            return {
                'success': False,
                'message': 'Kullanıcı adı ve şifre alanları boş bırakılamaz!'
            }
        return super().handle(request, **kwargs)

class UserExistenceHandler(AuthHandler):
    def handle(self, request, **kwargs):
        username = kwargs.get('username')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, password FROM users 
                WHERE username = %s
            """, [username])
            user = cursor.fetchone()
            
        if not user:
            return {
                'success': False,
                'message': 'Kullanıcı bulunamadı!'
            }
        
        kwargs['user_id'] = user[0]
        kwargs['stored_password'] = user[1]
        return super().handle(request, **kwargs)

class PasswordVerificationHandler(AuthHandler):
    def handle(self, request, **kwargs):
        password = kwargs.get('password')
        stored_password = kwargs.get('stored_password')
        
        if not check_password(password, stored_password):
            return {
                'success': False,
                'message': 'Şifre hatalı!'
            }
        
        return {
            'success': True,
            'user_id': kwargs.get('user_id'),
            'message': 'Giriş başarılı!'
        }

# Kayıt işlemleri için handler'lar
class RegistrationFieldHandler(AuthHandler):
    def handle(self, request, **kwargs):
        username = kwargs.get('username')
        email = kwargs.get('email')
        password = kwargs.get('password')
        password2 = kwargs.get('password2')
        
        if not all([username, email, password, password2]):
            return {
                'success': False,
                'message': 'Tüm alanlar doldurulmalıdır!'
            }
        return super().handle(request, **kwargs)

class PasswordMatchHandler(AuthHandler):
    def handle(self, request, **kwargs):
        password = kwargs.get('password')
        password2 = kwargs.get('password2')
        
        if password != password2:
            return {
                'success': False,
                'message': 'Şifreler eşleşmiyor!'
            }
        return super().handle(request, **kwargs)

class EmailValidationHandler(AuthHandler):
    def handle(self, request, **kwargs):
        email = kwargs.get('email')
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return {
                'success': False,
                'message': 'Geçerli bir email adresi giriniz!'
            }
        return super().handle(request, **kwargs)

class UniqueUserHandler(AuthHandler):
    def handle(self, request, **kwargs):
        username = kwargs.get('username')
        email = kwargs.get('email')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM users 
                WHERE username = %s OR email = %s
            """, [username, email])
            count = cursor.fetchone()[0]
            
        if count > 0:
            return {
                'success': False,
                'message': 'Bu kullanıcı adı veya email zaten kullanımda!'
            }
        return super().handle(request, **kwargs) 