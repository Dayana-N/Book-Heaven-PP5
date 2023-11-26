from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin-panel'),
    path('discount_codes/', views.admin_discounts, name='admin-discounts'),
    path('discount_codes_delete/<str:pk>/',
         views.admin_discounts_delete, name='admin-discounts-delete'),
    path('discount_codes_edit/<str:pk>/',
         views.admin_discounts_edit, name='admin-discounts-edit'),
]
