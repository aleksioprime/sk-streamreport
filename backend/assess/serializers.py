from rest_framework import serializers
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkGroupDate, WorkAssessment, WorkCriteriaMark, \
    PeriodAssessment, ReportPeriod, ReportTeacher, EventParticipation, EventType, ReportMentor, GRADES, WorkLoad, ReportAchievements, \
    ReportPsychologist
from curriculum.serializers import SubjectSerializer, ClassYearSerializer, UnitMYPSerializerListCreate, CriterionSerializer
from member.serializers import UserSerializer
from member.models import ProfileTeacher, User, ProfileStudent
from curriculum.models import Subject, ClassYear, Criterion
from django.db.models import Q
import math

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'photo']

class ClassGroupSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassGroup
        fields = '__all__'

class ProfileStudentSerializer(serializers.ModelSerializer):
    groups = ClassGroupSimpleSerializer(many=True, required=False)
    user = UserSerializer(required=False)
    class Meta:
        model = ProfileStudent
        fields = '__all__'

class StudyYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = '__all__'

class ProfileTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ProfileTeacher
        fields = '__all__'

class ClassGroupSerializer(serializers.ModelSerializer):
    class_year = ClassYearSerializer(read_only=True)
    mentor = ProfileTeacherSerializer(read_only=True)
    psychologist = ProfileTeacherSerializer(read_only=True)
    class Meta:
        model = ClassGroup
        fields = ['id', 'class_year', 'letter', 'id_dnevnik', 'count', 'study_year', 
                  'mentor', 'psychologist']
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        return super().update(instance, validated_data)

