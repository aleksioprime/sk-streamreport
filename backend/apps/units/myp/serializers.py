from rest_framework import serializers

from apps.units.myp.models import (
    MypUnitPlanner,
    MypUnitPlannerId,
    MypObjective,
    Strand,
    StrandLevel,
    StrandLevelAchievement,
    MypAim,
    MypKeyConcept,
    MypKeyConceptOfSubjects,
    MypRelatedConcept,
    GlobalContext,
    GlobalContextExploration,
    MypAtlSkill,
    MypAtlDevelop,
    MypAtlDevelopIdu,
    MypInquiryQuestion,
    MypInquiryQuestionIdu,
    )

from apps.curriculum.models import (
    IbSubjectGroup,
    IbDiscipline,
    Subject,
)

from general.models import (
    User,
    StudyYear
)

from apps.ibo.models import (
    AtlCategory,
    AtlCluster,
    LearnerProfile,
    IbProfileDevelop,
    UnitReflectionPost,
)

# Уровни достижений предметных целей для MYP
class StrandLevelAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrandLevelAchievement
        fields = (
            "id",
            "name",
            "name_rus",
            "point",
            )

# Cтрэнды предметных целей по уровням и годам обучения для MYP
class StrandLevelSerializer(serializers.ModelSerializer):
    achieve_levels = StrandLevelAchievementSerializer(many=True)
    class Meta:
        model = StrandLevel
        fields = (
            "id",
            "name",
            "name_rus",
            "level",
            "achieve_levels",
            )

# Cтрэнды предметных целей для MYP
class StrandSerializer(serializers.ModelSerializer):
    strand_levels = StrandLevelSerializer(many=True)
    class Meta:
        model = StrandLevel
        fields = (
            "id",
            "number",
            "letter",
            "name",
            "name_rus",
            "strand_levels",
            )

# Предметные цели для MYP
class MypObjectiveSerializer(serializers.ModelSerializer):
    strands = StrandSerializer(many=True)
    class Meta:
        model = MypObjective
        fields = (
            "id",
            "letter",
            "name",
            "name_rus",
            "description",
            "description_rus",
            "strands",
            )

# Вывод списка предметных групп
class IbSubjectGroupMypSerializer(serializers.ModelSerializer):
    class Meta:
        model = IbSubjectGroup
        fields = (
            "id",
            "name",
            "name_rus",
            "logo",
            "program",
            )

# Вывод списка предметных целей для MYP
class MypObjectiveListSerializer(serializers.ModelSerializer):
    group = IbSubjectGroupMypSerializer()
    class Meta:
        model = MypObjective
        fields = (
            "id",
            "letter",
            "name",
            "name_rus",
            "description",
            "description_rus",
            "group",
            )

# Вывод списка стрэндов предметных целей для MYP
class StrandListSerializer(serializers.ModelSerializer):
    objective = MypObjectiveListSerializer()
    strand_levels = StrandLevelSerializer(many=True)
    class Meta:
        model = Strand
        fields = (
            "id",
            "number",
            "letter",
            "name",
            "name_rus",
            "objective",
            "strand_levels"
            )

# Вывод списка стрэндов предметных целей по уровням и годам обучения для MYP
class StrandLevelListSerializer(serializers.ModelSerializer):
    strand = MypObjectiveListSerializer()
    achieve_levels = StrandLevelAchievementSerializer()
    class Meta:
        model = StrandLevel
        fields = (
            "id",
            "name",
            "name_rus",
            "level",
            "strand",
            "achieve_levels",
            )

# Вывод списка уровней достижений предметных целей для MYP
class StrandLevelAchievementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrandLevelAchievement
        fields = (
            "id",
            "name",
            "name_rus",
            "level",
            "point",
            )

# Вывод списка целей предметных групп для MYP
class MypAimListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypAim
        fields = (
            "id",
            "name",
            "name_rus",
            "group",
            )

# Вывод рекомендуемых предметных групп для MYP
class MypKeyConceptOfSubjectsSerializer(serializers.ModelSerializer):
    groups = IbSubjectGroupMypSerializer(many=True)
    class Meta:
        model = MypKeyConceptOfSubjects
        fields = (
            "id",
            "groups",
            "comment",
            "comment_rus",
            )

# Вывод списка ключевых концептов для MYP
class MypKeyConceptListSerializer(serializers.ModelSerializer):
    subjects_recomends = MypKeyConceptOfSubjectsSerializer(many=True)
    class Meta:
        model = MypKeyConcept
        fields = (
            "id",
            "name",
            "name_rus",
            "subjects_recomends",
            )

# Вывод IB-дисциплин
class IbDisciplineMypSerializer(serializers.ModelSerializer):
    group = IbSubjectGroupMypSerializer()
    class Meta:
        model = IbDiscipline
        fields = (
            "id",
            "name",
            "name_rus",
            "group",
            )

