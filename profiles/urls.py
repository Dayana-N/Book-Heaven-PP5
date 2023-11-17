from django.urls import path

from . import views

urlpatterns = [
    path('profile/<str:pk>/', views.profile_page, name='profile'),
    path('order_history/<str:pk>/', views.order_history, name='order-history')
]
