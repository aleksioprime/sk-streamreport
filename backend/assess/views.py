from django.shortcuts import render
from rest_framework import viewsets
from assess.serializers import StudyYearSerializer, ClassGroupSerializer, ClassGroupExtraSerializer,  StudyPeriodSerializer, SummativeWorkSerializer, \
    WorkAssessmentSerializer, WorkCriteriaMarkSerializer, ProfileStudentSerializer, WorkGroupDateItemSerializer, \
    PeriodAssessmentSerializer, StudentWorkSerializer, ReportPeriodSerializer, StudentReportTeacherSerializer, ReportTeacherSerializer, \
    EventTypeSerializer, EventParticipationSerializer
from curriculum.serializers import ClassYearSerializer, SubjectSerializer      
 
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkAssessment, WorkCriteriaMark, WorkGroupDate, PeriodAssessment, \
    ReportPeriod, ReportTeacher, EventType, EventParticipation
from member.models import ProfileTeacher, ProfileStudent, User
from curriculum.models import ClassYear, Subject

from rest_framework.response import Response
from rest_framework.views import APIView

class StudyYearViewSet(viewsets.ModelViewSet):
    queryset = StudyYear.objects.all()
    serializer_class = StudyYearSerializer


class ClassGroupViewSet(viewsets.ModelViewSet):
    queryset = ClassGroup.objects.all()
    # serializer_class = ClassGroupSerializer
    default_serializer_class = ClassGroupSerializer
    serializer_classes = {
        'retrieve': ClassGroupExtraSerializer,
        'update': ClassGroupExtraSerializer,
    }
    def get_queryset(self):
        class_year = self.request.query_params.get("class_year", None)
        study_year = self.request.query_params.get("study_year", None)
        groups = ClassGroup.objects.all()
        if class_year:
            groups = groups.filter(class_year=class_year)
        if study_year:
            groups = groups.filter(study_year=study_year)
        return groups
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


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
        year = self.request.query_params.get("year", None)
        subject = self.request.query_params.get("subject", None)
        if period:
            summative_work = summative_work.filter(period=period)
        if teacher:
            summative_work = summative_work.filter(teacher=teacher)
        if year:
            summative_work = summative_work.filter(groups__class_year=year).distinct()
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
        group = self.request.query_params.get("class", None)
        year = self.request.query_params.get("year", None)
        students = ProfileStudent.objects.all()
        if group:
            students = students.filter(groups__in=[group]).distinct()
        if year:
            students = students.filter(groups__class_year__in=[year]).distinct()
        return students
    def get_serializer_context(self, *args, **kwargs):
        period = self.request.query_params.get("period", None)
        year = self.request.query_params.get("year", None)
        subject = self.request.query_params.get("subject", None)
        context = super().get_serializer_context()
        if period:
            context.update({"period": period})
        if year:
            context.update({"year": year})
        if subject:
            context.update({"subject": subject})
        return context
    
class AssessmentJournalAPIView(APIView):
    def get(self, request):
        period = request.query_params.get("period", None)
        year = request.query_params.get("year", None)
        subject = request.query_params.get("subject", None)
        period_queryset = StudyPeriod.objects.filter(id=period).first()
        year_queryset = ClassYear.objects.filter(id=year).first()
        subject_queryset = Subject.objects.filter(id=subject).first()
        groups_queryset = ClassGroup.objects.filter(class_year=year_queryset.year_rus)
        return Response({
            'period': StudyPeriodSerializer(period_queryset).data,
            'year': ClassYearSerializer(year_queryset).data,
            'groups': ClassGroupSerializer(groups_queryset, many=True).data,
            'subject': SubjectSerializer(subject_queryset).data
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
        study_year = self.request.query_params.get("class_year", None)
        study_year = self.request.query_params.get("study_year", None)
        subject = self.request.query_params.get("subject", None)
        author = self.request.query_params.get("author", None)
        context = super().get_serializer_context()
        if period:
            context.update({"period": period})
        if study_year:
            context.update({"study_year": study_year})
        if subject:
            context.update({"subject": subject})
        if author:
            context.update({"author": author})
        if study_year:
            context.update({"study_year": author})
        return context

class ReportTeacherViewSet(viewsets.ModelViewSet):
    queryset = ReportTeacher.objects.all()
    serializer_class = ReportTeacherSerializer

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