from django.contrib import admin
from apps.syllabus.models import (
    Subject,
    FgosSubjectGroup,
    IbSubjectGroup,
    IbDisciplines,
    Syllabus,
    SyllabusSubjectHours,
    TeachingLoad
)

@admin.register(Subject)
class SubjectModelAdmin(admin.ModelAdmin):
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

@admin.register(FgosSubjectGroup)
class SubjectGroupFgosModelAdmin(admin.ModelAdmin):
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

@admin.register(IbSubjectGroup)
class SubjectGroupIbModelAdmin(admin.ModelAdmin):
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

@admin.register(IbDisciplines)
class SubjectGroupIbModelAdmin(admin.ModelAdmin):
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

@admin.register(Syllabus)
class SyllabusModelAdmin(admin.ModelAdmin):
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

@admin.register(SyllabusSubjectHours)
class SyllabusSubjectHoursModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "syllabus",
        "subject",
        "hours",
    )
    list_display_links = (
        "syllabus",
    )
    fields = (
        "syllabus",
        "subject",
        "years",
        "hours",
    )

@admin.register(TeachingLoad)
class TeachingLoadModelAdmin(admin.ModelAdmin):
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