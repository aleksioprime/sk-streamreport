from rest_framework import serializers
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkGroupDate, WorkAssessment, WorkCriteriaMark, \
    PeriodAssessment, ReportPeriod, ReportTeacher, EventParticipation, EventType, ReportMentor
from curriculum.serializers import SubjectSerializer, ClassYearSerializer, UnitMYPSerializerListCreate, CriterionSerializer
from member.serializers import ClassGroupSerializer, UserSerializer
from member.models import ProfileTeacher, User, ProfileStudent
from django.db.models import Q
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'photo']

class ProfileTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ProfileTeacher
        fields = '__all__'

class ProfileStudentSerializer(serializers.ModelSerializer):
    groups = ClassGroupSerializer(many=True, required=False)
    user = UserSerializer(required=False)
    class Meta:
        model = ProfileStudent
        fields = '__all__'

class StudyYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = '__all__'

class ClassGroupSerializer(serializers.ModelSerializer):
    mentor = ProfileTeacherSerializer(read_only=True)
    psychologist = ProfileTeacherSerializer(read_only=True)
    class Meta:
        model = ClassGroup
        fields = ['id', 'class_year', 'letter', 'id_dnevnik', 'count', 'study_year', 
                  'mentor', 'psychologist']
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        return super().update(instance, validated_data)
    
class ClassGroupExtraSerializer(serializers.ModelSerializer):
    students = ProfileStudentSerializer(many=True, read_only=True)
    mentor = ProfileTeacherSerializer(read_only=True)
    psychologist = ProfileTeacherSerializer(read_only=True)
    class Meta:
        model = ClassGroup
        fields = ['id', 'class_year', 'letter', 'id_dnevnik', 'students', 'students_ids', 
                  'support', 'support_id', 'mentor', 'mentor_id', 'psychologist', 'psychologist_id']
        extra_kwargs = {
            'students_ids': {'source': 'students', 'write_only': True},
            'mentor_id': {'source': 'mentor', 'write_only': True},
            'psychologist_id': {'source': 'psychologist', 'write_only': True},
            'support_id': {'source': 'support', 'write_only': True},
        }
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        return super().update(instance, validated_data)

class StudyPeriodSerializer(serializers.ModelSerializer):
    study_year = StudyYearSerializer()
    class_year = ClassYearSerializer(many=True)
    type = serializers.SerializerMethodField(source="get_type")
    class Meta:
        model = StudyPeriod
        fields = '__all__'
    def get_type(self, obj):
        return obj.get_type_display()

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
    period = StudyPeriodSerializer(read_only=True)
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
    # students = WorkAssessmentSerializer(many=True, read_only=True)
    class Meta:
        model = WorkGroupDate
        fields = ['id', 'work', 'group', 'group_id', 'date', 'lesson', 'students']
        extra_kwargs = {
            'group_id': {'source': 'group', 'write_only': True},
            # 'students_ids': {'source': 'group', 'write_only': True},
            'date': {'required': False},
        }
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        workassess = validated_data.pop('workassess', None)
        if workassess is not None:
            print(workassess)
            instance_students = [ item.student for item in WorkAssessment.objects.filter(work_date=instance)]
            WorkAssessment.objects.filter(Q(work_date=instance) & ~Q(student__in=[item.get('student') for item in workassess])).delete()
            new_workassess = []
            for data in workassess:
                if data.get('student') not in instance_students:
                    new_workassess.append(WorkAssessment(work_date=instance, **data))
            WorkAssessment.objects.bulk_create(new_workassess)
        return super().update(instance, validated_data)
    
class PeriodAssessmentSerializer(serializers.ModelSerializer):
    student = ProfileStudentSerializer(read_only=True)
    period = StudyPeriodSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    year = ClassYearSerializer(read_only=True)
    class Meta:
        model = PeriodAssessment
        fields = ['id', 'student', 'student_id', 'period', 'period_id', 'subject', 'subject_id',
                  'year', 'year_id', 'criterion_a', 'criterion_b', 'criterion_c', 'criterion_d', 
                  'summ_grade', 'summ_criterion', 'count_criterion', 'form_grade', 'final_grade',
                  'prediction_criterion']
        extra_kwargs = {
            'student_id': {'source': 'student', 'write_only': True},
            'period_id': {'source': 'period', 'write_only': True},
            'subject_id': {'source': 'subject', 'write_only': True},
            'year_id': {'source': 'year', 'write_only': True},
        }

class WorkGroupDateStudentListSerializer(serializers.ModelSerializer):
    work = SummativeWorkSerializer(read_only=True)
    class Meta:
        model = WorkGroupDate
        fields = ['id', 'work', 'date', 'lesson']

