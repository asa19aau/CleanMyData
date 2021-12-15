from django.urls import path
from .views import frontpage_view, merge_documents_view, success_view, headerChoice_view, help_view, merge_view, download_view


urlpatterns = [
    path('', frontpage_view, name='frontpage'),
    path('success/', success_view, name='success'),
    path('header-choices/<int:pk>', headerChoice_view, name='header-choices'),
    path('help/', help_view, name='help'),
    path('merge/', merge_view, name='merge'),
    path('merge/documents/<int:pk>', merge_documents_view, name='merge-documents'), #pk refers to "master" document in upload
    path('document/download/<int:pk>', download_view, name='download-document')
]   