class ClassGroupStudentsSerializer(serializers.ModelSerializer):
    students = ProfileStudentSerializer(many=True, read_only=True)
    class_year = ClassYearSerializer(read_only=True)
    mentor = ProfileTeacherSerializer(read_only=True)
    psychologist = ProfileTeacherSerializer(read_only=True)
    class Meta:
        model = ClassGroup
        fields = ['id', 'class_year', 'letter', 'id_dnevnik', 'count', 'study_year', 
                  'mentor', 'psychologist', 'students']
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
                  'mentor', 'mentor_id', 'psychologist', 'psychologist_id']
        extra_kwargs = {
            'students_ids': {'source': 'students', 'write_only': True},
            'mentor_id': {'source': 'mentor', 'write_only': True},
            'psychologist_id': {'source': 'psychologist', 'write_only': True},
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
    group = ClassGroupStudentsSerializer(read_only=True)
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
    def to_internal_value(self, data):
        if 'criterion_a' in data and not data['criterion_a'].isdigit():
            data.pop('criterion_a', None)
        if 'criterion_b' in data and not data['criterion_b'].isdigit():
            data.pop('criterion_b', None)
        if 'criterion_c' in data and not data['criterion_c'].isdigit():
            data.pop('criterion_c', None)
        if 'criterion_d' in data and not data['criterion_d'].isdigit():
            data.pop('criterion_d', None)
        return super(PeriodAssessmentSerializer, self).to_internal_value(data)


#####################################################
# Набор сериализаторов для журнала оценок за период #
#####################################################

class WorkAssessmentStudentSerializer(serializers.ModelSerializer):
    lesson = serializers.CharField(source='work_date.lesson', read_only=True)
    date = serializers.CharField(source='work_date.date', read_only=True)
    criteria_marks = WorkCriteriaMarkSerializer(many=True, source='work_criteria_mark', read_only=True)
    class Meta:
        model = WorkAssessment
        fields = ['id', 'criteria_marks', 'grade', 'date', 'lesson']

class PeriodAssessmentStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodAssessment
        fields = ['id', 'criterion_a', 'criterion_b', 'criterion_c', 'criterion_d', 
                  'summ_grade', 'summ_criterion', 'count_criterion', 'form_grade', 'final_grade',
                  'prediction_criterion']

def get_grade_for_criteria(summ, num):
    if summ >= GRADES[num][2]:
        return 5
    elif summ < GRADES[num][2] and summ >= GRADES[num][1]:
        return 4
    elif summ < GRADES[num][1] and summ >= GRADES[num][0]:
        return 3
    elif summ < GRADES[num][0] and summ > 0:
        return 2
    else:
        return '-'

class StudentWorkSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    periodassess = serializers.SerializerMethodField('get_assessment')
    class Meta:
        model = ProfileStudent
        fields = '__all__'
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
        serializer = PeriodAssessmentStudentSerializer(instance=period_assessment_queryset.first(), context=self.context)
        return serializer.data
    def to_representation(self, instance):
        result = super(StudentWorkSerializer, self).to_representation(instance)
        subject = self.context.get("subject", None)
        period = self.context.get("period", None)
        group = self.context.get("group", None)
        work_queryset = instance.workassess.all()
        if subject:
            work_queryset = work_queryset.filter(work_date__work__subject=subject)
        if period:
            work_queryset = work_queryset.filter(work_date__work__period=period)
        if group:
            work_queryset = work_queryset.filter(work_date__work__groups__in=[group]).distinct()
        criterias = {}
        for work in work_queryset:
            for cmark in work.work_criteria_mark.all():
                if cmark.criterion.letter == 'A':
                    criterias['criteria_a'] = criterias.get('criteria_a', []) + [ cmark.mark ]
                if cmark.criterion.letter == 'B':
                    criterias['criteria_b'] = criterias.get('criteria_b', []) + [ cmark.mark ]
                if cmark.criterion.letter == 'C':
                    criterias['criteria_c'] = criterias.get('criteria_c', []) + [ cmark.mark ]
                if cmark.criterion.letter == 'D':
                    criterias['criteria_d'] = criterias.get('criteria_d', []) + [ cmark.mark ]
        criterias_avg = {}
        for crs in criterias:
            criterias_avg[crs] = math.ceil(sum(criterias[crs]) / len(criterias[crs]))
        result['criteria_list'] = criterias
        result['criteria_sum'] = sum(criterias_avg.values())
        result['criteria_num'] = len(criterias_avg.values())
        if result['criteria_num']:
            result['criteria_result'] = get_grade_for_criteria(result['criteria_sum'], result['criteria_num'])
        else:
            result['criteria_result'] = None
        return result

class ReportPeriodSerializer(serializers.ModelSerializer):
    study_year = StudyYearSerializer()
    assessment_periods = StudyPeriodSerializer(many=True, read_only=True)
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

###################
# РЕПОРТЫ УЧИТЕЛЯ #
###################


class ProfileStudentSimpleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = ProfileStudent
        fields = '__all__'

class ReportAchievementsSerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(source='objective.level.id', read_only=True)
    objective_description = serializers.CharField(source='objective.name_eng', read_only=True)
    criterion = serializers.IntegerField(source='objective.strand.criterion.id', read_only=True)
    point = serializers.IntegerField(source='achievement.point', read_only=True)
    achievement_description = serializers.CharField(source='achievement.name_eng', read_only=True)
    class Meta:
        model = ReportAchievements
        fields = ['id', 'objective', 'objective_id', 'achievement', 'achievement_id', 'level', 'criterion', 'point', 
                  'objective_description', 'achievement_description']
        extra_kwargs = {
            'objective_id': {'source': 'objective', 'write_only': True},
            'achievement_id': {'source': 'achievement', 'write_only': True},
        }

class ReportTeacherSerializer(serializers.ModelSerializer):
    student = ProfileStudentSimpleSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    year = ClassYearSerializer(read_only=True)
    events = EventParticipationSerializer(many=True, required=False)
    author = ProfileTeacherSerializer(read_only=True)
    achievements = ReportAchievementsSerializer(many=True, required=False)
    class Meta:
        model = ReportTeacher
        fields = ['id', 'student', 'student_id', 'period', 'period_id', 'subject', 'subject_id',
                  'year', 'year_id', 'text', 'events', 'author', 'author_id', 'achievements', 
                  'criterion_a', 'criterion_b', 'criterion_c', 'criterion_d']
        extra_kwargs = {
            'student_id': {'source': 'student', 'write_only': True},
            'period_id': {'source': 'period', 'write_only': True},
            'subject_id': {'source': 'subject', 'write_only': True},
            'year_id': {'source': 'year', 'write_only': True},
            'author_id': {'source': 'author', 'write_only': True},
            # 'achievements_ids': {'source': 'achievements', 'write_only': True},
        }
    def create_or_update_events(self, events):
        events_ids = []
        for event in events:
            event_instance, created = EventParticipation.objects.update_or_create(pk=event.get('id'), defaults=event)
            events_ids.append(event_instance.pk)
        return events_ids
    def create_or_update_achievements(self, achievements):
        achievements_ids = []
        for achievement in achievements:
            achievement_instance, created = ReportAchievements.objects.update_or_create(pk=achievement.get('id'), defaults=achievement)
            achievements_ids.append(achievement_instance.pk)
        return achievements_ids
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        events = validated_data.pop('events', None)
        if events is not None:
            original = EventParticipation.objects.filter(teacher_reports=instance)
            original.filter(~Q(id__in=[item.get('id') for item in events if 'id' in item])).delete()
            instance.events.set(self.create_or_update_events(events))
            instance.save()
        achievements = validated_data.pop('achievements', None)
        if achievements is not None:
            original = ReportAchievements.objects.filter(teacher_reports=instance)
            original.filter(~Q(id__in=[item.get('id') for item in achievements if 'id' in item])).delete()
            instance.achievements.set(self.create_or_update_achievements(achievements))
            instance.save()
        return super().update(instance, validated_data)
    def to_representation(self, instance):
        result = super(ReportTeacherSerializer, self).to_representation(instance)
        # subject = self.context.get("subject", None)
        # class_year = self.context.get("class_year", None)
        # report_period = self.context.get("period", None)
        if result['subject'] is None and result['year'] is None and result['period'] is None:
            return result
        subject_id = result['subject']['id']
        class_year_id = result['year']['id']
        period_id = result['period']
        assessment = PeriodAssessment.objects.filter(student=instance.student,
                                                            subject=subject_id,
                                                            year=class_year_id,
                                                            period__report_period__in=[period_id]).distinct()
        criteria = {}
        avg_criteria = {}
        for assess in assessment:
            criteria['criteria_a'] = criteria.get('criteria_a', []) + [ { 'mark': assess.criterion_a, 'period': assess.period.number } ]
            if assess.criterion_a:
                avg_criteria['criteria_a_sum'] = avg_criteria.get('criteria_a_sum', 0) + assess.criterion_a
                avg_criteria['criteria_a_num'] = avg_criteria.get('criteria_a_num', 0) + 1
            criteria['criteria_b'] = criteria.get('criteria_b', []) + [ { 'mark': assess.criterion_b, 'period': assess.period.number } ]
            if assess.criterion_b:
                avg_criteria['criteria_b_sum'] = avg_criteria.get('criteria_b_sum', 0) + assess.criterion_b
                avg_criteria['criteria_b_num'] = avg_criteria.get('criteria_b_num', 0) + 1
            criteria['criteria_c'] = criteria.get('criteria_c', []) + [ { 'mark': assess.criterion_c, 'period': assess.period.number } ]
            if assess.criterion_c:
                avg_criteria['criteria_c_sum'] = avg_criteria.get('criteria_c_sum', 0) + assess.criterion_c
                avg_criteria['criteria_c_num'] = avg_criteria.get('criteria_c_num', 0) + 1
            criteria['criteria_d'] = criteria.get('criteria_d', []) + [ { 'mark': assess.criterion_d, 'period': assess.period.number } ]
            if assess.criterion_d:
                avg_criteria['criteria_d_sum'] = avg_criteria.get('criteria_d_sum', 0) + assess.criterion_d
                avg_criteria['criteria_d_num'] = avg_criteria.get('criteria_d_num', 0) + 1
            criteria['summ_grades'] = criteria.get('summ_grades', []) + [ { 'mark': assess.summ_grade, 'period': assess.period.number } ]
            criteria['form_grades'] = criteria.get('form_grades', []) + [ { 'mark': assess.form_grade, 'period': assess.period.number } ]
            criteria['final_grades'] = criteria.get('final_grades', []) + [ { 'mark': assess.final_grade, 'period': assess.period.number } ]
        result['assessment'] = criteria 
        result['avg_assessment'] = {}
        if avg_criteria:
            if 'criteria_a_num' in avg_criteria:
                result['avg_assessment']['criterion_a'] = math.ceil(avg_criteria['criteria_a_sum'] / avg_criteria['criteria_a_num'])
            if 'criteria_b_num' in avg_criteria:
                result['avg_assessment']['criterion_b'] = math.ceil(avg_criteria['criteria_b_sum'] / avg_criteria['criteria_b_num'])
            if 'criteria_c_num' in avg_criteria:
                result['avg_assessment']['criterion_c'] = math.ceil(avg_criteria['criteria_c_sum'] / avg_criteria['criteria_c_num'])
            if 'criteria_d_num' in avg_criteria:
                result['avg_assessment']['criterion_d'] = math.ceil(avg_criteria['criteria_d_sum'] / avg_criteria['criteria_d_num'])
        criteria = Criterion.objects.filter(subject_group__subject__in=[result['subject']['id']]).distinct()
        result['predict'] = {}
        for criterion in criteria:
            result['predict'][criterion.id] = {}
            result['predict'][criterion.id]['all_strands'] = criterion.strand.count()
        for item in result['achievements']:
            result['predict'][item['criterion']]['count_points'] = result['predict'][item['criterion']].get('count_points', 0) + 1
            if 'point' in item:
                result['predict'][item['criterion']]['sum_points'] = result['predict'][item['criterion']].get('sum_points', 0) + item['point']
        return result
    # def to_internal_value(self, data):
    #     if 'criterion_a' in data and not data['criterion_a'].isdigit():
    #         data.pop('criterion_a', None)
    #     if 'criterion_b' in data and not data['criterion_b'].isdigit():
    #         data.pop('criterion_b', None)
    #     if 'criterion_c' in data and not data['criterion_c'].isdigit():
    #         data.pop('criterion_c', None)
    #     if 'criterion_d' in data and not data['criterion_d'].isdigit():
    #         data.pop('criterion_d', None)
    #     return super(ReportTeacherSerializer, self).to_internal_value(data)

class PeriodAssessmentStudentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodAssessment
        fields = ['criterion_a', 'criterion_b', 'criterion_c', 'criterion_d']

class StudyPeriodReportSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(source="get_type")
    class Meta:
        model = StudyPeriod
        fields = ['type', 'number']
    def get_type(self, obj):
        return obj.get_type_display()
    
class StudentReportTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    teacher_report = serializers.SerializerMethodField('get_reports')
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
    def to_representation(self, instance):
        result = super(StudentReportTeacherSerializer, self).to_representation(instance)
        subject = self.context.get("subject", None)
        class_year = self.context.get("class_year", None)
        report_period = self.context.get("period", None)
        assessment = PeriodAssessment.objects.filter(student=instance,
                                                            subject=subject,
                                                            year=class_year,
                                                            period__report_period__in=[report_period]).distinct()
        criteria = {}
        avg_criteria = {}
        for assess in assessment:
            criteria['criteria_a'] = criteria.get('criteria_a', []) + [ { 'mark': assess.criterion_a, 'period': assess.period.number } ]
            if assess.criterion_a:
                avg_criteria['criteria_a_sum'] = avg_criteria.get('criteria_a_sum', 0) + assess.criterion_a
                avg_criteria['criteria_a_num'] = avg_criteria.get('criteria_a_num', 0) + 1
            criteria['criteria_b'] = criteria.get('criteria_b', []) + [ { 'mark': assess.criterion_b, 'period': assess.period.number } ]
            if assess.criterion_b:
                avg_criteria['criteria_b_sum'] = avg_criteria.get('criteria_b_sum', 0) + assess.criterion_b
                avg_criteria['criteria_b_num'] = avg_criteria.get('criteria_b_num', 0) + 1
            criteria['criteria_c'] = criteria.get('criteria_c', []) + [ { 'mark': assess.criterion_c, 'period': assess.period.number } ]
            if assess.criterion_c:
                avg_criteria['criteria_c_sum'] = avg_criteria.get('criteria_c_sum', 0) + assess.criterion_c
                avg_criteria['criteria_c_num'] = avg_criteria.get('criteria_c_num', 0) + 1
            criteria['criteria_d'] = criteria.get('criteria_d', []) + [ { 'mark': assess.criterion_d, 'period': assess.period.number } ]
            if assess.criterion_d:
                avg_criteria['criteria_d_sum'] = avg_criteria.get('criteria_d_sum', 0) + assess.criterion_d
                avg_criteria['criteria_d_num'] = avg_criteria.get('criteria_d_num', 0) + 1
            criteria['summ_grades'] = criteria.get('summ_grades', []) + [ { 'mark': assess.summ_grade, 'period': assess.period.number } ]
            criteria['form_grades'] = criteria.get('form_grades', []) + [ { 'mark': assess.form_grade, 'period': assess.period.number } ]
            criteria['final_grades'] = criteria.get('final_grades', []) + [ { 'mark': assess.final_grade, 'period': assess.period.number } ]
        result['assessment'] = criteria 
        result['avg_assessment'] = {}
        if avg_criteria:
            if 'criteria_a_num' in avg_criteria:
                result['avg_assessment']['criterion_a'] = math.ceil(avg_criteria['criteria_a_sum'] / avg_criteria['criteria_a_num'])
            if 'criteria_b_num' in avg_criteria:
                result['avg_assessment']['criterion_b'] = math.ceil(avg_criteria['criteria_b_sum'] / avg_criteria['criteria_b_num'])
            if 'criteria_c_num' in avg_criteria:
                result['avg_assessment']['criterion_c'] = math.ceil(avg_criteria['criteria_c_sum'] / avg_criteria['criteria_c_num'])
            if 'criteria_d_num' in avg_criteria:
                result['avg_assessment']['criterion_d'] = math.ceil(avg_criteria['criteria_d_sum'] / avg_criteria['criteria_d_num'])
        return result


#####################
# РЕПОРТЫ ПСИХОЛОГА #
#####################

class ReportPsychologistSerializer(serializers.ModelSerializer):
    student = ProfileStudentSerializer(read_only=True)
    period = ReportPeriodSerializer(read_only=True)
    year = ClassYearSerializer(read_only=True)
    events = EventParticipationSerializer(many=True, required=False)
    author = ProfileTeacherSerializer(read_only=True)
    class Meta:
        model = ReportPsychologist
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
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        events = validated_data.pop('events', None)
        if events is not None:
            instance = ReportPsychologist.objects.create(**validated_data)
            original = EventParticipation.objects.filter(psycho_reports=instance)
            original.filter(~Q(id__in=[item.get('id') for item in events if 'id' in item])).delete()
            instance.events.set(self.create_or_update_events(events))
            instance.save()
            return instance
        return super().create(validated_data)
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        events = validated_data.pop('events', None)
        if events is not None:
            original = EventParticipation.objects.filter(psycho_reports=instance)
            original.filter(~Q(id__in=[item.get('id') for item in events if 'id' in item])).delete()
            instance.events.set(self.create_or_update_events(events))
            instance.save()
        return super().update(instance, validated_data)

class StudentReportPsychologistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    psycho_report = serializers.SerializerMethodField('get_psycho_report')
    events = serializers.SerializerMethodField('get_events')
    class Meta:
        model = ProfileStudent
        fields = '__all__'
    def get_psycho_report(self, instance):
        report_queryset = ReportPsychologist.objects.filter(student=instance)
        period = self.context.get("period", None)
        class_year = self.context.get("class_year", None)
        author = self.context.get("author", None)
        if period:
            report_queryset = report_queryset.filter(period=period)
        if author:
            report_queryset = report_queryset.filter(author=author)
        if class_year:
            report_queryset = report_queryset.filter(year=class_year)
        serializer = ReportPsychologistSerializer(instance=report_queryset.first(), context=self.context)
        return serializer.data
    def get_events(self, instance):
        period_id = self.context.get("period", None)
        class_year_id = self.context.get("class_year", None)
        events_queryset = EventParticipation.objects.filter(teacher_reports__student=instance, 
                                                            teacher_reports__period=period_id,
                                                            teacher_reports__year=class_year_id)
        serializer = EventParticipationDetailSerializer(instance=events_queryset, many=True, context=self.context)
        return serializer.data

######################
# РЕПОРТЫ НАСТАВНИКА #
######################

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
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        events = validated_data.pop('events', None)
        if events is not None:
            instance = ReportMentor.objects.create(**validated_data)
            original = EventParticipation.objects.filter(mentor_reports=instance)
            original.filter(~Q(id__in=[item.get('id') for item in events if 'id' in item])).delete()
            instance.events.set(self.create_or_update_events(events))
            instance.save()
            return instance
        return super().create(validated_data)
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        events = validated_data.pop('events', None)
        if events is not None:
            original = EventParticipation.objects.filter(mentor_reports=instance)
            original.filter(~Q(id__in=[item.get('id') for item in events if 'id' in item])).delete()
            instance.events.set(self.create_or_update_events(events))
            instance.save()
        return super().update(instance, validated_data)

class ReportTeacherSmallSerializer(serializers.ModelSerializer):
    author = ProfileTeacherSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = ReportTeacher
        fields = ['subject', 'author']

class ReportPsychologistSmallSerializer(serializers.ModelSerializer):
    author = ProfileTeacherSerializer(read_only=True)
    class Meta:
        model = ReportPsychologist
        fields = ['author']

class EventParticipationDetailSerializer(serializers.ModelSerializer):
    type = EventTypeSerializer(read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    level_name = serializers.CharField(source='get_level_display', read_only=True)
    # teacher_reports = ReportTeacherSmallSerializer(many=True, read_only=True)
    teacher_report = serializers.SerializerMethodField('get_teacher_report')
    psycho_report = serializers.SerializerMethodField('get_psycho_report')
    class Meta:
        model = EventParticipation
        fields = ['id', 'type', 'type_name', 'level', 'level_name', 'type', 'title', 'result', 'teacher_report', 'psycho_report']
    def get_teacher_report(self, instance):
        report_queryset = ReportTeacher.objects.filter(events__in=[instance])
        serializer = ReportTeacherSmallSerializer(instance=report_queryset.first(), context=self.context)
        return serializer.data
    def get_psycho_report(self, instance):
        report_queryset = ReportPsychologist.objects.filter(events__in=[instance])
        serializer = ReportPsychologistSmallSerializer(instance=report_queryset.first(), context=self.context)
        return serializer.data

class StudentReportMentorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    mentor_report = serializers.SerializerMethodField('get_mentor_report')
    events = serializers.SerializerMethodField('get_events')
    class Meta:
        model = ProfileStudent
        fields = '__all__'
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
    def get_events(self, instance):
        period_id = self.context.get("period", None)
        class_year_id = self.context.get("class_year", None)
        events_queryset = EventParticipation.objects.filter(Q(teacher_reports__student=instance, 
                                                            teacher_reports__period=period_id,
                                                            teacher_reports__year=class_year_id) | 
                                                            Q(psycho_reports__student=instance,
                                                              psycho_reports__period=period_id,
                                                              psycho_reports__year=class_year_id,))
        serializer = EventParticipationDetailSerializer(instance=events_queryset, many=True, context=self.context)
        return serializer.data
    def to_representation(self, instance):
        result = super(StudentReportMentorSerializer, self).to_representation(instance)
        class_year_id = self.context.get("class_year", None)
        period_id = self.context.get("period", None)
        class_year = ClassYear.objects.filter(pk=class_year_id).first()
        subject_queryset = Subject.objects.filter(plan__class_year=class_year_id, group_ib__program=class_year.program)
        # subject_queryset = Subject.objects.filter(group_ib__program=class_year.program)
        subject_reports = list(subject_queryset.values('id', 'name_rus'))
        subjects = list(subject_queryset.values_list('id', flat=True))
        report_teacher_queryset = ReportTeacher.objects.filter(student=instance,
                                               period=period_id,
                                               year=class_year_id,
                                               subject__in=subjects)
        reports = list(report_teacher_queryset.values('subject__id', 'subject__group_ib', 'text', 'author_id', 
                                              'author__user__first_name', 'author__user__last_name', 'author__user__middle_name', 
                                              'criterion_a', 'criterion_b', 'criterion_c', 'criterion_d')) 
        for subject in subject_reports:
            for report in reports:
                if subject['id'] == report['subject__id']:
                    subject['group'] = report['subject__group_ib']
                    subject['text'] = report['text']
                    subject['author_name'] = f"{report['author__user__last_name']} {report['author__user__first_name']} {report['author__user__middle_name']}"
                    subject['author_id'] = report['author_id']
                    subject['criteria'] = {'criterion_a': report['criterion_a'],
                                           'criterion_b': report['criterion_b'],
                                           'criterion_c': report['criterion_c'],
                                           'criterion_d': report['criterion_d']}
                    break
        
        result['subject_reports'] = subject_reports
        report_psycho_queryset = ReportPsychologist.objects.filter(student=instance,
                                                                    period=period_id,
                                                                    year=class_year_id).first()
        result['psycho_report'] = ReportPsychologistSerializer(instance=report_psycho_queryset, context=self.context).data
        return result
    

class WorkLoadSerializer(serializers.ModelSerializer):
    study_year = StudyYearSerializer(read_only=True)
    teacher = ProfileTeacherSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    group = ClassGroupSimpleSerializer(read_only=True)
    class Meta:
        model = WorkLoad
        fields = '__all__'


class TextTranslateSerailizer(serializers.Serializer):
    text = serializers.CharField()
    language = serializers.CharField()

class GenerateReportSerailizer(serializers.Serializer):
    name = serializers.CharField()
    subject = serializers.CharField()
    text = serializers.CharField()