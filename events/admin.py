from django.contrib import admin

from events.models import Event


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'created_by')
    search_fields = ('title', 'description', 'location')
    list_filter = ('date', 'location',)
    ordering = ('date',)
    readonly_fields = ('created_by',)

    fieldsets = (
        ('Basic information', {
            'fields': ('title', 'description', 'date', 'location')
        }),
        ('Additional data', {
            'fields': ('image', 'artworks', 'created_by'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)