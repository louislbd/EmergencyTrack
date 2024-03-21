# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BlockedRoads(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    road_name = models.CharField(max_length=30)
    location_x_coordinate = models.PositiveSmallIntegerField()
    location_y_coordinate = models.PositiveSmallIntegerField()
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


class CovidCases(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    number_of_cases = models.SmallIntegerField()
    report_date = models.DateField()
    county = models.ForeignKey(Countys, models.DO_NOTHING)
    officer = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'covid_cases'


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


class DepartmentAccess(models.Model):
    department = models.OneToOneField('Departments', models.DO_NOTHING, primary_key=True)  # The composite primary key (department_id, officer_id) found, that is not supported. The first column is selected.
    officer = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'department_access'
        unique_together = (('department', 'officer'),)


class Departments(models.Model):
    department_id = models.AutoField(primary_key=True)
    county = models.ForeignKey(Countys, models.DO_NOTHING)
    department_type = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'departments'


class SecurityConcerns(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=30)
    location_x_coordinate = models.PositiveSmallIntegerField()
    location_y_coordinate = models.PositiveSmallIntegerField()
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


class Subscriptions(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, department_id) found, that is not supported. The first column is selected.
    department = models.ForeignKey(Departments, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'subscriptions'
        unique_together = (('user', 'department'),)


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.CharField(max_length=50)
    email_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    password = models.CharField(max_length=128)
    account_type = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    user_icon = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'users'


class WeatherEvents(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=30)
    location_x_coordinate = models.PositiveSmallIntegerField()
    location_y_coordinate = models.PositiveSmallIntegerField()
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
    location_x_coordinate = models.PositiveSmallIntegerField()
    location_y_coordinate = models.PositiveSmallIntegerField()
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
