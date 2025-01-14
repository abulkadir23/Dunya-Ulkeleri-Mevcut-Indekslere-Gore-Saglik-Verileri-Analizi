from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('your_app_name.urls')),  # your_app_name yerine uygulamanızın adını yazın
] 