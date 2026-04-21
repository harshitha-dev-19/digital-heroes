from django.urls import path
from . import views

urlpatterns = [
    path('', views.draw_list, name='draw_list'),
    path('<int:pk>/', views.draw_detail, name='draw_detail'),
    path('proof/<int:winner_id>/', views.upload_proof, name='upload_proof'),
    path('admin/draws/', views.admin_draws, name='admin_draws'),
    path('admin/draws/create/', views.create_draw, name='create_draw'),
    path('admin/draws/simulate/<int:pk>/', views.simulate_draw, name='simulate_draw'),
    path('admin/draws/publish/<int:pk>/', views.publish_draw, name='publish_draw'),
    path('admin/winners/', views.verify_winners, name='verify_winners'),
    path('admin/winners/approve/<int:winner_id>/', views.approve_winner, name='approve_winner'),
    path('admin/winners/reject/<int:winner_id>/', views.reject_winner, name='reject_winner'),
    path('admin/winners/paid/<int:winner_id>/', views.mark_paid, name='mark_paid'),
]