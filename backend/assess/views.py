from django.shortcuts import render
from rest_framework import viewsets
from assess.serializers import StudyYearSerializer, ClassGroupSerializer, StudyPeriodSerializer, SummativeWorkSerializer, \
    WorkAssessmentSerializer, WorkCriteriaMarkSerializer
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkAssessment, WorkCriteriaMark
from member.models import ProfileTeacher, ProfileStudent, User


class StudyYearViewSet(viewsets.ModelViewSet):
    queryset = StudyYear.objects.all()
    serializer_class = StudyYearSerializer


class ClassGroupViewSet(viewsets.ModelViewSet):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupSerializer


class StudyPeriodViewSet(viewsets.ModelViewSet):
    queryset = StudyPeriod.objects.all()
    serializer_class = StudyPeriodSerializer

    def get_queryset(self):
        study_period = StudyPeriod.objects.all()
        study_year = self.request.query_params.get("study_year", None)
        if study_year:
            study_period = study_period.filter(study_year=study_year)
        return study_period


class SummativeWorkViewSet(viewsets.ModelViewSet):
    queryset = SummativeWork.objects.all()
    serializer_class = SummativeWorkSerializer

    def get_queryset(self):
        summative_work = SummativeWork.objects.all()
        period = self.request.query_params.get("period", None)
        teacher = self.request.query_params.get("teacher", None)
        if period:
            print(f"[SummativeWork] Get-запрос period: {period}")
            summative_work = summative_work.filter(period=period)
        if teacher:
            print(f"[SummativeWork] Get-запрос period: {teacher}")
            summative_work = summative_work.filter(teacher=teacher)
        print(f"[SummativeWork] Ответ от сервера: {summative_work}")
        return summative_work


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
