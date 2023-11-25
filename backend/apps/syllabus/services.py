from apps.syllabus.models import (
    Syllabus,
    CourseTopic
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