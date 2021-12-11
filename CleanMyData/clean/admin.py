from django.contrib import admin

from .models import Upload, Document, HeaderPreference, Header

admin.site.register(Upload)
admin.site.register(Document)
admin.site.register(HeaderPreference)
admin.site.register(Header)