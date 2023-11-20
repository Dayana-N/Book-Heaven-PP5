from django.urls import path

from . import views

urlpatterns = [
    path('add_review/<str:pk>', views.create_review, name='add-review'),
]