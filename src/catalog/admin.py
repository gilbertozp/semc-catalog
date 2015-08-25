from django.contrib import admin
from catalog.models import Contact, Software, DownloadCount

admin.site.register(Contact)
admin.site.register(Software)
admin.site.register(DownloadCount)

