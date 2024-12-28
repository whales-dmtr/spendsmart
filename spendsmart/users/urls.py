from django.urls import path
from . import views

urlpatterns = [
    path('register_form/', views.view_register, name='register_form'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.view_profile, name='profile'),
]


