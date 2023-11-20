from django.urls import path

from . import views

urlpatterns = [
    path('my_profile/<str:pk>/', views.profile_page, name='profile'),
    path('profile/<str:pk>/orders/', views.my_orders, name='my-orders'),
    path('order_history/<str:pk>/', views.order_history, name='order-history'),
    path('profile/<str:pk>/wishlist/', views.my_wishlist, name='my-wishlist'),
    path('profile/wishlist_add/<str:pk>/',
         views.wishlist_add, name='wishlist-add'),
]
