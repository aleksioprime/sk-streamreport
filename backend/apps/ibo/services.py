from apps.ibo.models import (
    LearnerProfile,
    IbProfileDevelop,
    UnitReflectionPost
)

def get_learner_profile_queryset():
    return LearnerProfile.objects.all()

def get_ib_profile_develop_queryset():
    return IbProfileDevelop.objects.all().select_related(
        'profile'
    )

def get_unit_reflection_post_queryset():
    return UnitReflectionPost.objects.all().select_related(
        'author'
    )