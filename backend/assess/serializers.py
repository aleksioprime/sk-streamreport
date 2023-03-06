from rest_framework import serializers
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkAssessment, WorkCriteriaMark
from member.models import ProfileTeacher, User
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'gender']

class ProfileTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ProfileTeacher
        fields = '__all__'

class StudyYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = '__all__'
        
class ClassGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassGroup
        fields = '__all__'

class StudyPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPeriod
        fields = '__all__'

class SummativeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummativeWork
        fields = '__all__'

class WorkAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkAssessment
        fields = '__all__'

class WorkCriteriaMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCriteriaMark
        fields = '__all__'