from django.urls import path
from .views import addCleaner_view, success_view, preferences_view, help_view

urlpatterns = [
    path('', addCleaner_view, name='add-cleaner'),
    path('success/', success_view, name='success'),
    path('preferences/<int:pk>', preferences_view, name='preferences'),
    path('help/', help_view, name='help')
]   
