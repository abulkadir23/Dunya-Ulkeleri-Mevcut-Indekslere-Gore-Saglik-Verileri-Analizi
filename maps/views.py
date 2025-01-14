from django.shortcuts import render
from django.http import JsonResponse
from .models import CountryData
from django.views.decorators.csrf import csrf_protect
import json

def index(request):
    return render(request, 'maps/index.html')

def get_country_data(request):
    countries = CountryData.objects.all()
    data = []
    for country in countries:
        data.append({
            'country_name': country.country,
            'life_expectancy': float(country.life_expectancy) if country.life_expectancy else None,
            'happiness_level': float(country.happiness_level) if country.happiness_level else None,
            'cost_of_living': float(country.cost_of_living) if country.cost_of_living else None,
            'purchasing_power': float(country.purchasing_power) if country.purchasing_power else None,
        })
    return JsonResponse({'countries': data})

@csrf_protect
def add_country_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        country_name = data.get('country_name')
        # Burada favorilere ekleme işlemini yapabilirsiniz
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400) 