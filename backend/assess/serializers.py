from rest_framework import serializers
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkGroupDate, WorkAssessment, WorkCriteriaMark
from curriculum.serializers import SubjectSerializer, ClassYearSerializer, UnitMYPSerializerListCreate, CriterionSerializer
from member.serializers import ClassGroupSerializer, UserSerializer
from member.models import ProfileTeacher, User, ProfileStudent
from django.db.models import Q
        
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
    group = ClassGroupSerializer(required=False)
    user = UserSerializer(required=False)
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

class StudyPeriodSerializer(serializers.ModelSerializer):
    study_year = StudyYearSerializer()
    class_year = ClassYearSerializer(many=True)
    class Meta:
        model = StudyPeriod
        fields = '__all__'

class WorkCriteriaMarkSerializer(serializers.ModelSerializer):
    criterion = CriterionSerializer(read_only=True)
    class Meta:
        model = WorkCriteriaMark
        fields = ['id', 'criterion', 'mark', 'criterion_id']
        extra_kwargs = {
            'criterion_id': {'source': 'criterion', 'write_only': True},
            'id': {'read_only': False, 'required': False},
        }

class WorkGroupDateListSerializer(serializers.ModelSerializer):
    group = ClassGroupSerializer(read_only=True)
    class Meta:
        model = WorkGroupDate
        fields = ['id', 'work', 'group', 'group_id', 'date', 'lesson']
        extra_kwargs = {
            'group_id': {'source': 'group', 'write_only': True},
            'id': {'read_only': False, 'required': False},
        }
        
class WorkAssessmentSerializer(serializers.ModelSerializer):
    student = ProfileStudentSerializer(required=False)
    criteria_marks = WorkCriteriaMarkSerializer(many=True, source='work_criteria_mark', required=False)
    class Meta:
        model = WorkAssessment
        fields = ['id', 'work_date', 'student', 'criteria_marks', 'grade', 'student_id']
        extra_kwargs = {
            'student_id': {'source': 'student', 'write_only': True},
        }
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        criteria_mark = validated_data.pop('work_criteria_mark', None)
        instance_criteria_mark = WorkCriteriaMark.objects.filter(work_assess=instance)
        if criteria_mark:
            assess = criteria_mark[0]
            if not assess.get('id'):
                WorkCriteriaMark.objects.create(work_assess=instance, criterion=assess.get('criterion'), mark=assess.get('mark'))
            else: 
                instance_criteria_mark.filter(id=assess.get('id')).update(mark=assess.get('mark'))
        return super().update(instance, validated_data)
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        return super().create(validated_data)

class SummativeWorkSerializer(serializers.ModelSerializer):
    teacher = ProfileTeacherSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    unit = UnitMYPSerializerListCreate(read_only=True)
    criteria = CriterionSerializer(many=True, read_only=True)
    groups = WorkGroupDateListSerializer(many=True, source='workgroup', required=False)
    class Meta:
        model = SummativeWork
        fields = ['id', 'title', 'teacher', 'teacher_id', 'subject', 'subject_id', 
                  'unit', 'unit_id', 'criteria', 'criteria_ids', 'groups', 'period', 'period_id']
        extra_kwargs = {
            'teacher_id': {'source': 'teacher', 'write_only': True},
            'subject_id': {'source': 'subject', 'write_only': True},
            'unit_id': {'source': 'unit', 'write_only': True},
            'period_id': {'source': 'period', 'write_only': True},
            'criteria_ids': {'source': 'criteria', 'write_only': True},
            'title': {'required': False},
        }
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        workgroup = validated_data.pop('workgroup', None)
        if workgroup:
            instance_workgroup = WorkGroupDate.objects.filter(work=instance)
            print('Исходные данные: ', instance_workgroup)
            workgroup_ids = [item.get('id') for item in workgroup]
            instance_workgroup.filter(~Q(id__in=workgroup_ids)).delete()
            new_workgroup = []
            for item in workgroup:
                if item.get('id'):
                    instance_workgroup.filter(id=item.get('id')).update(**item)
                else:
                    new_workgroup.append(WorkGroupDate(work=instance, **item))
            WorkGroupDate.objects.bulk_create(new_workgroup)
        return super().update(instance, validated_data)
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        if 'workgroup' in validated_data.keys():
            workgroup = validated_data.pop('workgroup', None)
        if 'criteria' in validated_data.keys():
            criteria = validated_data.pop('criteria', None)
        instance = SummativeWork.objects.create(**validated_data)
        instance.criteria.set(criteria)
        workgroups = [WorkGroupDate(work=instance, 
                                    group=data.get('group'), 
                                    date=data.get('date'),
                                    lesson=data.get('lesson')) for data in workgroup]
        workgroups_list = WorkGroupDate.objects.bulk_create(workgroups)
        return instance

class WorkGroupDateItemSerializer(serializers.ModelSerializer):
    work = SummativeWorkSerializer(read_only=True)
    group = ClassGroupSerializer(read_only=True)
    students = WorkAssessmentSerializer(many=True, source='workassess', required=False)
    class Meta:
        model = WorkGroupDate
        fields = ['id', 'work', 'group', 'group_id', 'date', 'lesson', 'students']
        extra_kwargs = {
            'group_id': {'source': 'group', 'write_only': True},
            'date': {'required': False},
        }
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        workassess = validated_data.pop('workassess', None)
        if workassess:
            instance_students = [ item.student for item in WorkAssessment.objects.filter(work_date=instance)]
            WorkAssessment.objects.filter(~Q(student__in=[item.get('student') for item in workassess])).delete()
            new_workassess = []
            for data in workassess:
                if data.get('student') not in instance_students:
                    new_workassess.append(WorkAssessment(work_date=instance, **data))
            WorkAssessment.objects.bulk_create(new_workassess)
        return super().update(instance, validated_data)