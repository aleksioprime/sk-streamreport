from general.models import (
    User,
    ClassGroup,
)

def get_user_queryset():
    return User.objects.all().prefetch_related(
            "myp_unitplans",
        ).order_by("-id")

def get_group_queryset():
    return ClassGroup.objects.all().select_related(
            "year_academic",
            "year_study",
        )