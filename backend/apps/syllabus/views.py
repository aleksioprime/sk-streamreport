from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.syllabus.services import (
    get_syllabus_list_queryset,
    get_course_topic_queryset
)

from apps.syllabus.serializers import (
    SyllabusListSerializer,
    CourseTopicListSerializer,
    CourseTopicUpdateSerializer
)

from apps.syllabus.filters import (
    SyllabusFilter,
    CourseTopicFilter
)

#TODO: Добавить просмотр и редактирование раздела учебного курса

# Учебные курсы по предмету: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка учебных курсов по предмету', tags=['Курсы: Общий курс']),
    retrieve=extend_schema(summary='Просмотр учебного курса по предмету', tags=['Курсы: Общий курс']),
    )
class SyllabusViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_syllabus_list_queryset()
    serializer_class = SyllabusListSerializer
    filterset_class = SyllabusFilter

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