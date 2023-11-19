from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin

from apps.portfolio.models import (
    EventParticipation,
)

@register(EventParticipation)
class EventParticipationModelAdmin(ImportExportModelAdmin):
    list_display = (
        "student",
        "group",
        "title",
    )
    list_display_links = (
        "student",
    )