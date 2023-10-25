from django.contrib import admin
from apps.units.models import (
    Criterion, 
    Strand, 
    EducationalLevel, 
    Objective, 
    AchievementLevel,
    Aim, 
    MypKeyConcept,
    MypKeyConceptOfSubjects,
    RelatedConcept,
    GlobalContext,
    GlobalContextExploration,
    MypAtlSkill,
    MypUnitPlanner,
    MypInquiryQuestion,
    MypAtlDevelop,
    MypReflectionPost,
    MypUnitPlannerInterdisciplinary
)

@admin.register(Criterion)
class CriterionModelAdmin(admin.ModelAdmin):
    list_display = (
        "letter",
        "name",
        "group",
    )
    list_display_links = (
        "name",
    )

@admin.register(Strand)
class StrandModelAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "letter",
        "name",
        "criterion",
    )
    list_display_links = (
        "name",
    )

@admin.register(EducationalLevel)
class EducationalLevelModelAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "name",
    )
    list_display_links = (
        "name",
    )

@admin.register(Objective)
class ObjectivenModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
        "strand",
    )
    list_display_links = (
        "name",
    )

@admin.register(AchievementLevel)
class AchievementLevelModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "objective",
        "point",
    )
    list_display_links = (
        "name",
    )

@admin.register(Aim)
class AimModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "group",
    )
    list_display_links = (
        "name",
    )

@admin.register(MypKeyConcept)
class KeyConceptModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = (
        "name",
    )

@admin.register(MypKeyConceptOfSubjects)
class KeyConceptOfSubjectsModelAdmin(admin.ModelAdmin):
    list_display = (
        "key_concept",
        "group",
        "comment",
    )
    list_display_links = (
        "key_concept",
    )

@admin.register(RelatedConcept)
class RelatedConceptModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = (
        "name",
    )

@admin.register(GlobalContext)
class GlobalContextModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = (
        "name",
    )

@admin.register(GlobalContextExploration)
class GlobalContextExplorationModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "global_context",
    )
    list_display_links = (
        "name",
    )

@admin.register(MypAtlSkill)
class AtlSkillMypModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cluster",
    )
    list_display_links = (
        "name",
    )

@admin.register(MypUnitPlanner)
class MypUnitPlannerModelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "year",
    )
    list_display_links = (
        "title",
    )

@admin.register(MypInquiryQuestion)
class MypInquiryQuestionModelAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "type",
        "unit",
        "idu"
    )
    list_display_links = (
        "question",
    )

@admin.register(MypAtlDevelop)
class MypAtlDevelopModelAdmin(admin.ModelAdmin):
    list_display = (
        "atl",
        "strand",
        "unit",
    )
    list_display_links = (
        "atl",
    )

@admin.register(MypReflectionPost)
class MypReflectionPostModelAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "type",
        "author",
        "unit",
        "idu"
    )
    list_display_links = (
        "post",
    )

@admin.register(MypUnitPlannerInterdisciplinary)
class MypUnitPlannerInterdisciplinaryModelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "year",
    )
    list_display_links = (
        "title",
    )