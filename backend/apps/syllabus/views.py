from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.syllabus.services import (
    get_syllabus_list_queryset,
    get_course_topic_queryset,
    get_course_chapter_queryset,
    get_course_queryset,
)

from apps.syllabus.serializers import (
    SyllabusListSerializer,
    CourseTopicListSerializer,
    CourseTopicUpdateSerializer,
    CourseChapterListSerializer,
    CourseChapterUpdateSerializer,
    CourseListSerializer,
)

from apps.syllabus.filters import (
    SyllabusFilter,
    CourseTopicFilter,
    CourseChapterFilter,
    CourseFilter,
)

#TODO: Добавить просмотр и редактирование раздела учебного курса

# Учебные курсы по предмету: список и просмотр
@extend_schema_view(
    list=extend_schema(summary='Вывод списка учебных курсов по предмету', tags=['Курсы: Общий курс']),
    retrieve=extend_schema(summary='Просмотр учебного курса по предмету', tags=['Курсы: Общий курс']),
    )
class SyllabusViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_syllabus_list_queryset()
    serializer_class = SyllabusListSerializer
    filterset_class = SyllabusFilter

# Курсы по предмету: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка курсов по предмету', tags=['Курсы: Курс учебного года']),
    )
class CourseViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_course_queryset()
    serializer_class = CourseListSerializer
    filterset_class = CourseFilter

# Разделы курсов по предмету: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка разделов курсов по предмету', tags=['Курсы: Разделы']),
    create=extend_schema(summary='Создание раздела курса по предмету', tags=['Курсы: Разделы']),
    update=extend_schema(summary='Обновление раздела курса по предмету', tags=['Курсы: Разделы']),
    destroy=extend_schema(summary='Удаление раздела курса по предмету', tags=['Курсы: Разделы']),
    )
class CourseChapterViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_course_chapter_queryset()
    filterset_class = CourseChapterFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return CourseChapterListSerializer
        return CourseChapterUpdateSerializer

# Темы курсов по предмету: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка тем курсов по предмету', tags=['Курсы: Темы']),
    create=extend_schema(summary='Создание темы курса по предмету', tags=['Курсы: Темы']),
    update=extend_schema(summary='Обновление темы курса по предмету', tags=['Курсы: Темы']),
    destroy=extend_schema(summary='Удаление темы курса по предмету', tags=['Курсы: Темы']),
    )
class CourseTopicViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_course_topic_queryset()
    filterset_class = CourseTopicFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return CourseTopicListSerializer
        return CourseTopicUpdateSerializer