# Вывод списка сопутствующих концептов для MYP
class MypRelatedConceptListSerializer(serializers.ModelSerializer):
    disciplines = IbDisciplineMypSerializer(many=True)
    class Meta:
        model = MypRelatedConcept
        fields = (
            "id",
            "name",
            "name_rus",
            "description",
            "description_rus",
            "disciplines",
            )

# Вывод списка глобальных контекстов для MYP
class GlobalContextListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalContext
        fields = (
            "id",
            "name",
            "name_rus",
            "description",
            "description_rus",
            )
        
# Вывод списка линий исследований глобальных контекстов для MYP
class GlobalContextExplorationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalContextExploration
        fields = (
            "id",
            "name",
            "name_rus",
            "global_context",
            )

# Список категорий ATL для MYP
class AtlCategoryMypSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlCategory
        fields = (
            "id",
            "name",
            "name_rus",
            )

# Список кластеров ATL для MYP
class AtlClusterMypSerializer(serializers.ModelSerializer):
    category = AtlCategoryMypSerializer()
    class Meta:
        model = AtlCluster
        fields = (
            "id",
            "name",
            "name_rus",
            "category",
            )
        
# Вывод списка навыков ATL для MYP
class MypAtlSkillListSerializer(serializers.ModelSerializer):
    cluster = AtlClusterMypSerializer()
    class Meta:
        model = MypAtlSkill
        fields = (
            "id",
            "name",
            "name_rus",
            "cluster",
            )

# Список качеств портрета студента IB
class LearnerProfileMypSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerProfile
        fields = (
            "id",
            "name",
            "name_rus",
            "description",
            "description_rus",
            )

# Список развития качеств портрета студента IB в юните
class IbProfileDevelopMypSerializer(serializers.ModelSerializer):
    profile = LearnerProfileMypSerializer()
    class Meta:
        model = IbProfileDevelop
        fields = (
            "id",
            "profile",
            "description",
            "unit",
            )

# Список пользователей
class UserMypSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            )

# Список постов рефлексии по юниту
class UnitReflectionPostMypSerializer(serializers.ModelSerializer):
    author = UserMypSerializer()
    class Meta:
        model = UnitReflectionPost
        fields = (
            "id",
            "post",
            "type",
            "author",
            "unit",
            )

# Список учебных параллелей
class StudyYearMypSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            )

# Список предметов
class SubjectMypSerializer(serializers.ModelSerializer):
    group_ib = IbSubjectGroupMypSerializer()
    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "group_ib",
            )

# Вывод списка исследовательских вопросов в юните MYP
class MypInquiryQuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypInquiryQuestion
        fields = (
            "id",
            "question",
            "type",
            "line",
            "unit",
            )
        
# Создание и редактирование исследовательских вопросов в юните MYP
class MypInquiryQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypInquiryQuestion
        fields = '__all__'

# Вывод списка пунктов развития ATL-навыков в юните MYP
class MypAtlDevelopListSerializer(serializers.ModelSerializer):
    atl = MypAtlSkillListSerializer()
    strand = StrandListSerializer()
    class Meta:
        model = MypAtlDevelop
        fields = (
            "id",
            "atl",
            "strand",
            "action",
            "unit",
            )
        
# Создание и редактирование пункта развития ATL-навыков в юните MYP
class MypAtlDevelopUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypAtlDevelop
        fields = '__all__'

# Вывод списка планнеров в MYP
class MypUnitPlannerListSerializer(serializers.ModelSerializer):
    teachers = UserMypSerializer(many=True)
    authors = UserMypSerializer(many=True)
    year = StudyYearMypSerializer()
    subject = SubjectMypSerializer()
    global_context = GlobalContextListSerializer()
    class Meta:
        model = MypUnitPlanner
        fields = (
            "id",
            "order",
            "title",
            "teachers",
            "authors",
            "year",
            "hours",
            "description",
            "created_at",
            "updated_at",
            "subject",
            "level",
            "global_context",
        )
        
# Подробный просмотр планнера в MYP
class MypUnitPlannerRetrieveSerializer(serializers.ModelSerializer):
    teachers = UserMypSerializer(many=True)
    authors = UserMypSerializer(many=True)
    year = StudyYearMypSerializer()
    subject = SubjectMypSerializer()
    key_concept = MypKeyConceptListSerializer()
    related_concepts = MypRelatedConceptListSerializer(many=True)
    global_context = GlobalContextListSerializer()
    explorations = GlobalContextExplorationListSerializer(many=True)
    aims = MypAimListSerializer(many=True)
    strands = StrandListSerializer(many=True)
    objectives = MypObjectiveListSerializer(many=True)
    inquiry_questions = MypInquiryQuestionListSerializer(many=True)
    atl_develops = MypAtlDevelopListSerializer(many=True)
    ibprofiles = IbProfileDevelopMypSerializer(many=True)
    reflection_posts = UnitReflectionPostMypSerializer(many=True)
    class Meta:
        model = MypUnitPlanner
        fields = (
            "id",
            "order",
            "title",
            "teachers",
            "authors",
            "year",
            "hours",
            "description",
            "created_at",
            "updated_at",
            "subject",
            "level",
            "key_concept",
            'related_concepts',
            "global_context",
            "explorations",
            "conceptual_understanding",
            "statement_inquiry",
            "aims",
            "strands",
            "content",
            "skills",
            "international_mindedness",
            "academic_integrity",
            "language_development",
            "infocom_technology",
            "service_as_action",
            "objectives",
            "formative_assessment",
            "summative_assessment_task",
            "summative_assessment_soi",
            "peer_self_assessment",
            "standardization_moderation",
            "prior_experiences",
            "learning_experiences",
            "teaching_strategies",
            "student_expectations",
            "feedback",
            "differentiation",
            "resources",
            "interdisciplinary",
            "inquiry_questions",
            "atl_develops",
            "ibprofiles",
            "reflection_posts",
            )
        
