from rest_framework import serializers

from apps.units.pyp.models import (
    PypUnitPlanner,
    TransdisciplinaryTheme,
    PypKeyConcept,
    PypAtlGroup,
    PypAtlSkill,
    PypLinesOfInquiry,
    PypRelatedConcept,
    PypAtlDevelop,
    PypAtlCluster
    )

from apps.ibo.models import (
    AtlCategory,
    LearnerProfile,
    IbProfileDevelop,
    UnitReflectionPost,
)

from general.models import (
    User,
    StudyYear,
    )

# Вывод списка трансдисциплинарных тем для PYP
class TransdisciplinaryThemeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransdisciplinaryTheme
        fields = (
            "id",
            "name",
            "name_rus",
            "description",
            "description_rus",
            )
        
# Вывод списка ключевых концептов в PYP
class PypKeyConceptListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PypKeyConcept
        fields = (
            "id",
            "name",
            "name_rus",
            "description",
            "description_rus",
            )

# Вывод списка категорий ATL
class AtlCategoryPypSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlCategory
        fields = (
            "id",
            "name",
            "name_rus",
            )

# Вывод списка кластеров ATL
class PypAtlClusterListSerializer(serializers.ModelSerializer):
    category = AtlCategoryPypSerializer()
    class Meta:
        model = PypAtlCluster
        fields = (
            "id",
            "name",
            "name_rus",
            "category",
            )

# Вывод списка групп навыков ATL в PYP
class PypAtlGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PypAtlGroup
        fields = (
            "id",
            "name",
            "name_rus",
            "cluster",
            )
        
# Вывод списка навыков ATL в PYP
class PypAtlSkillListSerializer(serializers.ModelSerializer):
    group = PypAtlGroupListSerializer()
    cluster = PypAtlClusterListSerializer()
    class Meta:
        model = PypAtlSkill
        fields = (
            "id",
            "name",
            "name_rus",
            "group",
            "cluster",
            )
        
# Вывод списка линий исследования в юните PYP
class PypLinesOfInquiryListSerializer(serializers.ModelSerializer):
    key_concept = PypKeyConceptListSerializer()
    class Meta:
        model = PypLinesOfInquiry
        fields = (
            "id",
            "name",
            "key_concept",
            "unit",
            )
        
# Создание и редактирование линий исследования в юните PYP
class PypLinesOfInquiryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PypLinesOfInquiry
        fields = '__all__'

# Вывод списка сопутствующих понятий в юните PYP
class PypRelatedConceptListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PypRelatedConcept
        fields = (
            "id",
            "name",
            "unit",
            )
        
# Создание и редактирование сопутствующего понятия в юните PYP
class PypRelatedConceptUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PypRelatedConcept
        fields = '__all__'

# Вывод списка пунктов развития ATL-навыков в юните PYP
class PypAtlDevelopListSerializer(serializers.ModelSerializer):
    category = AtlCategoryPypSerializer()
    cluster = PypAtlClusterListSerializer()
    skill = PypAtlSkillListSerializer()
    class Meta:
        model = PypAtlDevelop
        fields = (
            "id",
            "cluster",
            "category",
            "skill",
            "action",
            "unit",
            )
        
# Создание и редактирование пункта развития ATL-навыков в юните PYP
class PypAtlDevelopUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PypAtlDevelop
        fields = '__all__'
    
# Список пользователей
class UserPypSerializer(serializers.ModelSerializer):
    short_name = serializers.CharField(source='get_short_name', read_only=True)
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "short_name",
            )

# Список учебных параллелей
class StudyYearPypSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            "name",
            )

# Список качеств портрета студента IB
class LearnerProfilePypSerializer(serializers.ModelSerializer):
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
class IbProfileDevelopPypSerializer(serializers.ModelSerializer):
    profile = LearnerProfilePypSerializer()
    class Meta:
        model = IbProfileDevelop
        fields = (
            "id",
            "profile",
            "description",
            "unit",
            )

# Список постов рефлексии по юниту
class UnitReflectionPostPypSerializer(serializers.ModelSerializer):
    author = UserPypSerializer()
    class Meta:
        model = UnitReflectionPost
        fields = (
            "id",
            "post",
            "type",
            "author",
            "unit",
            )

# Вывод списка планнеров в PYP
class PypUnitPlannerListSerializer(serializers.ModelSerializer):
    teachers = UserPypSerializer(many=True)
    year = StudyYearPypSerializer()
    transdisciplinary_theme = TransdisciplinaryThemeListSerializer()
    class Meta:
        model = PypUnitPlanner
        fields = (
            "id",
            "order",
            "title",
            "teachers",
            "year",
            "hours",
            "description",
            "created_at",
            "updated_at",
            "transdisciplinary_theme",
            )
        
# Подробный просмотр планнера в PYP
class PypUnitPlannerRetrieveSerializer(serializers.ModelSerializer):
    teachers = UserPypSerializer(many=True)
    authors = UserPypSerializer(many=True)
    year = StudyYearPypSerializer()
    transdisciplinary_theme = PypKeyConceptListSerializer()
    key_concepts = PypKeyConceptListSerializer(many=True)
    inquiry_lines = PypLinesOfInquiryListSerializer(many=True)
    related_concepts = PypRelatedConceptListSerializer(many=True)
    ibprofiles = IbProfileDevelopPypSerializer(many=True)
    atl_develops = PypAtlDevelopListSerializer(many=True)
    ibprofiles = IbProfileDevelopPypSerializer(many=True)
    reflection_posts = UnitReflectionPostPypSerializer(many=True)
    class Meta:
        model = PypUnitPlanner
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
            "transdisciplinary_theme",
            "central_idea",
            "key_concepts",
            "action",
            "reflections_initial",
            "prior_learning",
            "conncetions",
            "learning_goals",
            "questions_teacher",
            "questions_student",
            "engaging_learning",
            "supporting_agency",
            "questions_all",
            "ongoing_assessment",
            "resources",
            "peer_self_assessment",
            "reflections_ongoing",
            "reflections_additional",
            "notes",
            "ibprofiles",
            "inquiry_lines",
            "related_concepts",
            "atl_develops",
            "ibprofiles",
            "reflection_posts",
            "teacher_roles",
            )
        
# Создание планнера в PYP
class PypUnitPlannerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PypUnitPlanner
        fields = (
            "id",
            "order",
            "title",
            "teachers",
            "year",
            "hours",
            "transdisciplinary_theme",
            )
        
# Обновление планнера в PYP
class PypUnitPlannerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PypUnitPlanner
        fields = '__all__'
    # def update(self, instance, validated_data):
    #     if 'teachers' in validated_data:
    #         if not validated_data['teachers']:
    #             # Если список пуст, очищаем связь
    #             instance.teachers.clear()
    #         else:
    #             # Если список не пуст, обновляем связь
    #             instance.teachers.set(validated_data['teachers'])
    #         validated_data.pop('teachers')

    #     return super().update(instance, validated_data)