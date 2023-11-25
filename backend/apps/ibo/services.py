from apps.ibo.models import (
    LearnerProfile,
)

def get_learner_profile_queryset():
    return LearnerProfile.objects.all()