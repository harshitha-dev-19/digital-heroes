from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_score, name='add_score'),
    path('edit/<int:pk>/', views.edit_score, name='edit_score'),
    path('delete/<int:pk>/', views.delete_score, name='delete_score'),
]