from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin

from apps.ibo.models import (
    LearnerProfile,
    AtlCategory,
    AtlCluster,
)

@register(LearnerProfile)
class LearnerProfileModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "name_rus",
        "description",
    )
    list_display_links = (
        "name",
    )

@register(AtlCategory)
class AtlCategoryModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "name_rus",
    )
    list_display_links = (
        "name",
    )

@register(AtlCluster)
class AtlClusterModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "name_rus",
    )
    list_display_links = (
        "name",
    )