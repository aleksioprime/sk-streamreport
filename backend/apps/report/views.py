from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated


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
)

from apps.report.services import (
    get_report_report_queryset,
    get_report_criterion_queryset,
    get_report_criterion_level_queryset,
    get_report_criterion_achievement_queryset,
    get_report_primary_achievement_queryset,
    get_report_teacher_primary_queryset,
    get_report_secondary_criterion_queryset,
    get_report_secondary_level_queryset,
    get_report_teacher_secondary_queryset,
    get_report_teacher_high_queryset
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
    ReportTeacherHighFilter
)

# Отчётные периоды для репортов: список
@extend_schema_view(
    list=extend_schema(summary='Список отчётных периодов для репортов', tags=['Отчётные периоды репортов']),
    )
class ReportPeriodViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_report_queryset()
    serializer_class = ReportPeriodListSerializer
    filter_class = ReportPeriodFilter

# Критерии для репортов: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка критериев для репортов', tags=['Критерии для репортов']),
    create=extend_schema(summary='Создание критериев для репортов', tags=['Критерии для репортов']),
    update=extend_schema(summary='Обновление критериев для репортов', tags=['Критерии для репортов']),
    destroy=extend_schema(summary='Удаление критериев для репортов', tags=['Критерии для репортов']),
    )
class ReportCriterionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_criterion_queryset()
    filter_class = ReportCriterionFilter
    def get_serializer_class(self):
        if self.action == "list":
            return ReportCriterionListSerializer
        return ReportCriterionUpdateSerializer
    
# Уровни достижений по критериям для репортов: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка уровней достижений по критериям для репортов', tags=['Уровни достижений по критериям']),
    create=extend_schema(summary='Создание уровня достижений по критериям для репортов', tags=['Уровни достижений по критериям']),
    update=extend_schema(summary='Обновление уровня достижений по критериям для репортов', tags=['Уровни достижений по критериям']),
    destroy=extend_schema(summary='Удаление уровня достижений по критериям для репортов', tags=['Уровни достижений по критериям']),
    )
class ReportCriterionLevelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_criterion_level_queryset()
    filter_class = ReportCriterionLevelFilter
    serializer_class = ReportCriterionLevelSerializer

# Достижения по критериям в репорте: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка достижений по критериям в репорте', tags=['Достижения по критериям в репорте']),
    create=extend_schema(summary='Создание достижения по критериям в репорте', tags=['Достижения по критериям в репорте']),
    update=extend_schema(summary='Обновление достижения по критериям в репорте', tags=['Достижения по критериям в репорте']),
    destroy=extend_schema(summary='Удаление достижения по критериям в репорте', tags=['Достижения по критериям в репорте']),
    )
class ReportCriterionAchievementViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_criterion_achievement_queryset()
    filter_class = ReportCriterionAchievementFilter
    def get_serializer_class(self):
        if self.action == "list":
            return ReportCriterionAchievementListSerializer
        return ReportCriterionAchievementUpdateSerializer
    
# Репорты учителя в начальной школе: список, просмотре, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов учителя в начальной школе', tags=['Репорты учителя НШ']),
    create=extend_schema(summary='Создание репорта учителя в начальной школе', tags=['Репорты учителя НШ']),
    retrieve=extend_schema(summary='Просмотр репорта учителя в начальной школе', tags=['Репорты учителя НШ']),
    update=extend_schema(summary='Обновление репорта учителя в начальной школе', tags=['Репорты учителя НШ']),
    partial_update=extend_schema(summary='Частичное обновление репорта учителя в начальной школе', tags=['Репорты учителя НШ']),
    destroy=extend_schema(summary='Удаление репорта учителя в начальной школе', tags=['Репорты учителя НШ']),
    )
class ReportTeacherPrimaryViewSet(ModelViewSet):
    queryset = get_report_teacher_primary_queryset()
    filter_class = ReportTeacherPrimaryFilter
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ReportTeacherPrimaryListSerializer
        elif self.action == "retrieve":
            return ReportTeacherPrimaryRetrieveSerializer
        return ReportTeacherPrimaryUpdateSerializer

