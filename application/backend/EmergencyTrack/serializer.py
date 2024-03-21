from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from . models import *

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['first_name',
                  'last_name',
                  'email',
                  'user_icon',
                  'password',
                  'account_type']

    def validate_account_type(self, account_type):
        print("account_type: " + str(account_type.account_type))
        if account_type.account_type not in [0, 1]:
            raise serializers.ValidationError("Invalid account type. Has to be 0 (Citizen) or 1 (pending Officer)")

    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(email=clean_data['email'],
                                                 password=clean_data['password'])
        user_obj.first_name = clean_data['first_name']
        user_obj.last_name = clean_data['last_name']
        user_obj.account_type = AccountTypes.objects.get(account_type=clean_data['account_type'])
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        request = self.context.get('request')
        user = authenticate(request=request,
                            username=clean_data['email'],
                            password=clean_data['password'])
        if not user:
            raise ValidationError('User not found or invalid credentials')

        return user


class UsersSerializer(serializers.ModelSerializer):
    account_type_name = serializers.CharField(source='account_type.account_type_name', read_only=True)

    class Meta:
        model = UserModel
        fields = ['user_id',
                  'first_name',
                  'last_name',
                  'email',
                  'email_status',
                  'account_type',
                  'account_type_name',
                  'user_icon',
                  'last_login']


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ['fake_id',
                  'user',
                  'department']


class CountysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countys
        fields = ['county_id',
                  'county_name',
                  'state',
                  'county_population']


class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = ['state_id',
                  'state_name',
                  'state_population']


class CovidSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.county_name', read_only=True)

    class Meta:
        model = CovidCases
        fields = ['dataset_id',
                  'number_of_cases',
                  'report_date',
                  'county',
                  'county_name',
                  'officer']


class DeathSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.county_name', read_only=True)

    class Meta:
        model = Deaths
        fields = ['dataset_id',
                  'number_of_deaths',
                  'cause_of_deaths',
                  'report_date',
                  'county',
                  'county_name',
                  'officer']


class BlockedRoadsSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.county_name', read_only=True)

    class Meta:
        model = BlockedRoads
        fields = ['dataset_id',
                  'road_name',
                  'location_x_coordinate',
                  'location_y_coordinate',
                  'reason',
                  'intersection1',
                  'intersection2',
                  'starting_datetime',
                  'ending_datetime',
                  'informations_for_public',
                  'county',
                  'county_name',
                  'officer']


class SecurityConcernsSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.county_name', read_only=True)

    class Meta:
        model = SecurityConcerns
        fields = ['dataset_id',
                  'location_name',
                  'location_x_coordinate',
                  'location_y_coordinate',
                  'cause_of_concern',
                  'reported_datetime',
                  'instructions_for_public',
                  'concern_is_present',
                  'county',
                  'county_name',
                  'officer']


class WeatherEventsSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.county_name', read_only=True)

    class Meta:
        model = WeatherEvents
        fields = ['dataset_id',
                  'location_name',
                  'location_x_coordinate',
                  'location_y_coordinate',
                  'event_type',
                  'estimated_datetime',
                  'event_radius',
                  'instructions_for_public',
                  'level_of_evacuation',
                  'event_is_active',
                  'county',
                  'county_name',
                  'officer']


class WildfiresSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.county_name', read_only=True)

    class Meta:
        model = Wildfires
        fields = ['dataset_id',
                  'location_name',
                  'location_x_coordinate',
                  'location_y_coordinate',
                  'cause_of_fire',
                  'date_of_fire',
                  'instructions_for_public',
                  'level_of_evacuation',
                  'fire_is_active',
                  'county',
                  'county_name',
                  'officer']


class LocationSerializer(serializers.Serializer):
    department = serializers.CharField()
    dataset_id = serializers.IntegerField()
    location_x_coordinate = serializers.FloatField()
    location_y_coordinate = serializers.FloatField()
    county_name = serializers.CharField(source='county.county_name', read_only=True)


class CountyStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountyStatistics
        fields = ['county_id',
                  'county_name',
                  'state_id',
                  'covid_cases_7_days_per_100k',
                  'deaths_7_days_per_100k',
                  'wildfires',
                  'blocked_roads',
                  'security_concerns',
                  'weather_events']


class StateStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateStatistics
        fields = ['state_id',
                  'state_name',
                  'covid_cases_7_days_per_100k',
                  'deaths_7_days_per_100k',
                  'wildfires',
                  'blocked_roads',
                  'security_concerns',
                  'weather_events']


class CovidCaseStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CovidCaseStatistics
        fields = ['county_id',
                  'county_name',
                  'today_per_100k',
                  'last_7_days_per_100k',
                  'month_per_100k',
                  'year_per_100k',
                  'all_time_per_100k']


class DeathStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeathStatistics
        fields = ['county_id',
                  'county_name',
                  'today_per_100k',
                  'last_7_days_per_100k',
                  'month_per_100k',
                  'year_per_100k',
                  'all_time_per_100k']


class DepartmentSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.county_name', read_only=True)
    department_name = serializers.CharField(source='department_type.department_name', read_only=True)

    class Meta:
        model = Departments
        fields = ['department_id',
                  'county',
                  'county_name',
                  'department_type',
                  'department_name']


class DepartmentAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentAccess
        fields = ['department',
                  'officer']