class WorkAssessmentStudentSerializer(serializers.ModelSerializer):
    work_date = WorkGroupDateStudentListSerializer(read_only=True)
    criteria_marks = WorkCriteriaMarkSerializer(many=True, source='work_criteria_mark', read_only=True)
    class Meta:
        model = WorkAssessment
        fields = ['id', 'work_date', 'criteria_marks', 'grade']

class StudentWorkSerializer(serializers.ModelSerializer):
    groups = ClassGroupSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    # workgroups = WorkAssessmentStudentSerializer(many=True, source='workassess', read_only=True)
    workgroups = serializers.SerializerMethodField('get_workgroups')
    periodassess = serializers.SerializerMethodField('get_assessment')
    class Meta:
        model = ProfileStudent
        fields = '__all__'
    def get_workgroups(self, instance):
        workassess_queryset = WorkAssessment.objects.filter(student=instance)
        period = self.context.get("period", None)
        subject = self.context.get("subject", None)
        group = self.context.get("group", None)
        if period:
            workassess_queryset = workassess_queryset.filter(work_date__work__period=period)
        if subject:
            workassess_queryset = workassess_queryset.filter(work_date__work__subject=subject)
        if group:
            workassess_queryset = workassess_queryset.filter(work_date__work__groups__in=[group]).distinct()
        serializer = WorkAssessmentStudentSerializer(instance=workassess_queryset, many=True, context=self.context)
        return serializer.data
    def get_assessment(self, instance):
        period_assessment_queryset = PeriodAssessment.objects.filter(student=instance)
        subject = self.context.get("subject", None)
        class_year = self.context.get("class_year", None)
        period = self.context.get("period", None)
        if subject:
            period_assessment_queryset = period_assessment_queryset.filter(subject=subject)
        if class_year:
            period_assessment_queryset = period_assessment_queryset.filter(year=class_year)
        if period:
            period_assessment_queryset = period_assessment_queryset.filter(period=period)
        serializer = PeriodAssessmentSerializer(instance=period_assessment_queryset.first(), context=self.context)
        return serializer.data

class ReportPeriodSerializer(serializers.ModelSerializer):
    study_year = StudyYearSerializer()
    assessment_period = StudyPeriodSerializer()
    class Meta:
        model = ReportPeriod
        fields = '__all__'

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'

