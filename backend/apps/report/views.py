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
    get_report_extra_queryset
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
    ReportExtraFilter
)

# Отчётные периоды для репортов: список
@extend_schema_view(
    list=extend_schema(summary='Список отчётных периодов для репортов', tags=['Репорты: Периоды']),
    )
class ReportPeriodViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_period_queryset()
    serializer_class = ReportPeriodListSerializer
    filter_class = ReportPeriodFilter

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
    filter_class = ReportCriterionFilter
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
    filter_class = ReportCriterionLevelFilter
    serializer_class = ReportCriterionLevelSerializer

# Достижения по критериям в репорте: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка достижений по критериям в репорте', tags=['Репорты учителя: Достижения по своим критериям']),
    create=extend_schema(summary='Создание достижения по критериям в репорте', tags=['Репорты учителя: Достижения по своим критериям']),
    update=extend_schema(summary='Обновление достижения по критериям в репорте', tags=['Репорты учителя: Достижения по своим критериям']),
    destroy=extend_schema(summary='Удаление достижения по критериям в репорте', tags=['Репорты учителя: Достижения по своим критериям']),
    )
class ReportCriterionAchievementViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_criterion_achievement_queryset()
    filter_class = ReportCriterionAchievementFilter
    def get_serializer_class(self):
        if self.action == "list":
            return ReportCriterionAchievementListSerializer
        return ReportCriterionAchievementUpdateSerializer
    
# Репорты учителя в начальной школе: список, просмотр, создание, редактирование и удаление
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
    list=extend_schema(summary='Вывод списка достижений по темам в репорте НШ', tags=['Репорты учителя НШ: Достижения по темам']),
    create=extend_schema(summary='Создание достижения по темам в репорте НШ', tags=['Репорты учителя НШ: Достижения по темам']),
    update=extend_schema(summary='Обновление достижения по темам в репорте НШ', tags=['Репорты учителя НШ: Достижения по темам']),
    destroy=extend_schema(summary='Удаление достижения по темам в репорте НШ', tags=['Репорты учителя НШ: Достижения по темам']),
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
    list=extend_schema(summary='Вывод списка баллов по критериям в репорте СрШ', tags=['Репорты учителя СрШ: Баллы по критериям']),
    create=extend_schema(summary='Создание балла по критериям в репорте СрШ', tags=['Репорты учителя СрШ: Баллы по критериям']),
    update=extend_schema(summary='Обновление балла по критериям в репорте СрШ', tags=['Репорты учителя СрШ: Баллы по критериям']),
    destroy=extend_schema(summary='Удаление балла по критериям в репорте СрШ', tags=['Репорты учителя СрШ: Баллы по критериям']),
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
    list=extend_schema(summary='Вывод списка предметных достижений в репорте СрШ', tags=['Репорты учителя СрШ: Предметные достижения']),
    create=extend_schema(summary='Создание предметного достижения в репорте СрШ', tags=['Репорты учителя СрШ: Предметные достижения']),
    update=extend_schema(summary='Обновление предметного достижения в репорте СрШ', tags=['Репорты учителя СрШ: Предметные достижения']),
    destroy=extend_schema(summary='Удаление предметного достижения в репорте СрШ', tags=['Репорты учителя СрШ: Предметные достижения']),
    )
class ReportSecondaryLevelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_secondary_level_queryset()
    filter_class = ReportSecondaryLevelFilter
    def get_serializer_class(self):
        if self.action == "list":
            return ReportSecondaryLevelListSerializer
        return ReportSecondaryLevelUpdateSerializer
    
# Репорты учителя в средней школе: список, просмотр, создание, редактирование и удаление
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
    

# Репорты учителя в старшей школе: список, просмотр, создание, редактирование и удаление
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
    
# Оценки профиля студента в репорте классного руководителя: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка оценок профилей студента в репортах классного руководителя', tags=['Репорты классного руководителя: Развитие профиля студента']),
    create=extend_schema(summary='Создание оценки профиля студента в репортах классного руководителя', tags=['Репорты классного руководителя: Развитие профиля студента']),
    update=extend_schema(summary='Обновление оценки профиля студента в репортах классного руководителя', tags=['Репорты классного руководителя: Развитие профиля студента']),
    destroy=extend_schema(summary='Удаление оценки профиля студента в репортах классного руководителя', tags=['Репорты классного руководителя: Развитие профиля студента']),
    )
class ReportIbProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_ibprofile_queryset()
    filter_class = ReportIbProfileFilter
    def get_serializer_class(self):
        if self.action == "list":
            return ReportIbProfileListSerializer
        return ReportIbProfileUpdateSerializer
    
# Репорты классного руководителя: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов классного руководителя', tags=['Репорты классного руководителя']),
    create=extend_schema(summary='Создание репорта классного руководителя', tags=['Репорты классного руководителя']),
    retrieve=extend_schema(summary='Просмотр репорта классного руководителя', tags=['Репорты классного руководителя']),
    update=extend_schema(summary='Обновление репорта классного руководителя', tags=['Репорты классного руководителя']),
    partial_update=extend_schema(summary='Частичное обновление репорта классного руководителя', tags=['Репорты классного руководителя']),
    destroy=extend_schema(summary='Удаление репорта классного руководителя', tags=['Репорты классного руководителя']),
    )
class ReportMentorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_mentor_queryset()
    filter_class = ReportMentorFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return ReportMentorListSerializer
        elif self.action == "retrieve":
            return ReportMentorRetrieveSerializer
        return ReportMentorUpdateSerializer
    

# Результаты юнита в репорте классного руководителя НШ: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка результатов юнита в репорте классного руководителя НШ', tags=['Репорты классного руководителя НШ: Результаты юнита']),
    create=extend_schema(summary='Создание результата юнита в репорте классного руководителя НШ', tags=['Репорты классного руководителя НШ: Результаты юнита']),
    update=extend_schema(summary='Обновление результата юнита в репорте классного руководителя НШ', tags=['Репорты классного руководителя НШ: Результаты юнита']),
    destroy=extend_schema(summary='Удаление результата юнита в репорте классного руководителя НШ', tags=['Репорты классного руководителя НШ: Результаты юнита']),
    )
class ReportPrimaryUnitViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_primary_unit_queryset()
    filter_class = ReportPrimaryUnitFilter
    def get_serializer_class(self):
        if self.action == "list":
            return ReportPrimaryUnitListSerializer
        return ReportPrimaryUnitUpdateSerializer
    
# Репорты классного руководителя начальной школы: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов классного руководителя НШ', tags=['Репорты классного руководителя НШ']),
    create=extend_schema(summary='Создание репорта классного руководителя НШ', tags=['Репорты классного руководителя НШ']),
    retrieve=extend_schema(summary='Просмотр репорта классного руководителя НШ', tags=['Репорты классного руководителя НШ']),
    update=extend_schema(summary='Обновление репорта классного руководителя НШ', tags=['Репорты классного руководителя НШ']),
    partial_update=extend_schema(summary='Частичное обновление репорта классного руководителя НШ', tags=['Репорты классного руководителя НШ']),
    destroy=extend_schema(summary='Удаление репорта классного руководителя НШ', tags=['Репорты классного руководителя НШ']),
    )
class ReportMentorPrimaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_mentor_primary_queryset()
    filter_class = ReportMentorPrimaryFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return ReportMentorPrimaryListSerializer
        elif self.action == "retrieve":
            return ReportMentorPrimaryRetrieveSerializer
        return ReportMentorPrimaryUpdateSerializer
    
# Репорты дополнительных сотрудников класса: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка репортов классного сотрудника класса', tags=['Репорты сотрудников класса']),
    create=extend_schema(summary='Создание репорта классного сотрудника класса', tags=['Репорты сотрудников класса']),
    retrieve=extend_schema(summary='Просмотр репорта классного сотрудника класса', tags=['Репорты сотрудников класса']),
    update=extend_schema(summary='Обновление репорта классного сотрудника класса', tags=['Репорты сотрудников класса']),
    partial_update=extend_schema(summary='Частичное обновление репорта сотрудника класса', tags=['Репорты сотрудников класса']),
    destroy=extend_schema(summary='Удаление репорта классного сотрудника класса', tags=['Репорты сотрудников класса']),
    )
class ReportExtraViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_report_extra_queryset()
    filter_class = ReportExtraFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return ReportExtraListSerializer
        elif self.action == "retrieve":
            return ReportExtraRetrieveSerializer
        return ReportExtraUpdateSerializer