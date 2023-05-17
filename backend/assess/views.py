from django.shortcuts import render
from rest_framework import viewsets
from assess.serializers import StudyYearSerializer, ClassGroupSerializer, ClassGroupExtraSerializer,  StudyPeriodSerializer, SummativeWorkSerializer, \
    WorkAssessmentSerializer, WorkCriteriaMarkSerializer, ProfileStudentSerializer, WorkGroupDateItemSerializer, \
    PeriodAssessmentSerializer, StudentWorkSerializer, ReportPeriodSerializer, StudentReportTeacherSerializer, ReportTeacherSerializer, \
    EventTypeSerializer, EventParticipationSerializer, StudentReportMentorSerializer, ReportMentorSerializer, ClassGroupStudentsSerializer, \
    WorkLoadSerializer
from curriculum.serializers import ClassYearSerializer, SubjectSerializer      
 
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkAssessment, WorkCriteriaMark, WorkGroupDate, PeriodAssessment, \
    ReportPeriod, ReportTeacher, EventType, EventParticipation, ReportMentor, WorkLoad
from member.models import ProfileTeacher, ProfileStudent, User
from curriculum.models import ClassYear, Subject

from rest_framework.response import Response
from rest_framework.views import APIView

import requests
from datetime import datetime
import locale

class StudyYearViewSet(viewsets.ModelViewSet):
    queryset = StudyYear.objects.all()
    serializer_class = StudyYearSerializer


class ClassGroupViewSet(viewsets.ModelViewSet):
    queryset = ClassGroup.objects.all()
    default_serializer_class = ClassGroupSerializer
    serializer_classes = {
        'retrieve': ClassGroupExtraSerializer,
        'update': ClassGroupExtraSerializer,
    }
    def get_queryset(self):
        class_year = self.request.query_params.get("class_year", None)
        study_year = self.request.query_params.get("study_year", None)
        program = self.request.query_params.get("program", None)
        teacher = self.request.query_params.get("teacher", None)
        groups = ClassGroup.objects.all()
        if class_year:
            groups = groups.filter(class_year=class_year)
        if study_year:
            groups = groups.filter(study_year=study_year)
        if program:
            groups = groups.filter(class_year__program=program)
        if teacher:
            groups = groups.filter(workload__teacher=teacher)
        return groups
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class ClassGroupStudentsViewSet(viewsets.ModelViewSet):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupStudentsSerializer
    def get_queryset(self):
        class_year = self.request.query_params.get("class_year", None)
        study_year = self.request.query_params.get("study_year", None)
        program = self.request.query_params.get("program", None)
        teacher = self.request.query_params.get("teacher", None)
        groups = ClassGroup.objects.all()
        if class_year:
            groups = groups.filter(class_year=class_year)
        if study_year:
            groups = groups.filter(study_year=study_year)
        if program:
            groups = groups.filter(class_year__program=program)
        if teacher:
            groups = groups.filter(workload__teacher=teacher)
        return groups

# Набор CRUD-методов для работы с моделью Студенты
class StudentViewSet(viewsets.ModelViewSet):
    queryset = ProfileStudent.objects.all()
    serializer_class = ProfileStudentSerializer
    def get_queryset(self):
        group = self.request.query_params.get("class", None)
        year = self.request.query_params.get("year", None)
        students = ProfileStudent.objects.all()
        if group:
            print(f"Get-запрос class: {group}")
            students = students.filter(groups__in=[group])
        if year:
            print(f"Get-запрос year: {year}")
            students = students.filter(groups__class_year__in=[year])
        print(f"Ответ от сервера: {students}")
        return students

class StudyPeriodViewSet(viewsets.ModelViewSet):
    queryset = StudyPeriod.objects.all()
    serializer_class = StudyPeriodSerializer
    def get_queryset(self):
        study_period = StudyPeriod.objects.all()
        study_year = self.request.query_params.get("study_year", None)
        program = self.request.query_params.get("program", None)
        if study_year:
            study_period = study_period.filter(study_year=study_year)
        if program:
            study_period = study_period.filter(class_year__program__in=[program]).distinct()
        return study_period


