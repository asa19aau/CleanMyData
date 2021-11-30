from django.urls import path
from .views import frontpage_view, success_view, headerChoice_view, headerDefinition_view, help_view


urlpatterns = [
    path('', frontpage_view, name='frontpage'),
    path('success/', success_view, name='success'),
    path('header-choices/<int:pk>', headerChoice_view, name='header-choices'),
    path('header-choices/<int:pk>/definitions', headerDefinition_view, name='header-definitions'),
    path('help/', help_view, name='help'),
]   
