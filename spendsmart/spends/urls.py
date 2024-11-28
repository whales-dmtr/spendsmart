from django.urls import path
from . import views

urlpatterns = [
    path('all_spends/', views.view_all_spends),
]
