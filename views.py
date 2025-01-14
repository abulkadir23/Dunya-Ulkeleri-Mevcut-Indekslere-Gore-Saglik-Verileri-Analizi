from django.shortcuts import render, redirect
from django.contrib import messages
import psycopg2
from functools import wraps

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Lütfen önce giriş yapın!')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="1234",
                host="localhost"
            )
            cur = conn.cursor()
            
            # Direkt şifre karşılaştırması
            cur.execute("""
                SELECT id, username 
                FROM users 
                WHERE username = %s AND password = %s
            """, (username, password))
            
            user = cur.fetchone()
            
            if user:
                request.session['user_id'] = user[0]
                request.session['username'] = user[1]
                messages.success(request, 'Başarıyla giriş yaptınız!')
                return redirect('user_map')
            else:
                messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
            
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"Hata: {e}")
            messages.error(request, 'Bir hata oluştu.')
            
    return render(request, 'registration/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Şifreler eşleşmiyor!')
            return render(request, 'registration/register.html')
            
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="1234",
                host="localhost"
            )
            cur = conn.cursor()
            
            # Kullanıcı adı kontrolü
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cur.fetchone():
                messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor!')
                return render(request, 'registration/register.html')
            
            # Şifreyi direkt kaydet
            cur.execute("""
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (username, email, password1))
            
            conn.commit()
            messages.success(request, 'Kayıt başarıyla oluşturuldu!')
            
            cur.close()
            conn.close()
            
            return redirect('login')
            
        except Exception as e:
            print(f"Hata: {e}")
            messages.error(request, 'Kayıt sırasında bir hata oluştu.')
            
    return render(request, 'registration/register.html')

@custom_login_required
def user_map_view(request):
    return render(request, 'user_map.html') 