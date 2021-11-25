from django.contrib import admin

from .models import File, Preferences, Header

admin.site.register(File)
admin.site.register(Preferences)
admin.site.register(Header)