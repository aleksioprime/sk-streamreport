from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin
from apps.curriculum.models import (
    Subject,
    FgosSubjectGroup,
    IbSubjectGroup,
    IbDiscipline,
    Curriculum,
    CurriculumLoad,
    TeachingLoad
)

@register(Subject)
class SubjectModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "group_ib",
        "group_fgos",
        "type"
    )
    list_display_links = (
        "name",
    )
    fields = (
        "name",
        "group_ib",
        "group_fgos",
        "type",
        "dnevnik_id",
        "department",
        "level",
        "need_report"
    )

@register(FgosSubjectGroup)
class SubjectGroupFgosModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "type"
    )
    list_display_links = (
        "name",
    )
    fields = (
        "name",
        "type",
    )

@register(IbSubjectGroup)
class SubjectGroupIbModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "program",
    )
    list_display_links = (
        "name",
    )
    fields = (
        "name",
        "name_rus",
        "logo",
        "program",
    )

@register(IbDiscipline)
class SubjectGroupIbModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "group",
    )
    list_display_links = (
        "name",
    )
    fields = (
        "name",
        "name_rus",
        "group",
    )

@register(Curriculum)
class CurriculumModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "name_short",
        "level",
        "year",
    )
    list_display_links = (
        "name_short",
    )
    fields = (
        "name",
        "name_short",
        "level",
        "year",
    )

@register(CurriculumLoad)
class CurriculumLoadModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "curriculum",
        "subject",
        "hours",
    )
    list_display_links = (
        "curriculum",
    )
    fields = (
        "curriculum",
        "subject",
        "years",
        "hours",
    )

@register(TeachingLoad)
class TeachingLoadModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "year",
        "teacher",
        "subject",
        "hours",
    )
    list_display_links = (
        "year",
    )
    fields = (
        "year",
        "teacher",
        "subject",
        "groups",
        "hours",
    )