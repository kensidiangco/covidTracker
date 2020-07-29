from django.urls import path
from . import views

urlpatterns = [
    path('', views.GlobalCovid, name='Global'),
    path('Country/<int:id>/', views.countryCases, name='Country'),
]