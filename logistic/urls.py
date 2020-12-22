# myapp's urls.py
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', Welcome, name='index'),
]
