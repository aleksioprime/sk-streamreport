from rest_framework import serializers
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkGroupDate, WorkAssessment, WorkCriteriaMark
from curriculum.serializers import SubjectSerializer, ClassYearSerializer, UnitMYPSerializerListCreate, CriterionSerializer
from member.serializers import ClassGroupSerializer, UserSerializer
from member.models import ProfileTeacher, User, ProfileStudent
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'gender']

class ProfileTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ProfileTeacher
        fields = '__all__'

class ProfileStudentSerializer(serializers.ModelSerializer):
    group = ClassGroupSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = ProfileStudent
        fields = '__all__'

class StudyYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = '__all__'
        
class ClassGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassGroup
        fields = '__all__'

class WorkGroupDateSerializer(serializers.ModelSerializer):
    group = ClassGroupSerializer()
    class Meta:
        model = WorkGroupDate
        fields = '__all__'

class StudyPeriodSerializer(serializers.ModelSerializer):
    study_year = StudyYearSerializer()
    class_year = ClassYearSerializer(many=True)
    class Meta:
        model = StudyPeriod
        fields = '__all__'

class SummativeWorkSerializer(serializers.ModelSerializer):
    teacher = ProfileTeacherSerializer()
    subject = SubjectSerializer()
    unit = UnitMYPSerializerListCreate()
    criteria = CriterionSerializer(many=True)
    groups = WorkGroupDateSerializer(many=True, source='workgroup', required=False)
    class Meta:
        model = SummativeWork
        fields = '__all__'

class WorkCriteriaMarkSerializer(serializers.ModelSerializer):
    criterion = CriterionSerializer()
    class Meta:
        model = WorkCriteriaMark
        fields = '__all__'

class WorkAssessmentSerializer(serializers.ModelSerializer):
    work = SummativeWorkSerializer(required=False)
    student = ProfileStudentSerializer(required=False)
    criteria_marks = WorkCriteriaMarkSerializer(many=True, source='work_criteria_mark', required=False)
    class Meta:
        model = WorkAssessment
        fields = '__all__'
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        if 'work_criteria_mark' in validated_data.keys():
            instance_criterion = WorkCriteriaMark.objects.filter(work_assess=instance)
            list_criterion = [x.get('criterion') for x in validated_data['work_criteria_mark']]
            print(list_criterion)
            print(instance_criterion)
            validated_data.pop('work_criteria_mark', None)
        return super().update(instance, validated_data)

class WorkCriteriaMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCriteriaMark
        fields = '__all__'