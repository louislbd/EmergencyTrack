"""
URL configuration for EmergencyTrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from . views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('about.urls')),
    path('', include('searchvp.urls')),
    path('api/register', UserRegister.as_view(), name='register'),
    path('api/login', UserLogin.as_view(), name='login'),
    path('api/logout', UserLogout.as_view(), name='logout'),
    path('api/user', UserApiView.as_view(), name='user'),
    path('api/users', UsersAdminApiView.as_view()),
    path('api/users/<str:id>', UsersAdminDetailApiView.as_view()),
    path('api/pending_officers', PendingOfficersApiView.as_view()),
    path('api/subscription', SubscriptionApiView.as_view()),
    path('api/countys', CountysApiView.as_view()),
    path('api/departments', DepartmentsApiView.as_view()),
    path('api/departments/<int:id>', DepartmentsDetailApiView.as_view()),
    path('api/covid_cases', CovidApiView.as_view()),
    path('api/covid_cases/<int:id>', CovidDetailApiView.as_view()),
    path('api/covid_case_stats', CovidCaseStatisticsApiView.as_view()),
    path('api/covid_case_stats/<str:name>', CovidCaseStatisticsDetailApiView.as_view()),
    path('api/deaths', DeathApiView.as_view()),
    path('api/deaths/<int:id>', DeathDetailApiView.as_view()),
    path('api/death_stats', DeathStatisticsApiView.as_view()),
    path('api/death_stats/<str:name>', DeathStatisticsDetailApiView.as_view()),
    path('api/county_statistics', CountyStatisticsApiView.as_view()),
    path('api/county_statistics/<str:name>', CountyStatisticsDetailApiView.as_view()),
    path('api/state_statistics', StateStatisticsApiView.as_view()),
    path('api/state_statistics/<int:state_id>', StateStatisticsDetailApiView.as_view()),
    path('api/blocked_roads', BlockedRoadsApiView.as_view()),
    path('api/blocked_roads/<int:id>', BlockedRoadsDetailApiView.as_view()),
    path('api/security_concerns', SecurityConcernsApiView.as_view()),
    path('api/security_concerns/<int:id>', SecurityConcernsDetailApiView.as_view()),
    path('api/weather_events', WeatherEventsApiView.as_view()),
    path('api/weather_events/<int:id>', WeatherEventsDetailApiView.as_view()),
    path('api/wildfires', WildfiresApiView.as_view()),
    path('api/wildfires/<int:id>', WildfiresDetailApiView.as_view()),
    path('api/locations/', LocationsApiView.as_view())
]
