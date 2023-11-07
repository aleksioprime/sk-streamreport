from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

from django.utils.translation import gettext_lazy as _

class GenderChoices(models.TextChoices):
        MALE = "male", "Мужчина"
        FEMALE = "female", "Женщина"
        NONE = None, "Не указан"

class ProgramIbChoices(models.TextChoices):
        PYP = "pyp", "Primary Years Programme"
        MYP = "myp", "Middle Years Programme"
        DP = "dp", "Diploma Programme"
        NONE = None, "No program"

class LevelNationChoices(models.TextChoices):
        NOO = "noo", "Начальная школа"
        OOO = "ooo", "Средняя школа"
        SOO = "soo", "Старшая школа"
        NONE = None, "Не указано"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    """ Расширеная модель пользователя """
    username = None
    email = models.EmailField(verbose_name=_("Электронная почта"), unique=True)
    last_name = models.CharField(verbose_name=_("Фамилия"), max_length=30, blank=True)
    first_name = models.CharField(verbose_name=_("Имя"), max_length=30, blank=True)
    middle_name = models.CharField(verbose_name=_("Отчество"), max_length=32, null=True, blank=True)
    gender = models.CharField(verbose_name=_("Пол"), max_length=6, choices=GenderChoices.choices, default='none', null=True, blank=True)
    photo = models.ImageField(verbose_name=_("Фотография"), upload_to="member_photos", blank=True, null=True)
    dnevnik_token = models.CharField(verbose_name=_("Токен доступа в Дневник"), max_length=255, null=True, blank=True)
    dnevnik_id = models.CharField(verbose_name=_("ID пользователя Дневника"), max_length=40, blank=True, null=True)
    last_activity = models.DateTimeField(verbose_name=_("Последняя активность"), auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name', 'is_active']
    def get_full_name(self):
        if not self.middle_name:
            full_name = f"{self.last_name} {self.first_name}"
        else:
            full_name = f"{self.last_name} {self.first_name} {self.middle_name}"
        return full_name.strip()
    def get_short_name(self):
        if self.first_name and self.middle_name:
            return f"{self.last_name} {self.first_name[0]}. {self.middle_name[0]}."
        elif self.first_name:
            return f"{self.last_name} {self.first_name[0]}."
        else:
            return f"{self.last_name} {self.first_name}"
    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Department(models.Model):
    """ Учебные подразделения / Кафедры """
    name = models.CharField(max_length=255, verbose_name=_("Название кафедры"))
    logo = models.ImageField(upload_to="department_logos", blank=True, verbose_name=_("Фотография"), null=True)
    employees = models.ManyToManyField('general.user', verbose_name=_("Сотрудники"), related_name="departments")
    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ['name']
    def __str__(self):
        return f'{self.name}'

class AcademicYear(models.Model):
    """ Учебные года """
    name = models.CharField(max_length=32, verbose_name=_("Учебный год"))
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    class Meta:
        verbose_name = 'Учебный год'
        verbose_name_plural = 'Учебные года'
        ordering = ['date_start']
    def __str__(self):
        return f"{self.name}"

class StudyYear(models.Model):
    """ Параллель обучения """
    number = models.PositiveIntegerField(verbose_name=_("Год обучения"))
    number_ib = models.CharField(max_length=12, verbose_name=_("Год обучения в IB"), null=True)
    level = models.CharField(verbose_name=_("Национальные уровни образования"), choices=LevelNationChoices.choices, default=None, max_length=4)
    program_ib = models.CharField(verbose_name=_("IB-программа"), choices=ProgramIbChoices.choices, default=None, null=True, max_length=4)
    class Meta:
        verbose_name = 'Параллель обучения'
        verbose_name_plural = 'Параллели обучения'
        ordering = ['number']
    def __str__(self):
        if self.number_ib is not None:
            return f"{self.number} класс ({self.number_ib} {self.program_ib.upper()})"
        else:
            return f"{self.number} класс"

class ClassGroup(models.Model):
    """ Учебные классы """
    year_academic = models.ForeignKey('general.AcademicYear', verbose_name=_("Учебный год"), on_delete=models.CASCADE, null=True, related_name="classes")
    year_study = models.ForeignKey('general.StudyYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, related_name="classes")
    letter = models.CharField(max_length=1, verbose_name=_("Литера класса"), null=True)
    dnevnik_id = models.CharField(max_length=255, verbose_name=_('ID системы Дневник.РУ'), null=True)
    students = models.ManyToManyField('general.user', verbose_name=_("Студенты"), related_name="classes")
    mentor = models.ForeignKey('general.user', verbose_name=_("Наставник"), related_name='mentor_classes', null=True, on_delete=models.SET_NULL)
    extra = models.ManyToManyField('general.user', verbose_name=_("Сотрудники класса"), through='general.ClassGroupRole', related_name="extra_classes")
    program_ib = models.CharField(verbose_name=_("IB-программа"), choices=ProgramIbChoices.choices, default=None, null=True, max_length=4)
    class Meta:
        verbose_name = 'Учебный класс'
        verbose_name_plural = 'Учебные классы'
        ordering = ['year_academic', 'year_study', 'letter']
    @property
    def count(self):
        return self.students.count
    @property
    def name(self):
        return f"{self.year_study.number}{self.letter}"
    def __str__(self):
        return f"{self.year_study}{self.letter} класс"
    
class ClassGroupRole(models.Model):
    """ Роли сотрудников класса """
    user = models.ForeignKey('general.user', verbose_name=_("Пользователь"), on_delete=models.CASCADE, null=True, related_name="group_roles")
    group = models.ForeignKey('general.ClassGroup', verbose_name=_("Группа"), on_delete=models.SET_NULL, null=True, related_name="user_roles")
    роль = models.CharField(max_length=255, verbose_name=_("Роль"), null=True)
    class Meta:
        verbose_name = 'Учебный класс: роль'
        verbose_name_plural = 'Учебные классы: роли'
        ordering = ['user', 'group', 'роль']
    def __str__(self):
        return f"{self.user}{self.роль}"
    
# Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))