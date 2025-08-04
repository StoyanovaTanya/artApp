from django.contrib import admin

from artwork.models import Artwork


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at',)
    search_fields = ('title', 'description',)
    list_filter = ('created_at', 'owner',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Basic information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Additional data', {
            'fields': ('owner', 'created_at'),
        }),
    )