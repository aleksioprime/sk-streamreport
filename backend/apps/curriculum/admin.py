from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin

from apps.curriculum.filters import SubjectAdminFilter
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter

from apps.curriculum.models import (
    Subject,
    FgosSubjectGroup,
    IbSubjectGroup,
    IbDiscipline,
    Curriculum,
    CurriculumLoad,
    TeachingLoad
)

@register(Subject)
class SubjectModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "level",
        "name",
        "group_fgos",
        "group_ib",
        "discipline_ib",
    )
    list_display_links = (
        "name",
    )
    search_fields = (
        "name",
    )
    autocomplete_fields = (
        'group_fgos',
        'discipline_ib'
    )


@register(FgosSubjectGroup)
class SubjectGroupFgosModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "level"
    )
    list_display_links = (
        "name",
    )
    search_fields = (
        "name",
    )

@register(IbSubjectGroup)
class SubjectGroupIbModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "program",
    )
    list_display_links = (
        "name",
    )

@register(IbDiscipline)
class SubjectGroupIbModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "group",
    )
    list_display_links = (
        "name",
    )
    search_fields = (
        "name",
    )

@register(Curriculum)
class CurriculumModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name_short",
        "level",
        "year",
        "ib",
    )
    readonly_fields = (
        "display_loads",
    )
    list_display_links = (
        "name_short",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('year').prefetch_related('curriculum_loads', 'curriculum_loads__years')
    
    def display_loads(self, obj):
        cl_dict = {}
        for cl in obj.curriculum_loads.all().select_related('subject').prefetch_related('years'):
            years = ', '.join(str(obj.number) for obj in cl.years.all()) 
            cl_dict[cl.subject.name] = cl_dict.get(cl.subject.name, []) + [ f"{years} кл: {cl.hours} ч." ]
        return '\n'.join(f"{key.upper()}: {' | '.join([v for v in sorted(value)])}" for key, value in cl_dict.items())
    
    display_loads.short_description = "Нагрузка учебного плана"

@register(CurriculumLoad)
class CurriculumLoadModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "curriculum",
        "subject",
        "type",
        "display_years",
        "hours",
    )
    readonly_fields = (
        "display_years",
    )
    list_display_links = (
        "curriculum",
    )
    filter_horizontal = (
        'years',
    )
    search_fields = (
        "subject",
    )
    list_filter = (
        SubjectAdminFilter,
        "curriculum__year",
        "curriculum",
        "years",
        "type",
    )
    autocomplete_fields = (
        'subject',
    )

    def display_years(self, obj):
        years = ", ".join([f"{cl.number}" for cl in obj.years.all()])
        return f"{years} классы"
    
    display_years.short_description = "Учебные классы"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('curriculum__year','curriculum', 'subject').prefetch_related('years')

@register(TeachingLoad)
class TeachingLoadModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "year",
        "teacher",
        "subject",
        "hours",
    )
    list_display_links = (
        "year",
    )
    filter_horizontal = (
        'groups',
    )
    autocomplete_fields = (
        'subject',
        'teacher',
    )