from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from apps.report.serializers import (
    ReportPeriodListSerializer,
    ReportCriterionListSerializer,
    ReportCriterionUpdateSerializer,
    ReportCriterionLevelSerializer,
    ReportCriterionAchievementListSerializer,
    ReportCriterionAchievementUpdateSerializer,
    ReportPrimaryTopicListSerializer,
    ReportPrimaryTopicUpdateSerializer,
    ReportTeacherPrimaryUpdateSerializer, 
    ReportTeacherPrimaryRetrieveSerializer,
    ReportTeacherPrimaryListSerializer,
    ReportSecondaryCriterionListSerializer,
    ReportSecondaryCriterionUpdateSerializer,
    ReportSecondaryLevelListSerializer,
    ReportSecondaryLevelUpdateSerializer,
    ReportTeacherSecondaryListSerializer,
    ReportTeacherSecondaryRetrieveSerializer,
    ReportTeacherSecondaryUpdateSerializer,
    ReportTeacherHighListSerializer,
    ReportTeacherHighRetrieveSerializer,
    ReportTeacherHighUpdateSerializer,
    ReportIbProfileListSerializer,
    ReportIbProfileUpdateSerializer,
    ReportMentorListSerializer,
    ReportMentorRetrieveSerializer,
    ReportMentorUpdateSerializer,
    ReportPrimaryUnitListSerializer,
    ReportPrimaryUnitUpdateSerializer,
    ReportMentorPrimaryListSerializer,
    ReportMentorPrimaryRetrieveSerializer,
    ReportMentorPrimaryUpdateSerializer,
    ReportExtraListSerializer,
    ReportExtraRetrieveSerializer,
    ReportExtraUpdateSerializer,
    UserListReportExtraSerializer,
    UserListReportMentorPrimarySerializer,
    UserListReportMentorSerializer
)

from apps.report.services import (
    get_report_period_queryset,
    get_report_criterion_queryset,
    get_report_criterion_level_queryset,
    get_report_criterion_achievement_queryset,
    get_report_primary_achievement_queryset,
    get_report_teacher_primary_queryset,
    get_report_secondary_criterion_queryset,
    get_report_secondary_level_queryset,
    get_report_teacher_secondary_queryset,
    get_report_teacher_high_queryset,
    get_report_ibprofile_queryset,
    get_report_mentor_queryset,
    get_report_primary_unit_queryset,
    get_report_mentor_primary_queryset,
    get_report_extra_queryset,
    get_user_report_extra_queryset,
    get_user_report_mentor_primary_queryset,
    get_user_report_mentor_queryset
)

from apps.report.filters import (
    ReportPeriodFilter,
    ReportCriterionFilter,
    ReportCriterionLevelFilter,
    ReportCriterionAchievementFilter,
    ReportPrimaryTopicFilter,
    ReportTeacherPrimaryFilter,
    ReportSecondaryCriterionFilter,
    ReportSecondaryLevelFilter,
    ReportTeacherSecondaryFilter,
    ReportTeacherHighFilter,
    ReportIbProfileFilter,
    ReportMentorFilter,
    ReportPrimaryUnitFilter,
    ReportMentorPrimaryFilter,
    ReportExtraFilter,
    UserFilter
)

# Отчётные периоды для репортов: список
@extend_schema_view(
    list=extend_schema(summary='Список отчётных периодов для репортов', tags=['Репорты: Периоды']),
    )
class ReportPeriodViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_period_queryset()
    serializer_class = ReportPeriodListSerializer
    filterset_class = ReportPeriodFilter
    pagination_class = None

# Критерии для репортов: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка критериев для репортов', tags=['Репорты: Критерии']),
    create=extend_schema(summary='Создание критериев для репортов', tags=['Репорты: Критерии']),
    update=extend_schema(summary='Обновление критериев для репортов', tags=['Репорты: Критерии']),
    destroy=extend_schema(summary='Удаление критериев для репортов', tags=['Репорты: Критерии']),
    )
class ReportCriterionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_criterion_queryset()
    filterset_class = ReportCriterionFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ReportCriterionListSerializer
        return ReportCriterionUpdateSerializer
    
    
# Уровни достижений по критериям для репортов: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка уровней достижений по критериям для репортов', tags=['Репорты: Уровни достижений по критерию']),
    create=extend_schema(summary='Создание уровня достижений по критериям для репортов', tags=['Репорты: Уровни достижений по критерию']),
    update=extend_schema(summary='Обновление уровня достижений по критериям для репортов', tags=['Репорты: Уровни достижений по критерию']),
    destroy=extend_schema(summary='Удаление уровня достижений по критериям для репортов', tags=['Репорты: Уровни достижений по критерию']),
    )
class ReportCriterionLevelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_criterion_level_queryset()
    filterset_class = ReportCriterionLevelFilter
    serializer_class = ReportCriterionLevelSerializer

# Достижения по критериям в репорте: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка достижений по критериям в репорте', tags=['Репорты: Учителя. Достижения по своим критериям']),
    create=extend_schema(summary='Создание достижения по критериям в репорте', tags=['Репорты: Учителя. Достижения по своим критериям']),
    update=extend_schema(summary='Обновление достижения по критериям в репорте', tags=['Репорты: Учителя. Достижения по своим критериям']),
    destroy=extend_schema(summary='Удаление достижения по критериям в репорте', tags=['Репорты: Учителя. Достижения по своим критериям']),
    )
class ReportCriterionAchievementViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_criterion_achievement_queryset()
    filterset_class = ReportCriterionAchievementFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ReportCriterionAchievementListSerializer
        return ReportCriterionAchievementUpdateSerializer
    
    # Переопределение метода create для массового создания объектов
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if isinstance(serializer.instance, list):
            data = [ReportCriterionAchievementListSerializer(instance).data for instance in serializer.instance]
        else:
            data = ReportCriterionAchievementListSerializer(serializer.instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
    # Переопределение метода partial_update для ответа с другим сериализатором
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        detail_serializer = ReportCriterionAchievementListSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
    
# Репорты учителя в начальной школе: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов учителя в начальной школе', tags=['Репорты: Учителя НШ']),
    create=extend_schema(summary='Создание репорта учителя в начальной школе', tags=['Репорты: Учителя НШ']),
    retrieve=extend_schema(summary='Просмотр репорта учителя в начальной школе', tags=['Репорты: Учителя НШ']),
    update=extend_schema(summary='Обновление репорта учителя в начальной школе', tags=['Репорты: Учителя НШ']),
    partial_update=extend_schema(summary='Частичное обновление репорта учителя в начальной школе', tags=['Репорты: Учителя НШ']),
    destroy=extend_schema(summary='Удаление репорта учителя в начальной школе', tags=['Репорты: Учителя НШ']),
    )
class ReportTeacherPrimaryViewSet(ModelViewSet):
    queryset = get_report_teacher_primary_queryset()
    filterset_class = ReportTeacherPrimaryFilter
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "list":
            return ReportTeacherPrimaryListSerializer
        elif self.action == "retrieve":
            return ReportTeacherPrimaryRetrieveSerializer
        return ReportTeacherPrimaryUpdateSerializer
    
    # Переопределение метода partial_update для ответа с другим сериализатором
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        detail_serializer = ReportTeacherPrimaryListSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)

# Достижения по темам в репорте НШ: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка достижений по темам в репорте НШ', tags=['Репорты: Учителя НШ. Достижения по темам']),
    create=extend_schema(summary='Создание достижения по темам в репорте НШ', tags=['Репорты: Учителя НШ. Достижения по темам']),
    update=extend_schema(summary='Обновление достижения по темам в репорте НШ', tags=['Репорты: Учителя НШ. Достижения по темам']),
    partial_update=extend_schema(summary='Частичное обновление достижения по темам в репорте НШ', tags=['Репорты: Учителя НШ. Достижения по темам']),
    destroy=extend_schema(summary='Удаление достижения по темам в репорте НШ', tags=['Репорты: Учителя НШ. Достижения по темам']),
    )
class ReportPrimaryTopicViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_primary_achievement_queryset()
    filterset_class = ReportPrimaryTopicFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ReportPrimaryTopicListSerializer
        return ReportPrimaryTopicUpdateSerializer
    
    # Переопределение метода create для массового создания объектов
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if isinstance(serializer.instance, list):
            data = [ReportPrimaryTopicListSerializer(instance).data for instance in serializer.instance]
        else:
            data = ReportPrimaryTopicListSerializer(serializer.instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
    # Переопределение метода partial_update для ответа с другим сериализатором
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        detail_serializer = ReportPrimaryTopicListSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
    
# Баллы по критериям в репорте СрШ: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка баллов по критериям в репорте СрШ', tags=['Репорты: Учителя СрШ. Баллы по критериям']),
    create=extend_schema(summary='Создание балла по критериям в репорте СрШ', tags=['Репорты: Учителя СрШ. Баллы по критериям']),
    update=extend_schema(summary='Обновление балла по критериям в репорте СрШ', tags=['Репорты: Учителя СрШ. Баллы по критериям']),
    destroy=extend_schema(summary='Удаление балла по критериям в репорте СрШ', tags=['Репорты: Учителя СрШ. Баллы по критериям']),
    )
class ReportSecondaryCriterionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_secondary_criterion_queryset()
    filterset_class = ReportSecondaryCriterionFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ReportSecondaryCriterionListSerializer
        return ReportSecondaryCriterionUpdateSerializer
    
    # Переопределение метода partial_update для ответа с другим сериализатором
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        detail_serializer = ReportSecondaryCriterionListSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
    
# Предметные достижения в репорте СрШ: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка предметных достижений в репорте СрШ', tags=['Репорты: Учителя СрШ. Предметные достижения']),
    create=extend_schema(summary='Создание предметного достижения в репорте СрШ', tags=['Репорты: Учителя СрШ. Предметные достижения']),
    update=extend_schema(summary='Обновление предметного достижения в репорте СрШ', tags=['Репорты: Учителя СрШ. Предметные достижения']),
    destroy=extend_schema(summary='Удаление предметного достижения в репорте СрШ', tags=['Репорты: Учителя СрШ. Предметные достижения']),
    )
class ReportSecondaryLevelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_secondary_level_queryset()
    filterset_class = ReportSecondaryLevelFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ReportSecondaryLevelListSerializer
        return ReportSecondaryLevelUpdateSerializer
    
# Репорты учителя в средней школе: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов учителя в средней школе', tags=['Репорты: Учителя СрШ']),
    create=extend_schema(summary='Создание репорта учителя в средней школе', tags=['Репорты: Учителя СрШ']),
    retrieve=extend_schema(summary='Просмотр репорта учителя в средней школе', tags=['Репорты: Учителя СрШ']),
    update=extend_schema(summary='Обновление репорта учителя в средней школе', tags=['Репорты: Учителя СрШ']),
    partial_update=extend_schema(summary='Частичное обновление репорта учителя в средней школе', tags=['Репорты: Учителя СрШ']),
    destroy=extend_schema(summary='Удаление репорта учителя в средней школе', tags=['Репорты: Учителя СрШ']),
    )
class ReportTeacherSecondaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_teacher_secondary_queryset()
    filterset_class = ReportTeacherSecondaryFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return ReportTeacherSecondaryListSerializer
        elif self.action == "retrieve":
            return ReportTeacherSecondaryRetrieveSerializer
        return ReportTeacherSecondaryUpdateSerializer
    
    # Переопределение метода partial_update для ответа с другим сериализатором
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        detail_serializer = ReportTeacherSecondaryRetrieveSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
    

