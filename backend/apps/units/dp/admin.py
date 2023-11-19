from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin
from django import forms

from apps.units.dp.models import (
    DpAim,
    DpObjective,
    DpObjectiveItem,
    CourseTopic,
    CourseContent,
    Criterion,
    DpAtlSkill,
    DpUnitPlanner,
    DpInquiryQuestion,
    DpAtlDevelop,
    DpProfileDevelop,
    DpReflectionPost,
    LevelDpChoices,
    LanguageLearningChoices,
    TokConnectionsChoices,
    CasConnectionsChoices,
    LearningProcessChoices,
    DifferentiationChoices
)

@register(DpAim)
class DpAimModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "type",
        "discipline",
    )
    list_display_links = (
        "name",
    )

@register(DpObjective)
class DpObjectiveModelAdmin(ImportExportModelAdmin):
    list_display = (
        "number",
        "name",
        "discipline",
    )
    list_display_links = (
        "name",
    )

@register(DpObjectiveItem)
class DpObjectiveItemModelAdmin(ImportExportModelAdmin):
    list_display = (
        "letter",
        "name",
        "objective",
    )
    list_display_links = (
        "name",
    )

@register(CourseTopic)
class CourseTopicModelAdmin(ImportExportModelAdmin):
    list_display = (
        "letter",
        "name",
        "discipline",
    )
    list_display_links = (
        "name",
    )

@register(CourseContent)
class CourseContentModelAdmin(ImportExportModelAdmin):
    list_display = (
        "letter",
        "name",
        "topic",
    )
    list_display_links = (
        "name",
    )

@register(Criterion)
class CriterionModelAdmin(ImportExportModelAdmin):
    list_display = (
        "letter",
        "name",
        "discipline",
    )
    list_display_links = (
        "name",
    )

# Кастомное поле формы, которое обрабатывает данные между ArrayField и CheckboxSelectMultiple
class MultipleCheckboxField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def to_python(self, value):
        if not value:
            return []
        return value

    def prepare_value(self, value):
        return value if value else []

@register(DpUnitPlanner)
class DpUnitPlannerModelAdmin(ModelAdmin):
    list_display = (
        "title",
        "year",
    )
    list_display_links = (
        "title",
    )
    # переопределяем метод: для определённых полей заменяем виджет, иначе вызываем родительскую реализацию
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "levels":
            return MultipleCheckboxField(
                label=db_field.verbose_name,
                initial=db_field.default,
                choices=LevelDpChoices.choices,
                help_text=db_field.help_text
            )
        if db_field.name == "language_learning":
            return MultipleCheckboxField(
                label=db_field.verbose_name,
                initial=db_field.default,
                choices=LanguageLearningChoices.choices,
                help_text=db_field.help_text
            )
        if db_field.name == "tok_connections":
            return MultipleCheckboxField(
                label=db_field.verbose_name,
                initial=db_field.default,
                choices=TokConnectionsChoices.choices,
                help_text=db_field.help_text
            )
        if db_field.name == "cas_connections":
            return MultipleCheckboxField(
                label=db_field.verbose_name,
                initial=db_field.default,
                choices=CasConnectionsChoices.choices,
                help_text=db_field.help_text
            )
        if db_field.name == "learning_process":
            return MultipleCheckboxField(
                label=db_field.verbose_name,
                initial=db_field.default,
                choices=LearningProcessChoices.choices,
                help_text=db_field.help_text
            )
        if db_field.name == "differentiation":
            return MultipleCheckboxField(
                label=db_field.verbose_name,
                initial=db_field.default,
                choices=DifferentiationChoices.choices,
                help_text=db_field.help_text
            )
        return super().formfield_for_dbfield(db_field, **kwargs)

@register(DpInquiryQuestion)
class DpInquiryQuestionModelAdmin(ModelAdmin):
    list_display = (
        "question",
        "type",
        "unit",
    )
    list_display_links = (
        "question",
    )

@register(DpAtlDevelop)
class DpAtlDevelopModelAdmin(ModelAdmin):
    list_display = (
        "atl",
        "unit",
    )
    list_display_links = (
        "atl",
    )

@register(DpAtlSkill)
class DpAtlSkillModelAdmin(ModelAdmin):
    list_display = (
        "name",
        "cluster",
    )
    list_display_links = (
        "name",
    )

@register(DpProfileDevelop)
class DpProfileDevelopModelAdmin(ModelAdmin):
    list_display = (
        "profile",
        "unit",
    )
    list_display_links = (
        "profile",
    )

@register(DpReflectionPost)
class DpReflectionPostModelAdmin(ModelAdmin):
    list_display = (
        "type",
        "author",
        "post",
        "unit",
    )
    list_display_links = (
        "author",
    )