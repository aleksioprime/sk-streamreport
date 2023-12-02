from django.contrib.admin import register, ModelAdmin, TabularInline, StackedInline
from import_export.admin import ImportExportModelAdmin

from apps.report.models import (
    ReportPeriod,
    ReportCriterion,
    ReportCriterionLevel,
    ReportTeacher,
    ReportCriterionAchievement,
    ReportTeacherPrimary,
    ReportPrimaryTopic,
    ReportTeacherSecondary,
    ReportSecondaryLevel,
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

class ReportLevelInline(StackedInline):  # StackedInline, TabularInline
    model = ReportCriterionLevel
    extra = 1

@register(ReportCriterion)
class ReportCriterionModelAdmin(ImportExportModelAdmin):
    inlines = [ReportLevelInline]
    list_display = (
        "id",
        "name",
        "author",
    )
    list_display_links = (
        "name",
    )
    readonly_fields = (
        "display_levels",
    )
    filter_horizontal = (
        'subjects',
        'years',
    )
    autocomplete_fields = (
        'author',
    )

    def display_levels(self, obj):
        levels = "\n".join([f"{lvl.point} - {lvl.name}" for lvl in obj.levels.all()])
        return f"{levels}"
    
    display_levels.short_description = "Уровни критерия"

@register(ReportCriterionLevel)
class ReportCriterionLevelModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "criterion",
        "name",
        "point",
    )
    list_display_links = (
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

@register(ReportCriterionAchievement)
class ReportCriterionAchievementModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "report",
        "criterion",
        "achievement",
    )
    list_display_links = (
        "criterion",
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

@register(ReportPrimaryTopic)
class ReportPrimaryTopicModelAdmin(ModelAdmin):
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

@register(ReportSecondaryLevel)
class ReportSecondaryLevelModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "report",
        "objective",
        "level",
    )
    list_display_links = (
        "report",
        "objective",
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

@register(ReportIbProfile)
class ReportIbProfileModelAdmin(ModelAdmin):
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

@register(ReportMentorPrimary)
class ReportMentorPrimaryModelAdmin(ModelAdmin):
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

@register(ReportPrimaryUnit)
class ReportPrimaryUnitModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "report",
        "unit",
        "comment",
    )
    list_display_links = (
        "report",
        "unit",
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