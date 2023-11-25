from rest_framework import serializers

from apps.syllabus.models import (
    Syllabus,
    Course,
    CourseChapter,
    CourseTopic,
)

from apps.ibo.models import (
    UnitPlanerBaseModel
)

from general.models import (
    User,
    StudyYear
)

from apps.curriculum.models import (
    Subject
)

# Список тем курса учебного предмета
class CourseTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTopic
        fields = (
            "id", 
            "number",
            "name",
            "description",
            "hours",
            )

# Список тем курса учебного предмета
class UnitPlanerBaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitPlanerBaseModel
        fields = (
            "id", 
            "title",
            "pypunitplanner",
            "mypunitplanner",
            "dpunitplanner",
            )

# Список разделов курса учебного предмета
class CourseChapterSerializer(serializers.ModelSerializer):
    topics = CourseTopicSerializer(many=True)
    unit = UnitPlanerBaseModelSerializer()
    class Meta:
        model = CourseChapter
        fields = (
            "id", 
            "number",
            "name",
            "description",
            "hours",
            "unit",
            "topics",
            )

# Список курсов учебного предмета в году
class CourseSerializer(serializers.ModelSerializer):
    chapters = CourseChapterSerializer(many=True)
    class Meta:
        model = Course
        fields = (
            "id", 
            "syllabus", 
            "year",
            "chapters"
            )

# Список учебных параллелей
class StudyYearSyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            )

# Список пользователей
class UserSyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            )

# Список предметов
class SubjectSyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "group_ib",
            "discipline_ib",
            )

# Вывод списка учебных курсов по предмету
class SyllabusListSerializer(serializers.ModelSerializer):
    subject = SubjectSyllabusSerializer()
    years = StudyYearSyllabusSerializer(many=True)
    authors = UserSyllabusSerializer(many=True)
    class Meta:
        model = Syllabus
        fields = (
            "id", 
            "authors",
            "subject", 
            "years",
            "file",
            )
        
# Подробный просмотр учебного курса по предмету
class SyllabusRetrieveSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)
    years = StudyYearSyllabusSerializer(many=True)
    authors = UserSyllabusSerializer(many=True)
    subject = SubjectSyllabusSerializer()
    class Meta:
        model = Syllabus
        fields = (
            "id", 
            "authors",
            "subject", 
            "years",
            "file",
            "courses"
            )
        
# Вывод списка тем курса учебного предмета
class CourseTopicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTopic
        fields = (
            "id", 
            "number",
            "name",
            "description",
            "hours",
            )

# Создание и редактирование списка тем курса учебного предмета
class CourseTopicUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTopic
        fields = '__all__'