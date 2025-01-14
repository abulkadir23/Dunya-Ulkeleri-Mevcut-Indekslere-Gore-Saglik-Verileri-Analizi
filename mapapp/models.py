# mapapp/models.py
from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    name = models.CharField(max_length=100)
    population = models.BigIntegerField()
    area = models.FloatField()
    capital = models.CharField(max_length=100)
    currency = models.CharField(max_length=50)
    language = models.CharField(max_length=100)
    gdp = models.FloatField()
    timezone = models.CharField(max_length=50)
    internet_domain = models.CharField(max_length=10)
    calling_code = models.CharField(max_length=10)
    climate = models.CharField(max_length=100)
    flag_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country_name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'country_name', 'data_type')

    def __str__(self):
        return f"{self.user.username} - {self.country_name} - {self.data_type}"

class CountryData(models.Model):
    class Meta:
        managed = False
        db_table = 'son_veriler'
        
    Country = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Rank_x = models.FloatField(null=True, blank=True)
    sunshine_hours = models.FloatField(db_column='Sunshine hours(City)', null=True, blank=True)
    life_expectancy = models.FloatField(db_column='Life expectancy(years) (Country)', null=True, blank=True)
    pollution_index = models.FloatField(db_column='Pollution(Index score) (City)', null=True, blank=True)
    happiness_levels = models.FloatField(db_column='Happiness levels(Country)', null=True, blank=True)
    outdoor_activities = models.IntegerField(db_column='Outdoor activities(City)', null=True, blank=True)
    takeout_places = models.IntegerField(db_column='Number of take out places(City)', null=True, blank=True)
    cost_living_index = models.FloatField(db_column='Cost of Living Index', null=True, blank=True)
    rent_index = models.FloatField(db_column='Rent Index', null=True, blank=True)
    cost_living_rent_index = models.FloatField(db_column='Cost of Living Plus Rent Index', null=True, blank=True)
    groceries_index = models.FloatField(db_column='Groceries Index', null=True, blank=True)
    restaurant_price_index = models.FloatField(db_column='Restaurant Price Index', null=True, blank=True)
    local_purchasing_power = models.FloatField(db_column='Local Purchasing Power Index', null=True, blank=True)
    Rank_y = models.FloatField(null=True, blank=True)
    obesity_levels = models.FloatField(db_column='Obesity levels(Country)', null=True, blank=True)
    annual_hours_worked = models.FloatField(db_column='Annual avg. hours worked', null=True, blank=True)
    gym_membership_cost = models.FloatField(db_column='Cost of a monthly gym membership(City)', null=True, blank=True)
    water_bottle_cost = models.FloatField(db_column='Cost of a bottle of water(City)', null=True, blank=True)

    def __str__(self):
        return f"{self.Country} - {self.City}"

class CustomUser(models.Model):
    class Meta:
        db_table = 'users'
        managed = False
        
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class FavoriteCountry(models.Model):
    class Meta:
        db_table = 'favorite_countries'
        unique_together = ('user_id', 'country_name')
        
    user_id = models.IntegerField()
    country_name = models.CharField(max_length=100)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.country_name}"