from django.urls import path
from . import views

urlpatterns = [
    path('Country', views.PHCovid, name='PH'),
    path('Country/<int:pk>/', views.PHCovid, name='PH'),
    path('', views.GlobalCovid, name='Global'),
]