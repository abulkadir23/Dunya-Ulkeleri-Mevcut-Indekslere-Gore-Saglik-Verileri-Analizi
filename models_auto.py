# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AverageData(models.Model):
    cost_of_liv = models.FloatField(blank=True, null=True)
    rent_indx = models.FloatField(blank=True, null=True)
    groceries = models.FloatField(blank=True, null=True)
    restaurant = models.FloatField(blank=True, null=True)
    l_purchasing = models.FloatField(blank=True, null=True)
    sunshine = models.FloatField(blank=True, null=True)
    life_exp = models.FloatField(blank=True, null=True)
    pollution = models.FloatField(blank=True, null=True)
    happines = models.FloatField(blank=True, null=True)
    outdoor_actv = models.FloatField(blank=True, null=True)
    number_of_takeout = models.FloatField(blank=True, null=True)
    monthly_gym = models.FloatField(blank=True, null=True)
    cost_of_bootle = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'average_data'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FavoriteCountry(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey('SonVeriler', models.DO_NOTHING, db_column='country', blank=True, null=True)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'favorite_country'


class LoginAttempts(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    attempt_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'login_attempts'


class MapappCountry(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    flag_url = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'mapapp_country'


class MapappFavorite(models.Model):
    id = models.BigAutoField(primary_key=True)
    country_name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mapapp_favorite'
        unique_together = (('user', 'country_name', 'data_type'),)


class PasswordResetTokens(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    token = models.TextField()
    expires_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'password_reset_tokens'


class SonVeriler(models.Model):
    rank_x = models.IntegerField(db_column='Rank_x', blank=True, null=True)  # Field name made lowercase.
    country = models.TextField(db_column='Country', primary_key=True)  # Field name made lowercase.
    cost_of_living_index = models.FloatField(db_column='Cost of Living Index', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rent_index = models.FloatField(db_column='Rent Index', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cost_of_living_plus_rent_index = models.FloatField(db_column='Cost of Living Plus Rent Index', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    groceries_index = models.FloatField(db_column='Groceries Index', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    restaurant_price_index = models.FloatField(db_column='Restaurant Price Index', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    local_purchasing_power_index = models.FloatField(db_column='Local Purchasing Power Index', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    city = models.TextField(db_column='City', blank=True, null=True)  # Field name made lowercase.
    rank_y = models.IntegerField(db_column='Rank_y', blank=True, null=True)  # Field name made lowercase.
    sunshine_hours_city_field = models.FloatField(db_column='Sunshine hours(City)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cost_of_a_bottle_of_water_city_field = models.TextField(db_column='Cost of a bottle of water(City)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    obesity_levels_country_field = models.TextField(db_column='Obesity levels(Country)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    life_expectancy_years_country_field = models.FloatField(db_column='Life expectancy(years) (Country)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    pollution_index_score_city_field = models.FloatField(db_column='Pollution(Index score) (City)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    annual_avg_hours_worked = models.TextField(db_column='Annual avg. hours worked', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    happiness_levels_country_field = models.FloatField(db_column='Happiness levels(Country)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    outdoor_activities_city_field = models.IntegerField(db_column='Outdoor activities(City)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    number_of_take_out_places_city_field = models.IntegerField(db_column='Number of take out places(City)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cost_of_a_monthly_gym_membership_city_field = models.TextField(db_column='Cost of a monthly gym membership(City)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'son_veriler'


class Users(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    password_hash = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
