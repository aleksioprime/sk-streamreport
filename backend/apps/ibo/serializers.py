from rest_framework import serializers

from general.models import (
    User
)

from apps.ibo.models import (
    LearnerProfile,
    IbProfileDevelop,
    UnitReflectionPost,
    AtlCategory
)

# Список пользователей
class UserIboSerializer(serializers.ModelSerializer):
    short_name = serializers.CharField(source='get_short_name', read_only=True)
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "short_name",
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

# 
class AtlCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlCategory
        fields = (
            "id", 
            "name", 
            "name_rus",
            )

# Список развития качеств портрета студента IB в юните
class IbProfileDevelopListSerializer(serializers.ModelSerializer):
    profile = LearnerProfileListSerializer()
    class Meta:
        model = IbProfileDevelop
        fields = (
            "id",
            "profile",
            "description",
            "unit",
            )
        
class IbProfileDevelopUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IbProfileDevelop
        fields = '__all__'

# 
class UnitReflectionPostListSerializer(serializers.ModelSerializer):
    author = UserIboSerializer()
    class Meta:
        model = UnitReflectionPost
        fields = (
            "id",
            "post",
            "type",
            "author",
            "unit",
            )
        
class UnitReflectionPostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitReflectionPost
        fields = '__all__'