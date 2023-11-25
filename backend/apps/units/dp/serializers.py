from rest_framework import serializers

from apps.units.dp.models import (
    DpUnitPlanner,
    DpObjective,
    DpAim,
    DpObjectiveItem,
    CourseTopic,
    CourseContent,
    Criterion,
    DpAtlSkill,
    DpInquiryQuestion,
    DpAtlDevelop
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

from apps.curriculum.models import (
    IbSubjectGroup,
    IbDiscipline,
    Subject,
)

# Список пользователей
class UserDpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            )

# Список учебных параллелей
class StudyYearDpSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            )

# Вывод списка предметных групп IB
class IbSubjectGroupDpSerializer(serializers.ModelSerializer):
    class Meta:
        model = IbSubjectGroup
        fields = (
            "id",
            "name",
            "name_rus",
            "logo",
            "program",
            )

# Вывод IB-дисциплин
class IbDisciplineDpSerializer(serializers.ModelSerializer):
    group = IbSubjectGroupDpSerializer()
    class Meta:
        model = IbDiscipline
        fields = (
            "id",
            "name",
            "name_rus",
            "group",
            )

# Вывод списка целей предметных групп для DP
class DpAimListSerializer(serializers.ModelSerializer):
    discipline = IbDisciplineDpSerializer()
    class Meta:
        model = DpAim
        fields = (
            "id",
            "name",
            "type",
            "discipline",
            )

# Пункты предметных целей для DP
class DpObjectiveItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpObjectiveItem
        fields = (
            "id",
            "letter",
            "name",
            "objective",
            )

# Вывод списка предметных целей для DP
class DpObjectiveListSerializer(serializers.ModelSerializer):
    discipline = IbDisciplineDpSerializer()
    items = DpObjectiveItemListSerializer(many=True)
    class Meta:
        model = DpObjective
        fields = (
            "id",
            "number",
            "name",
            "discipline",
            "items",
            )
        
# Список разделов курса DP-дисциплин
class CourseTopicSerializer(serializers.ModelSerializer):
    discipline = IbDisciplineDpSerializer()
    class Meta:
        model = CourseTopic
        fields = (
            "id",
            "letter",
            "name",
            "discipline",
            )

# Вывод списка учебных тем для DP
class CourseContentListSerializer(serializers.ModelSerializer):
    topic = CourseTopicSerializer()
    class Meta:
        model = CourseContent
        fields = (
            "id",
            "letter",
            "name",
            "description",
            "topic",
            )
        
# Вывод списка критериев оценивания для DP
class CriterionListSerializer(serializers.ModelSerializer):
    discipline = IbDisciplineDpSerializer()
    class Meta:
        model = Criterion
        fields = (
            "id",
            "name",
            "letter",
            "discipline",
            )

# Список категорий ATL для MYP
class AtlCategoryDpSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlCategory
        fields = (
            "id",
            "name",
            "name_rus",
            )

# Список кластеров ATL для MYP
class AtlClusterDpSerializer(serializers.ModelSerializer):
    category = AtlCategoryDpSerializer()
    class Meta:
        model = AtlCluster
        fields = (
            "id",
            "name",
            "name_rus",
            "category",
            )
                
# Вывод списка критериев оценивания для DP
class DpAtlSkillListSerializer(serializers.ModelSerializer):
    cluster = AtlClusterDpSerializer()
    class Meta:
        model = DpAtlSkill
        fields = (
            "id",
            "name",
            "name_rus",
            "cluster",
            )
        
# Вывод списка исследовательских вопросов в юните DP
class DpInquiryQuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpInquiryQuestion
        fields = (
            "id",
            "question",
            "type",
            "unit",
            )
        
# Создание и редактирование исследовательских вопросов в юните DP
class DpInquiryQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpInquiryQuestion
        fields = '__all__'

# Вывод списка пунктов развития ATL-навыков в юните DP
class DpAtlDevelopListSerializer(serializers.ModelSerializer):
    atl = DpAtlSkillListSerializer()
    class Meta:
        model = DpAtlDevelop
        fields = (
            "id",
            "atl",
            "action",
            "unit",
            )
        
# Создание и редактирование пункта развития ATL-навыков в юните DP
class DpAtlDevelopUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpAtlDevelop
        fields = '__all__'

# Список качеств портрета студента IB
class LearnerProfileDpSerializer(serializers.ModelSerializer):
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
    profile = LearnerProfileDpSerializer()
    class Meta:
        model = IbProfileDevelop
        fields = (
            "id",
            "profile",
            "description",
            "unit",
            )
        
# Список постов рефлексии по юниту
class UnitReflectionPostMypSerializer(serializers.ModelSerializer):
    author = UserDpSerializer()
    class Meta:
        model = UnitReflectionPost
        fields = (
            "id",
            "post",
            "type",
            "author",
            "unit",
            )


# Список предметов
class SubjectDpSerializer(serializers.ModelSerializer):
    group_ib = IbSubjectGroupDpSerializer()
    discipline_ib = IbDisciplineDpSerializer()
    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "group_ib",
            "discipline_ib",
            )

# Вывод списка планнеров в DP
class DpUnitPlannerListSerializer(serializers.ModelSerializer):
    teachers = UserDpSerializer(many=True)
    authors = UserDpSerializer(many=True)
    year = StudyYearDpSerializer()
    class Meta:
        model = DpUnitPlanner
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
        )

# Подробный просмотр планера в DP
class DpUnitPlannerRetrieveSerializer(serializers.ModelSerializer):
    teachers = UserDpSerializer(many=True)
    authors = UserDpSerializer(many=True)
    year = StudyYearDpSerializer()
    subject = SubjectDpSerializer()
    aims = DpAimListSerializer(many=True)
    objectives = DpObjectiveListSerializer(many=True)
    syllabus_content = CourseContentListSerializer(many=True)
    criteria = CriterionListSerializer(many=True)
    inquiry_questions = DpInquiryQuestionListSerializer(many=True)
    atl_develops = DpAtlDevelopListSerializer(many=True)
    ibprofiles = IbProfileDevelopMypSerializer(many=True)
    reflection_posts = UnitReflectionPostMypSerializer(many=True)
    class Meta:
        model = DpUnitPlanner
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
            "levels",
            "transfer_goals",
            "essential_understandings",
            "misunderstandings",
            "aims",
            "objectives",
            "syllabus_content",
            "content",
            "skills",
            "concepts",
            "international_mindedness",
            "academic_integrity",
            "infocom_technology",
            "language_learning",
            "language_learning_text",
            "ee_connections",
            "tok_connections",
            "tok_connections_text",
            "cas_connections",
            "cas_connections_text",
            "formative_assessment",
            "summative_assessment",
            "internal_assessment",
            "peer_self_assessment",
            "criteria",
            "criteria_text",
            "prior_experiences",
            "pedagogical_approaches",
            "student_expectations",
            "feedback",
            "learning_process",
            "learning_process_text",
            "differentiation",
            "differentiation_text",
            "learning_experiences",
            "resources",
            "cross_curricular_links",
            "co_curricular_links",
            "work_well",
            "work_well_not",
            "notes",
            "inquiry_questions",
            "atl_develops",
            "ibprofiles",
            "reflection_posts",
        )

# Создание планера в DP
class DpUnitPlannerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpUnitPlanner
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
        )

# Редактирование планера в DP
class DpUnitPlannerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpUnitPlanner
        fields = '__all__'