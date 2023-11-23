from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_cart, name='view-cart'),
    path('add/<item_id>/', views.add_to_cart, name='add-to-cart'),
    path('update_cart/<item_id>/', views.update_cart, name='update-cart'),
    path('remove_item_cart/<item_id>/',
         views.remove_from_cart, name='remove-item-cart'),
    path('add_discount/', views.add_discount, name='add-discount'),
    path('remove_discount/', views.remove_discount, name='remove-discount'),
]
