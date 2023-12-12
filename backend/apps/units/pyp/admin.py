from django.contrib.admin import register, ModelAdmin, StackedInline
from import_export.admin import ImportExportModelAdmin

from apps.units.pyp.models import (
    TransdisciplinaryTheme,
    PypKeyConcept,
    PypAtlGroup,
    PypAtlSkill,
    PypUnitPlanner,
    PypLinesOfInquiry,
    PypRelatedConcept,
    PypAtlDevelop,
    PypAtlCluster
)

from apps.ibo.models import (
    UnitTeacherRoles
)

@register(TransdisciplinaryTheme)
class TransdisciplinaryThemeModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = (
        "name",
    )

@register(PypKeyConcept)
class PypKeyConceptModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = (
        "name",
    )

@register(PypAtlCluster)
class PypAtlClusterModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "category",
    )
    list_display_links = (
        "name",
    )

@register(PypAtlGroup)
class PypAtlGroupModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "cluster",
    )
    list_display_links = (
        "name",
    )

@register(PypAtlSkill)
class PypAtlSkillModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "group",
    )
    list_display_links = (
        "name",
    )

class TeacherRolesInline(StackedInline):  # StackedInline, TabularInline
    model = UnitTeacherRoles
    extra = 1

@register(PypUnitPlanner)
class PypUnitPlannerModelAdmin(ModelAdmin):
    inlines = [TeacherRolesInline]
    list_display = (
        "title",
        "year",
        "transdisciplinary_theme",
        "central_idea"
    )
    list_display_links = (
        "title",
    )
    filter_horizontal = (
        'teachers',
    )

@register(PypLinesOfInquiry)
class PypLinesOfInquiryModelAdmin(ModelAdmin):
    list_display = (
        "name",
        "key_concept",
        "unit"
    )
    list_display_links = (
        "name",
    )

@register(PypRelatedConcept)
class PypRelatedConceptModelAdmin(ModelAdmin):
    list_display = (
        "name",
        "unit"
    )
    list_display_links = (
        "name",
    )

@register(PypAtlDevelop)
class PypAtlDevelopModelAdmin(ModelAdmin):
    list_display = (
        "atl",
        "action",
        "unit"
    )
    list_display_links = (
        "atl",
    )