from django.contrib.admin import register, ModelAdmin, TabularInline, StackedInline
from import_export.admin import ImportExportModelAdmin

from apps.syllabus.models import (
    Syllabus,
    Course,
    CourseChapter,
    CourseTopic,
)

from apps.syllabus.filters import (
    SubjectAdminFilter,
)

class CourseInline(StackedInline):  # StackedInline, TabularInline
    model = Course
    extra = 1

@register(Syllabus)
class SyllabusModelAdmin(ImportExportModelAdmin):
    inlines = [CourseInline]
    list_display = (
        "id",
        "subject",
    )
    list_display_links = (
        "subject",
    )
    filter_horizontal = (
        'authors',
        'years'
    )
    list_filter = (
        SubjectAdminFilter,
    )
    search_fields = (
        "subject",
    )
    # autocomplete_fields = (
    #     'subject',
    # )

class CourseChapterInline(TabularInline):  # StackedInline, TabularInline
    model = CourseChapter
    extra = 1
    fields = (
        "number",
        "name",
        "hours",
    )


@register(Course)
class CourseModelAdmin(ImportExportModelAdmin):
    inlines = [CourseChapterInline]
    list_display = (
        "id",
        "syllabus",
        "year"
    )
    list_display_links = (
        "syllabus",
    )
    search_fields = (
        "syllabus",
        "year"
    )
    # autocomplete_fields = (
    #     'syllabus',
    # )

class CourseTopicInline(TabularInline):  # StackedInline, TabularInline
    model = CourseTopic
    extra = 1
    fields = (
        "number",
        "name",
        "hours",
    )

@register(CourseChapter)
class CourseChapterModelAdmin(ImportExportModelAdmin):
    inlines = [CourseTopicInline]
    list_display = (
        "id",
        "course",
        "number",
        "name",
        "unit"
    )
    search_fields = (
        "course",
        "name"
    )
    list_display_links = (
        "name",
    )
    # autocomplete_fields = (
    #     "course",
    # )

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
    # autocomplete_fields = (
    #     'chapter',
    # )
