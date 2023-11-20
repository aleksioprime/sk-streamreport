from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated


from apps.report.serializers import (
    ReportTeacherPrimaryCreateUpdateSerializer, 
    ReportTeacherPrimaryRetrieveSerializer,
    ReportTeacherPrimaryListSerializer,
)

from apps.report.models import (
    ReportTeacherPrimary
)

from apps.report.services import (
    get_peport_teacher_primary_queryset
)

from apps.report.filters import (
    ReportTeacherPrimaryFilter
)

@extend_schema_view(
    list=extend_schema(summary='Список репортов учителя в начальной школе', tags=['Репорты учителя НШ']),
    create=extend_schema(summary='Создание репорта учителя в начальной школе', tags=['Репорты учителя НШ']),
    retrieve=extend_schema(summary='Просмотр репорта учителя в начальной школе', tags=['Репорты учителя НШ']),
    update=extend_schema(summary='Обновление репорта учителя в начальной школе', tags=['Репорты учителя НШ']),
    destroy=extend_schema(summary='Удаление репорта учителя в начальной школе', tags=['Репорты учителя НШ']),
    )
class ReportTeacherPrimaryViewSet(ModelViewSet):
    queryset = get_peport_teacher_primary_queryset()
    filter_class = ReportTeacherPrimaryFilter
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == "list":
            return ReportTeacherPrimaryListSerializer
        elif self.action == "retrieve":
            return ReportTeacherPrimaryRetrieveSerializer
        return ReportTeacherPrimaryCreateUpdateSerializer