# Достижения по темам в репорте НШ: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка достижений по темам в репорте НШ', tags=['Достижения по темам в репорте НШ']),
    create=extend_schema(summary='Создание достижения по темам в репорте НШ', tags=['Достижения по темам в репорте НШ']),
    update=extend_schema(summary='Обновление достижения по темам в репорте НШ', tags=['Достижения по темам в репорте НШ']),
    destroy=extend_schema(summary='Удаление достижения по темам в репорте НШ', tags=['Достижения по темам в репорте НШ']),
    )
class ReportPrimaryTopicViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_primary_achievement_queryset()
    filter_class = ReportPrimaryTopicFilter
    def get_serializer_class(self):
        if self.action == "list":
            return ReportPrimaryTopicListSerializer
        return ReportPrimaryTopicUpdateSerializer
    
# Баллы по критериям в репорте СрШ: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка баллов по критериям в репорте СрШ', tags=['Баллы по критериям в репорте СрШ']),
    create=extend_schema(summary='Создание балла по критериям в репорте СрШ', tags=['Баллы по критериям в репорте СрШ']),
    update=extend_schema(summary='Обновление балла по критериям в репорте СрШ', tags=['Баллы по критериям в репорте СрШ']),
    destroy=extend_schema(summary='Удаление балла по критериям в репорте СрШ', tags=['Баллы по критериям в репорте СрШ']),
    )
class ReportSecondaryCriterionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_secondary_criterion_queryset()
    filter_class = ReportSecondaryCriterionFilter
    def get_serializer_class(self):
        if self.action == "list":
            return ReportSecondaryCriterionListSerializer
        return ReportSecondaryCriterionUpdateSerializer
    
# Предметные достижения в репорте СрШ: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка предметных достижений в репорте СрШ', tags=['Предметные достижения в репорте СрШ']),
    create=extend_schema(summary='Создание предметного достижения в репорте СрШ', tags=['Предметные достижения в репорте СрШ']),
    update=extend_schema(summary='Обновление предметного достижения в репорте СрШ', tags=['Предметные достижения в репорте СрШ']),
    destroy=extend_schema(summary='Удаление предметного достижения в репорте СрШ', tags=['Предметные достижения в репорте СрШ']),
    )
class ReportSecondaryLevelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_secondary_level_queryset()
    filter_class = ReportSecondaryLevelFilter
    def get_serializer_class(self):
        if self.action == "list":
            return ReportSecondaryLevelListSerializer
        return ReportSecondaryLevelUpdateSerializer
    
# Репорты учителя в средней школе: список, просмотре, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов учителя в средней школе', tags=['Репорты учителя СрШ']),
    create=extend_schema(summary='Создание репорта учителя в средней школе', tags=['Репорты учителя СрШ']),
    retrieve=extend_schema(summary='Просмотр репорта учителя в средней школе', tags=['Репорты учителя СрШ']),
    update=extend_schema(summary='Обновление репорта учителя в средней школе', tags=['Репорты учителя СрШ']),
    partial_update=extend_schema(summary='Частичное обновление репорта учителя в средней школе', tags=['Репорты учителя СрШ']),
    destroy=extend_schema(summary='Удаление репорта учителя в средней школе', tags=['Репорты учителя СрШ']),
    )
class ReportTeacherSecondaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_teacher_secondary_queryset()
    filter_class = ReportTeacherSecondaryFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return ReportTeacherSecondaryListSerializer
        elif self.action == "retrieve":
            return ReportTeacherSecondaryRetrieveSerializer
        return ReportTeacherSecondaryUpdateSerializer
    

# Репорты учителя в старшей школе: список, просмотре, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов учителя в старшей школе', tags=['Репорты учителя СтШ']),
    create=extend_schema(summary='Создание репорта учителя в старшей школе', tags=['Репорты учителя СтШ']),
    retrieve=extend_schema(summary='Просмотр репорта учителя в старшей школе', tags=['Репорты учителя СтШ']),
    update=extend_schema(summary='Обновление репорта учителя в старшей школе', tags=['Репорты учителя СтШ']),
    partial_update=extend_schema(summary='Частичное обновление репорта учителя в старшей школе', tags=['Репорты учителя СтШ']),
    destroy=extend_schema(summary='Удаление репорта учителя в старшей школе', tags=['Репорты учителя СтШ']),
    )
class ReportTeacherHighViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_teacher_high_queryset()
    filter_class = ReportTeacherHighFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return ReportTeacherHighListSerializer
        elif self.action == "retrieve":
            return ReportTeacherHighRetrieveSerializer
        return ReportTeacherHighUpdateSerializer