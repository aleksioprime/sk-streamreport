from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin

from apps.report.models import (
    ReportPeriod,
    ReportTeacherPrimary,
    ReportPrimaryIbProfile,
    ReportPrimaryAchievement,
    ReportTeacherSecondary,
    ReportSecondaryCriteria,
    ReportTeacherHigh,
    ReportMentor,
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
    fields = (
        "year",
        "order",
        "name",
        "date_start",
        "date_end",
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
    fields = (
        "student",
        "subject",
        "author",
        "period",
        "group",
        "comment",
        "created_at",
        "updated_at",
    )

@register(ReportPrimaryIbProfile)
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
    fields = (
        "report",
        "profile",
        "level",
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
    fields = (
        "report",
        "topic",
        "level",
        "comment",
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
    fields = (
        "student",
        "subject",
        "author",
        "period",
        "group",
        "comment",
        "achievements",
        "final_grade",
        "created_at",
        "updated_at",
    )
    filter_horizontal = ('achievements',)

@register(ReportSecondaryCriteria)
class ReportSecondaryCriteriaModelAdmin(ModelAdmin):
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
    fields = (
        "report",
        "criterion",
        "mark",
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
    fields = (
        "student",
        "subject",
        "author",
        "period",
        "group",
        "comment",
        "final_grade",
        "final_grade_ib",
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
    fields = (
        "student",
        "author",
        "period",
        "group",
        "comment",
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
    fields = (
        "student",
        "author",
        "role",
        "period",
        "group",
        "comment",
        "created_at",
        "updated_at",
    )