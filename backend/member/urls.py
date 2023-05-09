from xml.etree.ElementInclude import include
from django.urls import path
from member.views import UserAuth, DepartmentViewSet, ClassGroupViewSet, UserViewSet, \
    UserImportView, UserImportApply, UserCreateViewSet, TeacherViewSet


urlpatterns = [
    path('auth', UserAuth.as_view()),
    path('department', DepartmentViewSet.as_view({'get': 'list'})),
    path('group', ClassGroupViewSet.as_view({'get': 'list'})),
    path('user/load', UserImportView.as_view()),
    path('user/import', UserImportApply.as_view()),
    path('user', UserCreateViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('user/<int:pk>', UserViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('teachers', TeacherViewSet.as_view({'get': 'list'})),
]