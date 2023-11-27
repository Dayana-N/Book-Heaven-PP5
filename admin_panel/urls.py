from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin-panel'),
    path('discount_codes/', views.admin_discounts, name='admin-discounts'),
    path('discount_codes_delete/<str:pk>/',
         views.admin_discounts_delete, name='admin-discounts-delete'),
    path('discount_codes_edit/<str:pk>/',
         views.admin_discounts_edit, name='admin-discounts-edit'),
    path('orders/', views.admin_orders, name='admin-orders'),
    path('orders_edit/<str:pk>/', views.admin_orders_edit,
         name='admin-orders-edit'),
    path('add_product/', views.admin_add_product,
         name='admin-add-product'),
    path('edit_product/<str:pk>/', views.admin_edit_product,
         name='admin-edit-product'),
    path('delete_product/<str:pk>/', views.admin_delete_product,
         name='admin-delete-product'),
]
