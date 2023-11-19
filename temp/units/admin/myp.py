from django.contrib import admin
from apps.units.models import (
    MypObjective, 
    Strand, 
    EducationalLevel, 
    StrandLevel, 
    AchievementLevel,
    MypAim, 
    MypKeyConcept,
    MypKeyConceptOfSubjects,
    MypRelatedConcept,
    GlobalContext,
    GlobalContextExploration,
    MypAtlSkill,
    MypUnitPlanner,
    MypInquiryQuestion,
    MypAtlDevelop,
    MypReflectionPost,
    MypUnitPlannerInterdisciplinary,
    MypInquiryQuestionIdu,
    MypAtlDevelopIdu,
    MypReflectionPostIdu
)

@admin.register(MypObjective)
class MypObjectiveModelAdmin(admin.ModelAdmin):
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
        "objective",
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

@admin.register(StrandLevel)
class StrandLevelModelAdmin(admin.ModelAdmin):
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
        "strand_level",
        "point",
    )
    list_display_links = (
        "name",
    )

@admin.register(MypAim)
class MypAimModelAdmin(admin.ModelAdmin):
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

@admin.register(MypRelatedConcept)
class MypRelatedConceptModelAdmin(admin.ModelAdmin):
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

@admin.register(MypInquiryQuestionIdu)
class MypInquiryQuestionIduModelAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "type",
        "unit",
    )
    list_display_links = (
        "question",
    )

@admin.register(MypAtlDevelopIdu)
class MypAtlDevelopIduModelAdmin(admin.ModelAdmin):
    list_display = (
        "atl",
        "strand",
        "unit",
    )
    list_display_links = (
        "atl",
    )

@admin.register(MypReflectionPostIdu)
class MypReflectionPostIduModelAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "type",
        "author",
        "unit",
    )
    list_display_links = (
        "post",
    )