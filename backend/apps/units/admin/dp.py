from django.contrib import admin
from django import forms
from apps.units.models import (
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

@admin.register(DpAim)
class DpAimModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "discipline",
    )
    list_display_links = (
        "name",
    )

@admin.register(DpObjective)
class DpObjectiveModelAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "name",
        "discipline",
    )
    list_display_links = (
        "name",
    )

@admin.register(DpObjectiveItem)
class DpObjectiveItemModelAdmin(admin.ModelAdmin):
    list_display = (
        "letter",
        "name",
        "objective",
    )
    list_display_links = (
        "name",
    )

@admin.register(CourseTopic)
class CourseTopicModelAdmin(admin.ModelAdmin):
    list_display = (
        "letter",
        "name",
        "discipline",
    )
    list_display_links = (
        "name",
    )

@admin.register(CourseContent)
class CourseContentModelAdmin(admin.ModelAdmin):
    list_display = (
        "letter",
        "name",
        "topic",
    )
    list_display_links = (
        "name",
    )

@admin.register(Criterion)
class CriterionModelAdmin(admin.ModelAdmin):
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

@admin.register(DpUnitPlanner)
class DpUnitPlannerModelAdmin(admin.ModelAdmin):
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

@admin.register(DpInquiryQuestion)
class DpInquiryQuestionModelAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "type",
        "unit",
    )
    list_display_links = (
        "question",
    )

@admin.register(DpAtlDevelop)
class DpAtlDevelopModelAdmin(admin.ModelAdmin):
    list_display = (
        "atl",
        "unit",
    )
    list_display_links = (
        "atl",
    )

@admin.register(DpAtlSkill)
class DpAtlSkillModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cluster",
    )
    list_display_links = (
        "name",
    )

@admin.register(DpProfileDevelop)
class DpProfileDevelopModelAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "unit",
    )
    list_display_links = (
        "profile",
    )

@admin.register(DpReflectionPost)
class DpReflectionPostModelAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "author",
        "post",
        "unit",
    )
    list_display_links = (
        "author",
    )