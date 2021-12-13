from django.urls import path
from .views import frontpage_view, success_view, headerChoice_view, help_view, merge_view


urlpatterns = [
    path('', frontpage_view, name='frontpage'),
    path('success/', success_view, name='success'),
    path('header-choices/<int:pk>', headerChoice_view, name='header-choices'),
    path('help/', help_view, name='help'),
    path('merge/', merge_view, name='merge'),
]   
