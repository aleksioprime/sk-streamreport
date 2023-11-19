from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin

from apps.syllabus.models import (
    Course,
    CourseSection,
    CourseTopic,
)

@register(Course)
class CourseModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "subject",
    )
    list_display_links = (
        "subject",
    )

@register(CourseSection)
class CourseSectionModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "course",
        "year",
    )
    list_display_links = (
        "course",
    )

@register(CourseTopic)
class CourseTopicModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "section",
        "number",
        "name",
        "hours",
    )
    list_display_links = (
        "name",
    )