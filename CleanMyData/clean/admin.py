from django.contrib import admin

from .models import File, HeaderPreference, Header

admin.site.register(File)
admin.site.register(HeaderPreference)
admin.site.register(Header)