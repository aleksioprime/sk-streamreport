from rest_framework import serializers
from member.models import User, RoleUser, Department, ProfileStudent, ProfileTeacher
from assess.models import ClassGroup
from curriculum.serializers import SubjectSerializer, UnitMYPSerializerListCreate

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleUser
        fields = '__all__'
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        
class ClassGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassGroup
        fields = '__all__'

class ProfileStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileStudent
        fields = ['id', 'id_dnevnik']

class ProfileTeacherSerializer(serializers.ModelSerializer):
    units = UnitMYPSerializerListCreate(source='unitplan_myp', many=True, read_only=True)
    class Meta:
        model = ProfileTeacher
        fields = ['id', 'id_dnevnik', 'units', 'position', 'admin']

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True, read_only=True)
    student = ProfileStudentSerializer(required=False)
    teacher = ProfileTeacherSerializer(required=False)
    class Meta:
        model = User
        fields = ["id", "id_str", "username", "email", "first_name", "middle_name", 
                  "last_name", "last_login", "date_of_birth", "gender", "role", "student", 
                  "teacher", "photo", 'roles_ids', 'is_staff', 'password']
        read_only_fields = ['photo', 'is_staff']
        write_only_fields = ["password"]
        # extra_kwargs = {'username': {'required': False}, 'role': {'validators': []}}
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'roles_ids': {'source': 'role', 'write_only': True},
            }
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            middle_name=validated_data.get('middle_name'),
            date_of_birth=validated_data.get('date_of_birth'),
            gender=validated_data.get('gender'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        if 'teacher' in validated_data:
            teacher = ProfileTeacher.objects.create(user=user, **validated_data.get('teacher'))
            print('Создан учитель:', teacher)
        if 'student' in validated_data:
            print("Добавление студента")
            student = ProfileStudent.objects.create(user=user, **validated_data.get('student'))
            print('Создан студент:', student)
        return user
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        if 'student' in validated_data:
            ProfileStudent.objects.update_or_create(user=instance, defaults=dict(validated_data.get('student')))
            validated_data.pop('student')
        if 'teacher' in validated_data:
            ProfileTeacher.objects.update_or_create(user=instance, defaults=dict(validated_data.get('teacher')))
            validated_data.pop('teacher')
        return super().update(instance, validated_data)

class UserImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"