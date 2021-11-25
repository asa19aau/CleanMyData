from django.urls import path
from .views import frontpage_view, success_view, preferences_view, headerChoice_view, help_view


urlpatterns = [
    path('', frontpage_view, name='frontpage'),
    path('success/', success_view, name='success'),
    path('preferences/<int:pk>', preferences_view, name='preferences'), 
    path('header-choices/<int:pk>', headerChoice_view, name='header-choices'),
    path('help/', help_view, name='help'),
]   