class EventParticipationSerializer(serializers.ModelSerializer):
    type = EventTypeSerializer(read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    level_name = serializers.CharField(source='get_level_display', read_only=True)
    class Meta:
        model = EventParticipation
        fields = ['id', 'type', 'type_name', 'level', 'level_name', 'type', 'type_id', 
                  'title', 'result']
        extra_kwargs = {
            'type_id': {'source': 'type', 'write_only': True},
        }

class ReportTeacherSerializer(serializers.ModelSerializer):
    student = ProfileStudentSerializer(read_only=True)
    period = ReportPeriodSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    year = ClassYearSerializer(read_only=True)
    events = EventParticipationSerializer(many=True, required=False)
    author = ProfileTeacherSerializer(read_only=True)
    class Meta:
        model = ReportTeacher
        fields = ['id', 'student', 'student_id', 'period', 'period_id', 'subject', 'subject_id',
                  'year', 'year_id', 'text', 'events', 'author', 'author_id']
        extra_kwargs = {
            'student_id': {'source': 'student', 'write_only': True},
            'period_id': {'source': 'period', 'write_only': True},
            'subject_id': {'source': 'subject', 'write_only': True},
            'year_id': {'source': 'year', 'write_only': True},
            'author_id': {'source': 'author', 'write_only': True},
        }
    def create_or_update_events(self, events):
        events_ids = []
        for event in events:
            event_instance, created = EventParticipation.objects.update_or_create(pk=event.get('id'), defaults=event)
            events_ids.append(event_instance.pk)
        return events_ids
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        events = validated_data.pop('events', None)
        if events is not None:
            original = EventParticipation.objects.filter(teacher_reports=instance)
            original.filter(~Q(id__in=[item.get('id') for item in events if 'id' in item])).delete()
            instance.events.set(self.create_or_update_events(events))
            instance.save()
        return super().update(instance, validated_data)

class StudentReportTeacherSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField('get_group')
    user = UserSerializer(read_only=True)
    teacher_report = serializers.SerializerMethodField('get_reports')
    periodassess = serializers.SerializerMethodField('get_assessment')
    class Meta:
        model = ProfileStudent
        fields = '__all__'
    def get_reports(self, instance):
        report_queryset = ReportTeacher.objects.filter(student=instance)
        period = self.context.get("period", None)
        subject = self.context.get("subject", None)
        class_year = self.context.get("class_year", None)
        author = self.context.get("author", None)
        if period:
            report_queryset = report_queryset.filter(period=period)
        if subject:
            report_queryset = report_queryset.filter(subject=subject)
        if author:
            report_queryset = report_queryset.filter(author=author)
        if class_year:
            report_queryset = report_queryset.filter(year=class_year)
        serializer = ReportTeacherSerializer(instance=report_queryset.first(), context=self.context)
        return serializer.data
    def get_group(self, instance):
        group_queryset = ClassGroup.objects.filter(students__in=[instance])
        study_year = self.context.get("study_year", None)
        if study_year:
            group_queryset = group_queryset.filter(study_year=study_year)
        serializer = ClassGroupSerializer(instance=group_queryset.last(), context=self.context)
        return serializer.data
    def get_assessment(self, instance):
        period_assessment_queryset = PeriodAssessment.objects.filter(student=instance)
        subject = self.context.get("subject", None)
        class_year = self.context.get("class_year", None)
        report_period = self.context.get("period", None)
        if subject:
            period_assessment_queryset = period_assessment_queryset.filter(subject=subject)
        if class_year:
            period_assessment_queryset = period_assessment_queryset.filter(year=class_year)
        if report_period:
            period_assessment_queryset = period_assessment_queryset.filter(period__report_period__in=[report_period]).distinct()
        serializer = PeriodAssessmentSerializer(instance=period_assessment_queryset.first(), context=self.context)
        return serializer.data

class ReportMentorSerializer(serializers.ModelSerializer):
    student = ProfileStudentSerializer(read_only=True)
    period = ReportPeriodSerializer(read_only=True)
    year = ClassYearSerializer(read_only=True)
    events = EventParticipationSerializer(many=True, required=False)
    author = ProfileTeacherSerializer(read_only=True)
    class Meta:
        model = ReportMentor
        fields = ['id', 'student', 'student_id', 'period', 'period_id',
                  'year', 'year_id', 'text', 'events', 'author', 'author_id']
        extra_kwargs = {
            'student_id': {'source': 'student', 'write_only': True},
            'period_id': {'source': 'period', 'write_only': True},
            'year_id': {'source': 'year', 'write_only': True},
            'author_id': {'source': 'author', 'write_only': True},
        }
    def create_or_update_events(self, events):
        events_ids = []
        for event in events:
            event_instance, created = EventParticipation.objects.update_or_create(pk=event.get('id'), defaults=event)
            events_ids.append(event_instance.pk)
        return events_ids
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        events = validated_data.pop('events', None)
        if events is not None:
            original = EventParticipation.objects.filter(mentor_reports=instance)
            original.filter(~Q(id__in=[item.get('id') for item in events if 'id' in item])).delete()
            instance.events.set(self.create_or_update_events(events))
            instance.save()
        return super().update(instance, validated_data)

class StudentReportMentorSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField('get_group')
    user = UserSerializer(read_only=True)
    teacher_report = serializers.SerializerMethodField('get_teacher_reports')
    mentor_report = serializers.SerializerMethodField('get_mentor_report')
    periodassess = serializers.SerializerMethodField('get_assessments')
    class Meta:
        model = ProfileStudent
        fields = '__all__'
    def get_teacher_reports(self, instance):
        report_queryset = ReportTeacher.objects.filter(student=instance)
        period = self.context.get("period", None)
        class_year = self.context.get("class_year", None)
        author = self.context.get("author", None)
        if period:
            report_queryset = report_queryset.filter(period=period)
        if author:
            report_queryset = report_queryset.filter(author=author)
        if class_year:
            report_queryset = report_queryset.filter(year=class_year)
        serializer = ReportTeacherSerializer(instance=report_queryset, many=True, context=self.context)
        return serializer.data
    def get_mentor_report(self, instance):
        report_queryset = ReportMentor.objects.filter(student=instance)
        period = self.context.get("period", None)
        class_year = self.context.get("class_year", None)
        author = self.context.get("author", None)
        if period:
            report_queryset = report_queryset.filter(period=period)
        if author:
            report_queryset = report_queryset.filter(author=author)
        if class_year:
            report_queryset = report_queryset.filter(year=class_year)
        serializer = ReportMentorSerializer(instance=report_queryset.first(), context=self.context)
        return serializer.data
    def get_group(self, instance):
        group_queryset = ClassGroup.objects.filter(students__in=[instance])
        study_year = self.context.get("study_year", None)
        if study_year:
            group_queryset = group_queryset.filter(study_year=study_year)
        serializer = ClassGroupSerializer(instance=group_queryset.last(), context=self.context)
        return serializer.data
    def get_assessments(self, instance):
        period_assessment_queryset = PeriodAssessment.objects.filter(student=instance)
        class_year = self.context.get("class_year", None)
        report_period = self.context.get("period", None)
        if class_year:
            period_assessment_queryset = period_assessment_queryset.filter(year=class_year)
        if report_period:
            period_assessment_queryset = period_assessment_queryset.filter(period__report_period__in=[report_period]).distinct()
        serializer = PeriodAssessmentSerializer(instance=period_assessment_queryset, many=True, context=self.context)
        return serializer.data