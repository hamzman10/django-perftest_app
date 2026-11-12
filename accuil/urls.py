from django.urls import path
from . import views

urlpatterns = [
    path('',views.accuil, name='accuil')
]