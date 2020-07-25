from django.urls import path
from . import views

urlpatterns = [
    path('countries', views.countriesCases, name='countriesCases'),
    path('', views.GlobalCovid, name='Global'),
]