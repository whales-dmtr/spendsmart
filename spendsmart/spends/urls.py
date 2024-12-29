from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_all_spends),
    path('all_spends/', views.view_all_spends, name='main'),
    path('add_spend_form/', views.view_form_add_spend, name='form_add_spend'),
    path('add_spend', views.add_spend, name="add_spend")
]
