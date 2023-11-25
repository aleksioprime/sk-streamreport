from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin

from apps.syllabus.models import (
    Syllabus,
    Course,
    CourseChapter,
    CourseTopic,
)

@register(Syllabus)
class SyllabusModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "subject",
    )
    list_display_links = (
        "subject",
    )

@register(Course)
class CourseModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "syllabus",
        "year"
    )
    list_display_links = (
        "syllabus",
    )

@register(CourseChapter)
class CourseChapterModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "course",
        "number",
        "name",
        "unit"
    )
    list_display_links = (
        "name",
    )

@register(CourseTopic)
class CourseTopicModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "chapter",
        "number",
        "name",
        "hours",
    )
    list_display_links = (
        "name",
    )