from django.contrib import admin
from apps.units.models import (
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

@admin.register(TransdisciplinaryTheme)
class TransdisciplinaryThemeModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = (
        "name",
    )

@admin.register(PypKeyConcept)
class PypKeyConceptModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = (
        "name",
    )

@admin.register(PypAtlGroup)
class PypAtlGroupModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cluster",
    )
    list_display_links = (
        "name",
    )

@admin.register(PypAtlSkill)
class PypAtlSkillModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "group",
    )
    list_display_links = (
        "name",
    )

@admin.register(PypUnitPlanner)
class PypUnitPlannerModelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "year",
        "transdisciplinary_theme",
        "central_idea"
    )
    list_display_links = (
        "title",
    )

@admin.register(PypLinesOfInquiry)
class PypLinesOfInquiryModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "key_concept",
        "unit"
    )
    list_display_links = (
        "name",
    )

@admin.register(PypRelatedConcept)
class PypRelatedConceptModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "unit"
    )
    list_display_links = (
        "name",
    )

@admin.register(PypProfileAttribute)
class PypProfileAttributeModelAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "description",
        "unit"
    )
    list_display_links = (
        "profile",
    )

@admin.register(PypAtlDevelop)
class PypAtlDevelopModelAdmin(admin.ModelAdmin):
    list_display = (
        "atl",
        "action",
        "unit"
    )
    list_display_links = (
        "atl",
    )

@admin.register(PypUnitTeacherRoles)
class PypUnitTeacherRolesModelAdmin(admin.ModelAdmin):
    list_display = (
        "unit",
        "user",
        "role",
    )
    list_display_links = (
        "user",
    )

@admin.register(PypReflectionPost)
class PypReflectionPostModelAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "type",
        "author",
        "unit",
    )
    list_display_links = (
        "post",
    )