class SummativeWorkViewSet(viewsets.ModelViewSet):
    queryset = SummativeWork.objects.all()
    serializer_class = SummativeWorkSerializer
    def get_queryset(self):
        summative_work = SummativeWork.objects.all()
        period = self.request.query_params.get("period", None)
        teacher = self.request.query_params.get("teacher", None)
        group = self.request.query_params.get("group", None)
        subject = self.request.query_params.get("subject", None)
        if period:
            summative_work = summative_work.filter(period=period)
        if teacher:
            summative_work = summative_work.filter(teacher=teacher)
        if group:
            summative_work = summative_work.filter(groups__in=[group]).distinct()
        if subject:
            summative_work = summative_work.filter(subject=subject)
        print(f"[SummativeWork] Ответ от сервера: {summative_work}")
        return summative_work

class WorkGroupDateItemViewSet(viewsets.ModelViewSet):
    queryset = WorkGroupDate.objects.all()
    serializer_class = WorkGroupDateItemSerializer
    def get_queryset(self):
        workgroup = WorkGroupDate.objects.all()
        work = self.request.query_params.get("work", None)
        if work:
            workgroup = workgroup.filter(student__group=work)
        return workgroup

class WorkAssessmentViewSet(viewsets.ModelViewSet):
    queryset = WorkAssessment.objects.all()
    serializer_class = WorkAssessmentSerializer
    def get_queryset(self):
        work_assessment = WorkAssessment.objects.all()
        group = self.request.query_params.get("class", None)
        if group:
            # print(f"[WorkAssessment] Get-запрос period: {group}")
            work_assessment = work_assessment.filter(student__group=group)
        # print(f"[WorkAssessment] Ответ от сервера: {work_assessment}")
        return work_assessment
    def update(self, request, pk=None, *args, **kwargs):
        print('Переданные данные: ', request.data)
        return super().update(request, pk=None, *args, **kwargs)

class WorkAssessmentGiveMarksAPIView(APIView):
    def post(self, request):
        if 'marks' in request.data:
            marks = request.data['marks']
            print(marks)
            queryset = WorkAssessment.objects.filter(id__in=marks.keys())
            for element in queryset:
                if not element.grade and type(marks[str(element.id)]) == int:
                    element.grade = marks[str(element.id)]
                    element.save()
            print(queryset)
        return Response({'result': WorkAssessmentSerializer(queryset, many=True).data})


class WorkCriteriaMarkViewSet(viewsets.ModelViewSet):
    queryset = WorkCriteriaMark.objects.all()
    serializer_class = WorkCriteriaMarkSerializer

class PeriodAssessmentViewSet(viewsets.ModelViewSet):
    queryset = PeriodAssessment.objects.all()
    serializer_class = PeriodAssessmentSerializer
    def get_queryset(self):
        period_assessment = PeriodAssessment.objects.all()
        student = self.request.query_params.get("student", None)
        period = self.request.query_params.get("period", None)
        subject = self.request.query_params.get("subject", None)
        year = self.request.query_params.get("year", None)
        if student:
            period_assessment = period_assessment.filter(student=student)
        if period:
            period_assessment = period_assessment.filter(period=period)
        if subject:
            period_assessment = period_assessment.filter(subject=subject)
        if year:
            period_assessment = period_assessment.filter(year=year)
        return period_assessment
    
