from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_cart, name='view-cart'),
    path('add/<item_id>/', views.add_to_cart, name='add-to-cart'),
    path('update_cart/<item_id>/', views.update_cart, name='update-cart'),
]
