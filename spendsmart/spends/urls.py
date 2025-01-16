from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_all_spends),
    path('all_spends/', views.view_all_spends, name='main'),
    path('add_spend/', views.add_spend, name="add_spend"),
    path('create_category/', views.create_category, name="create_category"),
    path('control_panel', views.control_panel, name="control_panel"),
]