# Репорты учителя в старшей школе: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов учителя в старшей школе', tags=['Репорты: Учителя СтШ']),
    create=extend_schema(summary='Создание репорта учителя в старшей школе', tags=['Репорты: Учителя СтШ']),
    retrieve=extend_schema(summary='Просмотр репорта учителя в старшей школе', tags=['Репорты: Учителя СтШ']),
    update=extend_schema(summary='Обновление репорта учителя в старшей школе', tags=['Репорты: Учителя СтШ']),
    partial_update=extend_schema(summary='Частичное обновление репорта учителя в старшей школе', tags=['Репорты: Учителя СтШ']),
    destroy=extend_schema(summary='Удаление репорта учителя в старшей школе', tags=['Репорты: Учителя СтШ']),
    )
class ReportTeacherHighViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_teacher_high_queryset()
    filterset_class = ReportTeacherHighFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return ReportTeacherHighListSerializer
        elif self.action == "retrieve":
            return ReportTeacherHighRetrieveSerializer
        return ReportTeacherHighUpdateSerializer
    
    # Переопределение метода partial_update для ответа с другим сериализатором
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        detail_serializer = ReportTeacherHighListSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
    
# Оценки профиля студента в репорте классного руководителя: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка оценок профилей студента в репортах классного руководителя', tags=['Репорты: Классный руководитель. Развитие профиля студента']),
    create=extend_schema(summary='Создание оценки профиля студента в репортах классного руководителя', tags=['Репорты: Классный руководитель. Развитие профиля студента']),
    update=extend_schema(summary='Обновление оценки профиля студента в репортах классного руководителя', tags=['Репорты: Классный руководитель. Развитие профиля студента']),
    destroy=extend_schema(summary='Удаление оценки профиля студента в репортах классного руководителя', tags=['Репорты: Классный руководитель. Развитие профиля студента']),
    )
class ReportIbProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_ibprofile_queryset()
    filterset_class = ReportIbProfileFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ReportIbProfileListSerializer
        return ReportIbProfileUpdateSerializer
    
# Репорты классного руководителя: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов классного руководителя', tags=['Репорты: Классный руководитель']),
    create=extend_schema(summary='Создание репорта классного руководителя', tags=['Репорты: Классный руководитель']),
    retrieve=extend_schema(summary='Просмотр репорта классного руководителя', tags=['Репорты: Классный руководитель']),
    update=extend_schema(summary='Обновление репорта классного руководителя', tags=['Репорты: Классный руководитель']),
    partial_update=extend_schema(summary='Частичное обновление репорта классного руководителя', tags=['Репорты: Классный руководитель']),
    destroy=extend_schema(summary='Удаление репорта классного руководителя', tags=['Репорты: Классный руководитель']),
    )
class ReportMentorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_mentor_queryset()
    filterset_class = ReportMentorFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return ReportMentorListSerializer
        elif self.action == "retrieve":
            return ReportMentorRetrieveSerializer
        return ReportMentorUpdateSerializer
    

# Результаты юнита в репорте классного руководителя НШ: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка результатов юнита в репорте классного руководителя НШ', tags=['Репорты: Классный руководитель НШ. Результаты юнита']),
    create=extend_schema(summary='Создание результата юнита в репорте классного руководителя НШ', tags=['Репорты: Классный руководитель НШ. Результаты юнита']),
    update=extend_schema(summary='Обновление результата юнита в репорте классного руководителя НШ', tags=['Репорты: Классный руководитель НШ. Результаты юнита']),
    destroy=extend_schema(summary='Удаление результата юнита в репорте классного руководителя НШ', tags=['Репорты: Классный руководитель НШ. Результаты юнита']),
    )
class ReportPrimaryUnitViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_primary_unit_queryset()
    filterset_class = ReportPrimaryUnitFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ReportPrimaryUnitListSerializer
        return ReportPrimaryUnitUpdateSerializer
    
