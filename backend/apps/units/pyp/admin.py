from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin

from apps.units.pyp.models import (
    TransdisciplinaryTheme,
    PypKeyConcept,
    PypAtlGroup,
    PypAtlSkill,
    PypUnitPlanner,
    PypLinesOfInquiry,
    PypRelatedConcept,
    PypProfileAttribute,
    PypAtlDevelop,
    PypUnitTeacherRoles,
    PypReflectionPost
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

@register(PypUnitPlanner)
class PypUnitPlannerModelAdmin(ModelAdmin):
    list_display = (
        "title",
        "year",
        "transdisciplinary_theme",
        "central_idea"
    )
    list_display_links = (
        "title",
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

@register(PypProfileAttribute)
class PypProfileAttributeModelAdmin(ModelAdmin):
    list_display = (
        "profile",
        "description",
        "unit"
    )
    list_display_links = (
        "profile",
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

@register(PypUnitTeacherRoles)
class PypUnitTeacherRolesModelAdmin(ModelAdmin):
    list_display = (
        "unit",
        "user",
        "role",
    )
    list_display_links = (
        "user",
    )

@register(PypReflectionPost)
class PypReflectionPostModelAdmin(ModelAdmin):
    list_display = (
        "post",
        "type",
        "author",
        "unit",
    )
    list_display_links = (
        "post",
    )
