from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkAssessment, WorkCriteriaMark, PeriodAssessment, WorkGroupDate

# Register your models here.
@admin.register(StudyYear)
class StudyYearAdmin(ImportExportModelAdmin):
    list_display = ("name", "date_start", "date_end")
    
@admin.register(ClassGroup)
class ClassGroupAdmin(ImportExportModelAdmin):
    list_display = ("class_year", "letter", "id_dnevnik", "study_year")
    
@admin.register(StudyPeriod)
class StudyPeriodAdmin(ImportExportModelAdmin):
    list_display = ("study_year", "number", "type", "date_start", "date_end")

@admin.register(SummativeWork)
class SummativeWorkAdmin(ImportExportModelAdmin):
    list_display = ("title", "unit", "period", "subject")

@admin.register(WorkGroupDate)
class WorkGroupDateAdmin(ImportExportModelAdmin):
    list_display = ("work", "group", "date", "lesson")

@admin.register(WorkAssessment)
class WorkAssessmentAdmin(ImportExportModelAdmin):
    list_display = ("work_date", "student", "grade")

@admin.register(WorkCriteriaMark)
class WorkCriteriaMarkAdmin(ImportExportModelAdmin):
    list_display = ("work_assess", "criterion", "mark")

@admin.register(PeriodAssessment)
class PeriodAssessmentAdmin(ImportExportModelAdmin):
    list_display = ("period", "student", "criterion_a", "criterion_b", "criterion_c", "criterion_d", "final_grade")
