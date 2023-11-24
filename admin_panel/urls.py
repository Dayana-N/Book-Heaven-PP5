from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin-panel'),
    path('discount_codes/', views.admin_discounts, name='admin-discounts'),
]