class StudentWorkViewSet(viewsets.ModelViewSet):
    queryset = ProfileStudent.objects.all()
    serializer_class = StudentWorkSerializer
    def get_queryset(self):
        group = self.request.query_params.get("group", None)
        students = ProfileStudent.objects.all()
        if group:
            students = students.filter(groups__in=[group]).distinct()
        return students
    def get_serializer_context(self, *args, **kwargs):
        period = self.request.query_params.get("period", None)
        group = self.request.query_params.get("group", None)
        class_year = self.request.query_params.get("class_year", None)
        subject = self.request.query_params.get("subject", None)
        context = super().get_serializer_context()
        if period:
            context.update({"period": period})
        if group:
            context.update({"group": group})
        if group:
            context.update({"class_year": class_year})
        if subject:
            context.update({"subject": subject})
        return context

def get_marks_for_period_dnevnik(token, group, period, date):
    url_dnevnik_api = 'https://api.dnevnik.ru/v2/'
    headers = {
        'Access-Token': f'{token}',
        'Content-Type': 'application/json'
        }
    url = f'{url_dnevnik_api}edu-groups/{group}/reporting-periods/{period}/avg-marks/{date}'
    return requests.get(url, headers=headers)

class AssessmentJournalAPIView(APIView):
    def get(self, request):
        period_id = request.query_params.get("period", None)
        group_id = request.query_params.get("group", None)
        subject_id = request.query_params.get("subject", None)
        period = StudyPeriod.objects.filter(id=period_id).first()
        subject = Subject.objects.filter(id=subject_id).first()
        group = ClassGroup.objects.filter(id=group_id).first()
        return Response({
            'period': StudyPeriodSerializer(period).data,
            'group': ClassGroupSerializer(group).data,
            'subject': SubjectSerializer(subject).data,
            })

class AssessmentDnevnikAPIView(APIView):
    def get(self, request):
        period_dnevnik = request.query_params.get("period_dnevnik", None)
        group_dnevnik = request.query_params.get("group_dnevnik", None)
        subject_dnevnik = request.query_params.get("subject_dnevnik", None)
        user = request.query_params.get("user", None)
        user_queryset = User.objects.filter(id=user).first()
        response = get_marks_for_period_dnevnik(user_queryset.access_token_dnevnik,
                                                group_dnevnik,
                                                period_dnevnik,
                                                datetime.now().strftime("%Y-%m-%d"))
        student_mark = {}
        result = False
        if response.status_code == 200:
            for data in response.json():
                marks = list(filter(lambda mark: mark['subject_str'] == subject_dnevnik, data['per-subject-averages']))
                if marks:
                    student_mark[data['person_str']] = list(map(lambda mark: float(mark['avg-mark-value'].replace(',','.')), marks))[0]
            result = True
        elif response.json()['type'] == 'invalidToken':
            print('Ошибка токена доступа. Токен сброшен')
            user_queryset.access_token_dnevnik = ''
            user_queryset.save()
        else:
            print(f'Ошибка запроса: {response.json()}')
        return Response({
            'result': result,
            'marks': student_mark,
            })

class ReportTeacherJournalAPIView(APIView):
    def get(self, request):
        group_id = request.query_params.get("group", None)
        period_id = request.query_params.get("period", None)
        subject_id = request.query_params.get("subject", None)
        period = ReportPeriod.objects.filter(id=period_id).first()
        subject = Subject.objects.filter(id=subject_id).first()
        group = ClassGroup.objects.filter(id=group_id).first()
        types = EventType.objects.all()
        return Response({
            'group': ClassGroupSerializer(group).data,
            'subject': SubjectSerializer(subject).data,
            'period': ReportPeriodSerializer(period).data,
            'event_types': EventTypeSerializer(types, many=True).data
            })

class ReportMentorJournalAPIView(APIView):
    def get(self, request):
        group_id = request.query_params.get("group", None)
        period_id = request.query_params.get("period", None)
        period = ReportPeriod.objects.filter(id=period_id).first()
        group = ClassGroup.objects.filter(id=group_id).first()
        types = EventType.objects.all()
        return Response({
            'group': ClassGroupSerializer(group).data,
            'period': ReportPeriodSerializer(period).data,
            'event_types': EventTypeSerializer(types, many=True).data
            })

