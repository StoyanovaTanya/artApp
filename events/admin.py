from django.contrib import admin

from events.models import Event


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'created_by')
    search_fields = ('title', 'description', 'location')
    list_filter = ('date', 'location',)
    ordering = ('date',)
