from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.plans_view, name='plans'),
    path('subscribe/<str:plan>/', views.subscribe_view, name='subscribe'),
    path('cancel/', views.cancel_view, name='cancel'),
]