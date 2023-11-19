from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin

from apps.units.myp.models import (
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

@register(MypObjective)
class MypObjectiveModelAdmin(ImportExportModelAdmin):
    list_display = (
        "letter",
        "name",
        "group",
    )
    list_display_links = (
        "name",
    )

@register(Strand)
class StrandModelAdmin(ImportExportModelAdmin):
    list_display = (
        "number",
        "letter",
        "name",
        "objective",
    )
    list_display_links = (
        "name",
    )

@register(EducationalLevel)
class EducationalLevelModelAdmin(ImportExportModelAdmin):
    list_display = (
        "number",
        "name",
    )
    list_display_links = (
        "name",
    )

@register(StrandLevel)
class StrandLevelModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "level",
        "strand",
    )
    list_display_links = (
        "name",
    )

@register(AchievementLevel)
class AchievementLevelModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "strand_level",
        "point",
    )
    list_display_links = (
        "name",
    )

@register(MypAim)
class MypAimModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "group",
    )
    list_display_links = (
        "name",
    )

@register(MypKeyConcept)
class KeyConceptModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = (
        "name",
    )

@register(MypKeyConceptOfSubjects)
class KeyConceptOfSubjectsModelAdmin(ImportExportModelAdmin):
    list_display = (
        "key_concept",
        "group",
        "comment",
    )
    list_display_links = (
        "key_concept",
    )

@register(MypRelatedConcept)
class MypRelatedConceptModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = (
        "name",
    )

@register(GlobalContext)
class GlobalContextModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = (
        "name",
    )

@register(GlobalContextExploration)
class GlobalContextExplorationModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "global_context",
    )
    list_display_links = (
        "name",
    )

@register(MypAtlSkill)
class AtlSkillMypModelAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "cluster",
    )
    list_display_links = (
        "name",
    )

@register(MypUnitPlanner)
class MypUnitPlannerModelAdmin(ModelAdmin):
    list_display = (
        "title",
        "subject",
        "year",
    )
    list_display_links = (
        "title",
    )

@register(MypInquiryQuestion)
class MypInquiryQuestionModelAdmin(ModelAdmin):
    list_display = (
        "question",
        "type",
        "unit",
    )
    list_display_links = (
        "question",
    )

@register(MypAtlDevelop)
class MypAtlDevelopModelAdmin(ModelAdmin):
    list_display = (
        "atl",
        "strand",
        "unit",
    )
    list_display_links = (
        "atl",
    )

@register(MypReflectionPost)
class MypReflectionPostModelAdmin(ModelAdmin):
    list_display = (
        "post",
        "type",
        "author",
        "unit",
    )
    list_display_links = (
        "post",
    )

@register(MypUnitPlannerInterdisciplinary)
class MypUnitPlannerInterdisciplinaryModelAdmin(ModelAdmin):
    list_display = (
        "title",
        "year",
    )
    list_display_links = (
        "title",
    )

@register(MypInquiryQuestionIdu)
class MypInquiryQuestionIduModelAdmin(ModelAdmin):
    list_display = (
        "question",
        "type",
        "unit",
    )
    list_display_links = (
        "question",
    )

@register(MypAtlDevelopIdu)
class MypAtlDevelopIduModelAdmin(ModelAdmin):
    list_display = (
        "atl",
        "strand",
        "unit",
    )
    list_display_links = (
        "atl",
    )

@register(MypReflectionPostIdu)
class MypReflectionPostIduModelAdmin(ModelAdmin):
    list_display = (
        "post",
        "type",
        "author",
        "unit",
    )
    list_display_links = (
        "post",
    )
