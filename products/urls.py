from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_products, name='all-products'),
    path('product/<str:pk>/', views.product, name='product'),
    path('authors/', views.all_authors, name='authors'),
    path('authors/<str:pk>/', views.author, name='author'),
]
