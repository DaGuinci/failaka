from django.contrib import admin

from .models import (
    Item,
    Site,
    Subsite,
    Comment,
    Notable,
    Mission
    )

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'author', 'site')
    search_fields = ('name', 'description')
    list_per_page = 20

admin.site.register(Site)
admin.site.register(Subsite)
admin.site.register(Comment)
admin.site.register(Notable)
admin.site.register(Mission)