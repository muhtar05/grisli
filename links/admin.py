from django.contrib import admin
from .models import Link

class LinkAdmin(admin.ModelAdmin):
    list_display = ('url','when')

admin.site.register(Link,LinkAdmin)

