from django.urls import path
from .views import about, louis, roy, sungjun, antoine

urlpatterns = [
    path('about', about),
    path('about/louis', louis),
    path('about/roy', roy),
    path('about/sungjun', sungjun),
    path('about/antoine', antoine),
]