class ReportPeriodViewSet(viewsets.ModelViewSet):
    queryset = ReportPeriod.objects.all()
    serializer_class = ReportPeriodSerializer
    def get_queryset(self):
        report_period = ReportPeriod.objects.all()
        study_year = self.request.query_params.get("study_year", None)
        if study_year:
            report_period = report_period.filter(study_year=study_year)
        return report_period
    
class StudentReportTeacherViewSet(viewsets.ModelViewSet):
    queryset = ProfileStudent.objects.all()
    serializer_class = StudentReportTeacherSerializer
    def get_queryset(self):
        group = self.request.query_params.get("group", None)
        class_year = self.request.query_params.get("class_year", None)
        students = ProfileStudent.objects.all()
        if group:
            students = students.filter(groups__in=[group]).distinct()
        if class_year:
            students = students.filter(groups__class_year__in=[class_year]).distinct()
        return students
    def get_serializer_context(self, *args, **kwargs):
        period = self.request.query_params.get("period", None)
        class_year = self.request.query_params.get("class_year", None)
        subject = self.request.query_params.get("subject", None)
        author = self.request.query_params.get("author", None)
        context = super().get_serializer_context()
        if period:
            context.update({"period": period})
        if subject:
            context.update({"subject": subject})
        if author:
            context.update({"author": author})
        if class_year:
            context.update({"class_year": class_year})
        return context

class StudentReportMentorViewSet(viewsets.ModelViewSet):
    queryset = ProfileStudent.objects.all()
    serializer_class = StudentReportMentorSerializer
    def get_queryset(self):
        group = self.request.query_params.get("group", None)
        class_year = self.request.query_params.get("class_year", None)
        students = ProfileStudent.objects.all()
        if group:
            students = students.filter(groups__in=[group]).distinct()
        if class_year:
            students = students.filter(groups__class_year__in=[class_year]).distinct()
        return students
    def get_serializer_context(self, *args, **kwargs):
        period = self.request.query_params.get("period", None)
        class_year = self.request.query_params.get("class_year", None)
        study_year = self.request.query_params.get("study_year", None)
        author = self.request.query_params.get("author", None)
        context = super().get_serializer_context()
        if period:
            context.update({"period": period})
        if study_year:
            context.update({"study_year": study_year})
        if author:
            context.update({"author": author})
        if class_year:
            context.update({"class_year": class_year})
        return context

class ReportTeacherViewSet(viewsets.ModelViewSet):
    queryset = ReportTeacher.objects.all()
    serializer_class = ReportTeacherSerializer

class ReportMentorViewSet(viewsets.ModelViewSet):
    queryset = ReportMentor.objects.all()
    serializer_class = ReportMentorSerializer

class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer

class EventParticipationViewSet(viewsets.ModelViewSet):
    queryset = EventParticipation.objects.all()
    serializer_class = EventParticipationSerializer
    def get_queryset(self):
        event_participation = EventParticipation.objects.all()
        type = self.request.query_params.get("type", None)
        level = self.request.query_params.get("level", None)
        student = self.request.query_params.get("student", None)
        if type:
            event_participation = event_participation.filter(type=type)
        if level:
            event_participation = event_participation.filter(level=level)
        if student:
            event_participation = event_participation.filter(teacher_reports__student__in=[student], mentor_reports__student__in=[student])
        return event_participation
    
class WorkLoadViewSet(viewsets.ModelViewSet):
    queryset = WorkLoad.objects.all()
    serializer_class = WorkLoadSerializer
    def get_queryset(self):
        workload = WorkLoad.objects.all()
        teacher = self.request.query_params.get("teacher", None)
        study_year = self.request.query_params.get("study_year", None)
        if teacher:
            workload = workload.filter(teacher=teacher)
        if study_year:
            workload = workload.filter(study_year=study_year)
        return workload