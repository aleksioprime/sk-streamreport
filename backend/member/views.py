from django.shortcuts import render
from rest_framework import routers, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from member.serializers import UserSerializer, DepartmentSerializer, RoleSerializer, ClassGroupSerializer, UserImportSerializer, ProfileStudentSerializer
from member.models import User, Department, RoleUser, ProfileStudent, ProfileTeacher
from assess.models import ClassGroup
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import get_object_or_404
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from django.db.models import Q
import csv
import jwt, openpyxl
import pandas as pd
from django.forms.models import model_to_dict
from datetime import datetime

temp_storage = FileSystemStorage(location='tmp/')

# Получение пользователя по JWT-токену
class UserAuth(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        token = request.headers['Authorization'].split()[1]
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256', 'HS384', 'HS512'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        # print(payload)
        user =  User.objects.filter(id=payload['user_id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)    

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    
class RoleUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RoleUser.objects.all()
    serializer_class = RoleSerializer

class ClassGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupSerializer
    def get_queryset(self):
        # добавить фильтрацию по текущему учебному году
        return ClassGroup.objects.filter(study_year=1)

class UsersSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50

# Набор CRUD-методов для работы с моделью Пользователи
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UsersSetPagination
    def get_queryset(self):
        role = self.request.query_params.get("role", None)
        search = self.request.query_params.get("search", None)
        users = User.objects.all()
        if role == 'teacher':
            users = users.filter(teacher__isnull=False)
        if role == 'student':
            users = users.filter(student__isnull=False)
        if search:
            users = users.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search))
        return users
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk=None, *args, **kwargs)
    def update(self, request, pk=None, *args, **kwargs):
        print('Переданные данные для редактирования: ', request.data)
        return super().update(request, pk=None, *args, **kwargs)
    def destroy(self, request, pk=None, *args, **kwargs):
        print('Переданные данные для удаления: ', pk)
        return super().destroy(request, pk=None, *args, **kwargs)

# # Разлогинивание пользователя и удаление токенов
# class Logout(APIView):
#     def post(self, request):
#         response = Response()
#         response.delete_cookie('jwt_token')
#         response.delete_cookie('jwt_refresh')
#         response.data = {'message': 'success'}
#         return response

# Создание путей для CRUD-методов модели Пользователи
# def get_router_urls():
#     router = routers.DefaultRouter()
#     router.register(r'user', UserViewSet, basename='user')
#     return router.urls

# Экспорт пользователей через CSV
@csrf_exempt
def import_users(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel')
        if excel_file:
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb.active
            for value in worksheet.iter_rows(values_only=True):
                print(value)
            return JsonResponse({'data':'success'})
    return JsonResponse({'data':'fail'})

class UserImportView(APIView):
    def post(self, request):
        file = request.FILES.get('import')
        if file is None:
            return Response({'Message': 'No FILE'})
        content = file.read()
        file_content = ContentFile(content)
        file_name = temp_storage.save("_tmp.xlsx", file_content)
        tmp_file = temp_storage.path(file_name)
        
        # csv_file = open(tmp_file, errors="ignore")
        # reader = csv.reader(csv_file, delimiter=';')
        # next(reader)
        
        dfs = pd.read_excel(tmp_file, engine='openpyxl').fillna('')
        applicant_list = dfs.to_dict('records')
        validated_list = [obj for obj in applicant_list if User.objects.filter(username=obj['username']).first() is None]
        
        temp_storage.delete(file_name)
        return Response({
            'applicant_users': applicant_list,
            'validated_users': validated_list,
            'file_import': file_name})

class UserImportApply(APIView):
    def post(self, request):
        users_import = request.data.get("users_import", None)
        valid_data = lambda x : None if x=="NaT" else datetime.fromisoformat(x)
        if users_import:
            for item in users_import:
                print(item)
                if User.objects.filter(username=item['username']).first() is None:
                    user = User.objects.create(
                        username=item['username'],
                        email=item['email'],
                        password=make_password(item['password']),
                        first_name=item['first_name'],
                        middle_name=item['middle_name'],
                        last_name=item['last_name'],
                        date_of_birth=valid_data(item['date_of_birth']),
                        gender=item['gender'],
                        position=item['position'],
                    )
                    roles_list = [RoleUser.objects.filter(codename=x).first().id for x in item['role'].split(',')]
                    user.role.set(roles_list)
                    if 1 in roles_list:
                        student = ProfileStudent.objects.create(user=user, id_dnevnik=item['id_dnevnik_student'], group=item['group'])
                    if 2 in roles_list:
                        teacher = ProfileTeacher.objects.create(user=user, id_dnevnik=item['id_dnevnik_teacher'])
        return Response(UserSerializer(User.objects.all(), many=True).data)