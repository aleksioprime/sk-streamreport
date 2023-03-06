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

class SummativeWorkViewSet(viewsets.ModelViewSet):
    queryset = SummativeWork.objects.all()
    serializer_class = SummativeWorkSerializer

class WorkAssessmentViewSet(viewsets.ModelViewSet):
    queryset = WorkAssessment.objects.all()
    serializer_class = WorkAssessmentSerializer

class WorkCriteriaMarkViewSet(viewsets.ModelViewSet):
    queryset = WorkCriteriaMark.objects.all()
    serializer_class = WorkCriteriaMarkSerializer