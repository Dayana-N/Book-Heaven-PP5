from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('faq/', views.faq_page, name='faq-page'),
    path('about/', views.about_page, name='about-page'),
]
