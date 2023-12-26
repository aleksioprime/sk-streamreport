from django.contrib.admin import register, ModelAdmin, TabularInline, StackedInline
from import_export.admin import ImportExportModelAdmin
from django import forms

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
    TypeReportChoices
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

class ReportCriterionLevelInline(StackedInline):  # StackedInline, TabularInline
    model = ReportCriterionLevel
    extra = 1

# Кастомное поле формы, которое обрабатывает данные между ArrayField и CheckboxSelectMultiple
class MultipleCheckboxField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def to_python(self, value):
        if not value:
            return []
        return value

    def prepare_value(self, value):
        return value if value else []
    
@register(ReportCriterion)
class ReportCriterionModelAdmin(ImportExportModelAdmin):
    inlines = [ReportCriterionLevelInline]
    search_fields = (
        "name",
    )
    list_display = (
        "id",
        "name",
        "author",
        "type",
    )
    list_display_links = (
        "name",
    )
    filter_horizontal = (
        'subjects',
        'years',
    )
    # autocomplete_fields = (
    #     'author',
    # )
    # переопределяем метод: для определённых полей заменяем виджет, иначе вызываем родительскую реализацию
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "type":
            return MultipleCheckboxField(
                label=db_field.verbose_name,
                initial=db_field.default,
                choices=TypeReportChoices.choices,
                help_text=db_field.help_text
            )
        return super().formfield_for_dbfield(db_field, **kwargs)

@register(ReportCriterionLevel)
class ReportCriterionLevelModelAdmin(ImportExportModelAdmin):
    search_fields = (
        "criterion__name",
    )
    list_display = (
        "id",
        "criterion",
        "name",
        "point",
        "description",
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
        "strand",
        "level",
    )
    list_display_links = (
        "report",
        "strand",
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