# Создание планнера в MYP
class MypUnitPlannerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypUnitPlanner
        fields = (
            "id",
            "order",
            "title",
            "teachers",
            "authors",
            "year",
            "hours",
            "description",
            "created_at",
            "updated_at",
            "subject",
            "level",
            "global_context",
            )

# Редактирование планнера в MYP
class MypUnitPlannerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypUnitPlanner
        fields = '__all__'

# Вывод списка исследовательских вопросов в междисциплинарном юните MYP
class MypInquiryQuestionIduListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypInquiryQuestionIdu
        fields = (
            "id",
            "question",
            "type",
            "line",
            "unit",
            )
        
# Создание и редактирование исследовательских вопросов в междисциплинарном юните MYP
class MypInquiryQuestionIduUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypInquiryQuestionIdu
        fields = '__all__'

# Вывод списка пунктов развития ATL-навыков в междисциплинарном юните MYP
class MypAtlDevelopIduListSerializer(serializers.ModelSerializer):
    atl = MypAtlSkillListSerializer()
    strand = StrandListSerializer()
    class Meta:
        model = MypAtlDevelopIdu
        fields = (
            "id",
            "atl",
            "strand",
            "action",
            "unit",
            )
        
# Создание и редактирование пункта развития ATL-навыков в междисциплинарном юните MYP
class MypAtlDevelopIduUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypAtlDevelopIdu
        fields = '__all__'

# Список междисциплинарных планеров в MYP
class MypUnitPlannerIdListSerializer(serializers.ModelSerializer):
    teachers = UserMypSerializer(many=True)
    authors = UserMypSerializer(many=True)
    year = StudyYearMypSerializer()
    global_context = GlobalContextListSerializer()
    class Meta:
        model = MypUnitPlannerId
        fields = (
            "id",
            "order",
            "title",
            "teachers",
            "authors",
            "year",
            "hours",
            "description",
            "created_at",
            "updated_at",
            "global_context"
            )
        
# Подробный просмотр междисциплинарных планеров в MYP
class MypUnitPlannerIdRetrieveSerializer(serializers.ModelSerializer):
    teachers = UserMypSerializer(many=True)
    authors = UserMypSerializer(many=True)
    year = StudyYearMypSerializer()
    key_concepts = MypKeyConceptListSerializer(many=True)
    global_context = GlobalContextListSerializer()
    explorations = GlobalContextExplorationListSerializer(many=True)
    strands = StrandListSerializer(many=True)
    objectives = MypObjectiveListSerializer(many=True)
    inquiry_questions = MypInquiryQuestionIduListSerializer(many=True)
    atl_develops = MypAtlDevelopIduListSerializer(many=True)
    ibprofiles = IbProfileDevelopMypSerializer(many=True)
    reflection_posts = UnitReflectionPostMypSerializer(many=True)
    class Meta:
        model = MypUnitPlannerId
        fields = (
            "id",
            "order",
            "title",
            "teachers",
            "authors",
            "year",
            "hours",
            "description",
            "created_at",
            "updated_at",
            "real_world_issue",
            "integrated_purpose",
            "synthesis",
            "key_concepts",
            "conceptual_understanding",
            "global_context",
            "explorations",
            "statement_inquiry",
            "objectives",
            "strands",
            "tasks",
            "introduction",
            "learning_teaching",
            "summative_assessment",
            "differentiation",
            "resources",
            "inquiry_questions",
            "atl_develops",
            "ibprofiles",
            "reflection_posts",
            "teacher_roles",
            )
        
# Создание междисциплинарного планнера в MYP
class MypUnitPlannerIdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypUnitPlannerId
        fields = (
            "id",
            "order",
            "title",
            "teachers",
            "authors",
            "year",
            "hours",
            "description",
            "created_at",
            "updated_at",
            "global_context",
            )
        
# Редактирование междисциплинарного планнера в MYP
class MypUnitPlannerIdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypUnitPlannerId
        fields = '__all__'