# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class AccountTypes(models.Model):
    account_type = models.DecimalField(primary_key=True, max_digits=1, decimal_places=0)
    account_type_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_types'


class BlockedRoads(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    road_name = models.CharField(max_length=30)
    location_x_coordinate = models.DecimalField(max_digits=8, decimal_places=6)
    location_y_coordinate = models.DecimalField(max_digits=9, decimal_places=6)
    reason = models.CharField(max_length=30, blank=True, null=True)
    intersection1 = models.CharField(max_length=30)
    intersection2 = models.CharField(max_length=30)
    starting_datetime = models.DateTimeField()
    ending_datetime = models.DateTimeField()
    informations_for_public = models.CharField(max_length=255, blank=True, null=True)
    county = models.ForeignKey('Countys', models.DO_NOTHING)
    officer = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blocked_roads'


class Countys(models.Model):
    county_id = models.DecimalField(primary_key=True, max_digits=5, decimal_places=0)
    county_name = models.CharField(max_length=22, blank=True, null=True)
    state = models.ForeignKey('States', models.DO_NOTHING, blank=True, null=True)
    county_population = models.DecimalField(max_digits=8, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'countys'


class CountyStatistics(models.Model):
    county_id = models.DecimalField(primary_key=True, max_digits=5, decimal_places=0)
    county_name = models.CharField(max_length=22, db_collation='utf8mb4_0900_ai_ci')
    state_id = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    covid_cases_7_days_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    deaths_7_days_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    wildfires = models.BigIntegerField()
    blocked_roads = models.BigIntegerField()
    security_concerns = models.BigIntegerField()
    weather_events = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'county_statistics'


class CovidCases(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    number_of_cases = models.SmallIntegerField()
    report_date = models.DateField()
    county = models.ForeignKey(Countys, models.DO_NOTHING)
    officer = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'covid_cases'


class CovidCaseStatistics(models.Model):
    county_id = models.DecimalField(primary_key=True, max_digits=5, decimal_places=0)
    county_name = models.CharField(max_length=22, db_collation='utf8mb4_0900_ai_ci')
    today_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    last_7_days_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    month_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    year_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    all_time_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'covid_case_statistics'


class Deaths(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    number_of_deaths = models.SmallIntegerField()
    cause_of_deaths = models.CharField(max_length=30, blank=True, null=True)
    report_date = models.DateField()
    county = models.ForeignKey(Countys, models.DO_NOTHING)
    officer = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deaths'


class DeathStatistics(models.Model):
    county_id = models.DecimalField(primary_key=True, max_digits=5, decimal_places=0)
    county_name = models.CharField(max_length=22, db_collation='utf8mb4_0900_ai_ci')
    today_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    last_7_days_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    month_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    year_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    all_time_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'death_statistics'


class DepartmentAccess(models.Model):
    department = models.OneToOneField('Departments', models.DO_NOTHING, primary_key=True)  # The composite primary key (department_id, officer_id) found, that is not supported. The first column is selected.
    officer = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'department_access'
        unique_together = (('department', 'officer'),)


class Departments(models.Model):
    department_id = models.AutoField(primary_key=True)
    county = models.ForeignKey('Countys', models.DO_NOTHING)
    department_type = models.ForeignKey('DepartmentTypes', models.DO_NOTHING, db_column='department_type')

    class Meta:
        managed = False
        db_table = 'departments'


class DepartmentTypes(models.Model):
    department_type = models.PositiveIntegerField(primary_key=True)
    department_name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department_types'


class SecurityConcerns(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=30)
    location_x_coordinate = models.DecimalField(max_digits=8, decimal_places=6)
    location_y_coordinate = models.DecimalField(max_digits=9, decimal_places=6)
    cause_of_concern = models.CharField(max_length=30)
    reported_datetime = models.DateTimeField(blank=True, null=True)
    instructions_for_public = models.CharField(max_length=255, blank=True, null=True)
    concern_is_present = models.TextField(blank=True, null=True)  # This field type is a guess.
    county = models.ForeignKey(Countys, models.DO_NOTHING)
    officer = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'security_concerns'


class States(models.Model):
    state_id = models.DecimalField(primary_key=True, max_digits=2, decimal_places=0)
    state_name = models.CharField(max_length=13)
    state_population = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'states'


class StateStatistics(models.Model):
    state_id = models.DecimalField(primary_key=True, max_digits=2, decimal_places=0)
    state_name = models.CharField(max_length=13, db_collation='utf8mb4_0900_ai_ci')
    covid_cases_7_days_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    deaths_7_days_per_100k = models.DecimalField(max_digits=35, decimal_places=4, blank=True, null=True)
    wildfires = models.DecimalField(max_digits=42, decimal_places=0, blank=True, null=True)
    blocked_roads = models.DecimalField(max_digits=42, decimal_places=0, blank=True, null=True)
    security_concerns = models.DecimalField(max_digits=42, decimal_places=0, blank=True, null=True)
    weather_events = models.DecimalField(max_digits=42, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'state_statistics'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('An email is required.')
        if not password:
            raise ValueError('A password is required.')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('An email is required.')
        if not password:
            raise ValueError('A password is required.')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length=50, unique=True)
    email_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    account_type = models.ForeignKey('AccountTypes', models.DO_NOTHING, db_column='account_type', blank=True, null=True)
    user_icon = models.CharField(max_length=12, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return str(self.user_id)

    class Meta:
        managed = False
        db_table = 'users'


class WeatherEvents(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=30)
    location_x_coordinate = models.DecimalField(max_digits=8, decimal_places=6)
    location_y_coordinate = models.DecimalField(max_digits=9, decimal_places=6)
    event_type = models.CharField(max_length=30, blank=True, null=True)
    estimated_datetime = models.DateTimeField()
    event_radius = models.PositiveSmallIntegerField(blank=True, null=True)
    instructions_for_public = models.CharField(max_length=255, blank=True, null=True)
    level_of_evacuation = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_is_active = models.TextField(blank=True, null=True)  # This field type is a guess.
    county = models.ForeignKey(Countys, models.DO_NOTHING)
    officer = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather_events'


class Wildfires(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=30)
    location_x_coordinate = models.DecimalField(max_digits=8, decimal_places=6)
    location_y_coordinate = models.DecimalField(max_digits=9, decimal_places=6)
    cause_of_fire = models.CharField(max_length=30, blank=True, null=True)
    date_of_fire = models.DateField()
    instructions_for_public = models.CharField(max_length=255, blank=True, null=True)
    level_of_evacuation = models.TextField(blank=True, null=True)  # This field type is a guess.
    fire_is_active = models.TextField(blank=True, null=True)  # This field type is a guess.
    county = models.ForeignKey(Countys, models.DO_NOTHING)
    officer = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wildfires'


class Subscriptions(models.Model):
    # pretend there is an id field because combined primary keys do not work
    # fake_id = models.AutoField(primary_key=True, db_column=None)

    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_id', primary_key=True)
    department = models.ForeignKey(Departments, models.DO_NOTHING, db_column='department_id')

    class Meta:
        managed = False
        db_table = 'subscriptions'
        unique_together = (('user', 'department'),)
