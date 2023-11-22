from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin

from apps.report.models import (
    ReportPeriod,
    ReflectionChecklist,
    ReflectionChecklistLevel,
    ReportTeacher,
    ReportChecklistAchievement,
    ReportTeacherPrimary,
    ReportPrimaryAchievement,
    ReportTeacherSecondary,
    ReportSecondaryCriterion,
    ReportTeacherHigh,
    ReportMentor,
    ReportIbProfile,
    ReportMentorPrimary,
    ReportPrimaryUnit,
    ReportExtra,
)

@register(ReportPeriod)
class ReportPeriodModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "year",
        "order",
        "name",
        "date_start",
        "date_end",
    )
    list_display_links = (
        "order",
        "name",
    )

@register(ReportTeacher)
class ReportTeacherModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "period",
        "group",
        "student",
        "subject",
        "author",
        "updated_at",
    )
    list_display_links = (
        "student",
        "author",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

@register(ReportTeacherPrimary)
class ReportTeacherPrimaryModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "period",
        "group",
        "student",
        "subject",
        "author",
        "updated_at",
    )
    list_display_links = (
        "student",
        "author",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

@register(ReportIbProfile)
class ReportPrimaryIbProfileModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "report",
        "profile",
        "level",
    )
    list_display_links = (
        "report",
        "profile",
    )

@register(ReportPrimaryAchievement)
class ReportPrimaryAchievementModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "report",
        "topic",
        "level",
    )
    list_display_links = (
        "report",
        "topic",
    )

@register(ReportTeacherSecondary)
class ReportTeacherSecondaryModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "period",
        "group",
        "student",
        "subject",
        "author",
        "updated_at",
    )
    list_display_links = (
        "student",
        "author",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

@register(ReportSecondaryCriterion)
class ReportSecondaryCriterionModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "report",
        "criterion",
        "mark",
    )
    list_display_links = (
        "report",
        "criterion",
    )

@register(ReportTeacherHigh)
class ReportTeacherHighModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "period",
        "group",
        "student",
        "subject",
        "author",
        "final_grade",
        "final_grade_ib",
        "updated_at",
    )
    list_display_links = (
        "student",
        "author",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

@register(ReportMentor)
class ReportMentorModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "period",
        "group",
        "student",
        "author",
        "updated_at",
    )
    list_display_links = (
        "student",
        "author",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

@register(ReportExtra)
class ReportExtraModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "period",
        "group",
        "student",
        "author",
        "role",
        "updated_at",
    )
    list_display_links = (
        "student",
        "author",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )