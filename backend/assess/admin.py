from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkAssessment, WorkCriteriaMark

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
    list_display = ("title", "unit", "period", "date", "lesson", "subject")

@admin.register(WorkAssessment)
class WorkAssessmentAdmin(ImportExportModelAdmin):
    list_display = ("work", "student")

@admin.register(WorkCriteriaMark)
class WorkCriteriaMarkAdmin(ImportExportModelAdmin):
    list_display = ("work_assessment", "criterion", "mark")