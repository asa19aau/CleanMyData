from django.urls import path
from .views import addCleaner, success

urlpatterns = [
    path('', addCleaner, name='add-cleaner'),
    path('success/', success, name='success'),
]
