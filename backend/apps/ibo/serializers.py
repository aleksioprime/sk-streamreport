from rest_framework import serializers

from apps.ibo.models import (
    LearnerProfile,
)

# Список качеств профиля студента IB
class LearnerProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerProfile
        fields = (
            "id", 
            "name", 
            "name_rus",
            "description",
            "description_rus",
            )