# Репорты классного руководителя начальной школы: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов классного руководителя НШ', tags=['Репорты: Классный руководитель НШ']),
    create=extend_schema(summary='Создание репорта классного руководителя НШ', tags=['Репорты: Классный руководитель НШ']),
    retrieve=extend_schema(summary='Просмотр репорта классного руководителя НШ', tags=['Репорты: Классный руководитель НШ']),
    update=extend_schema(summary='Обновление репорта классного руководителя НШ', tags=['Репорты: Классный руководитель НШ']),
    partial_update=extend_schema(summary='Частичное обновление репорта классного руководителя НШ', tags=['Репорты: Классный руководитель НШ']),
    destroy=extend_schema(summary='Удаление репорта классного руководителя НШ', tags=['Репорты: Классный руководитель НШ']),
    )
class ReportMentorPrimaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_mentor_primary_queryset()
    filterset_class = ReportMentorPrimaryFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return ReportMentorPrimaryListSerializer
        elif self.action == "retrieve":
            return ReportMentorPrimaryRetrieveSerializer
        return ReportMentorPrimaryUpdateSerializer
    
# Репорты дополнительных сотрудников класса: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов классного сотрудника класса', tags=['Репорты: Сотрудники класса']),
    create=extend_schema(summary='Создание репорта классного сотрудника класса', tags=['Репорты: Сотрудники класса']),
    retrieve=extend_schema(summary='Просмотр репорта классного сотрудника класса', tags=['Репорты: Сотрудники класса']),
    update=extend_schema(summary='Обновление репорта классного сотрудника класса', tags=['Репорты: Сотрудники класса']),
    partial_update=extend_schema(summary='Частичное обновление репорта сотрудника класса', tags=['Репорты: Сотрудники класса']),
    destroy=extend_schema(summary='Удаление репорта классного сотрудника класса', tags=['Репорты: Сотрудники класса']),
    )
class ReportExtraViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_extra_queryset()
    filterset_class = ReportExtraFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return ReportExtraListSerializer
        elif self.action == "retrieve":
            return ReportExtraRetrieveSerializer
        return ReportExtraUpdateSerializer
    

# Список студентов с репортами сотрудников: список, 
@extend_schema_view(
    list=extend_schema(summary='Вывод списка студентов с репортами сотрудников класса', tags=['Репорты: Студенты с репортами сотрудников класса']),
    )
class UserReportExtraViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilter
    pagination_class = None

    def get_queryset(self):
        period = self.request.query_params.get('report_period', None)
        group = self.request.query_params.get('report_group', None)
        return get_user_report_extra_queryset(group, period)
    
    def get_serializer_class(self):
        return UserListReportExtraSerializer
    
# Список студентов с репортами классных руководитедей начальной школы: список, 
@extend_schema_view(
    list=extend_schema(summary='Вывод списка студентов с репортами классных руководителей начальной школы', tags=['Репорты: Студенты с репортами классных руководителей']),
    )
class UserReportMentorPrimaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilter
    pagination_class = None

    def get_queryset(self):
        period = self.request.query_params.get('report_period', None)
        group = self.request.query_params.get('report_group', None)
        return get_user_report_mentor_primary_queryset(group, period)
    
    def get_serializer_class(self):
        return UserListReportMentorPrimarySerializer
    

# Список студентов с репортами классных руководитедей: список, 
@extend_schema_view(
    list=extend_schema(summary='Вывод списка студентов с репортами классных руководителей', tags=['Репорты: Студенты с репортами классных руководителей']),
    )
class UserReportMentorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilter
    pagination_class = None

    def get_queryset(self):
        period = self.request.query_params.get('report_period', None)
        group = self.request.query_params.get('report_group', None)
        return get_user_report_mentor_queryset(group, period)
    
    def get_serializer_class(self):
        return UserListReportMentorSerializer