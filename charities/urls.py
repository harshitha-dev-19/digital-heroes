from django.urls import path
from . import views

urlpatterns = [
    path('', views.charity_list, name='charity_list'),
    path('select/<int:pk>/', views.select_charity, name='select_charity'),
]