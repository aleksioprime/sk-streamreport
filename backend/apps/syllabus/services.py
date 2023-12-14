from apps.syllabus.models import (
    Syllabus,
    CourseChapter,
    CourseTopic,
    Course
)

def get_syllabus_list_queryset():
    return Syllabus.objects.all().select_related(
        'subject',
        ).prefetch_related(
            'years',
            'authors'
        )

def get_course_topic_queryset():
    return CourseTopic.objects.all()

def get_course_chapter_queryset():
    return CourseChapter.objects.all().select_related(
        'unit'
    )

def get_course_queryset():
    return Course.objects.all().select_related(
        'year',
        'syllabus'
    ).prefetch_related(
            'chapters',
            'chapters__topics'
        )