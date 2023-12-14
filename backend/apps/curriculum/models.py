from django.db import models
from django.utils.translation import gettext_lazy as _
from general.models import (
    LevelNationChoices,
    ProgramIbChoices
)

class ProgramTypeChoices(models.TextChoices):
        BASE = "base", "Обязательная часть"
        BASE_FGOS = "base_fgos", "Обязательная часть ФГОС в IB"
        BASE_IB = "base_ib", "Обязательная часть IB"
        EXTRA = "extra", "Внеурочная деятельность"
        NONE = None, 'Не выбрано'

class SubjectTypeChoices(models.TextChoices):
        AREA = "area", "Предметная область"
        DIRECTION = "direction", "Направление"
        NONE = None, 'Не выбрано'

class FgosSubjectGroup(models.Model):
    """ Предметная группа ФГОС """
    name = models.CharField(max_length=128, verbose_name=_("Название"))
    type = models.CharField(choices=SubjectTypeChoices.choices, max_length=9, default='area', verbose_name=_("Тип группы"))
    level = models.CharField(verbose_name=_("Уровень образования"), choices=LevelNationChoices.choices, default=None, max_length=4)
    class Meta:
        verbose_name = 'Предметная группа ФГОС'
        verbose_name_plural = 'Предметные группы ФГОС'
        ordering = ['level', 'id']
    def __str__(self):
        return f"{self.name}"

class IbSubjectGroup(models.Model):
    """ Предметные группы IB """
    name = models.CharField(max_length=128, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=128, verbose_name=_("Название на рус. языке"), null=True)
    logo = models.ImageField(upload_to='subjectgroup_logos', verbose_name=_("Логотип"), null=True)
    program = models.CharField(verbose_name=_("Программа IB"), choices=ProgramIbChoices.choices, null=True, default=None, max_length=4)
    class Meta:
        verbose_name = 'Предметная группа IB'
        verbose_name_plural = 'Предметные группы IB'
        ordering = ['program', 'name']
    def __str__(self):
        return f"{self.name} ({self.program.upper()})"

class IbDiscipline(models.Model):
    """ Специальные дисцилины """
    name = models.CharField(max_length=128, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=128, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    group = models.ForeignKey('curriculum.IbSubjectGroup', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL, null=True, related_name="specific_disciplines")
    class Meta:
        verbose_name = 'Специальная IB-дисциплина'
        verbose_name_plural = 'Специальные IB-дисциплины'
        ordering = ['group', 'name']
    def __str__(self):
        return f"{self.name}"

class Subject(models.Model):
    """ Учебные дисциплины """
    name = models.CharField(max_length=128, verbose_name=_("Название"))
    name_eng = models.CharField(max_length=128, verbose_name=_("Название на англ. языке"), null=True, blank=True)
    group_ib = models.ForeignKey('curriculum.IbSubjectGroup', verbose_name=_("Предметная группа в IB"), on_delete=models.SET_NULL, blank=True , null=True, related_name="subjects")
    group_fgos = models.ForeignKey('curriculum.FgosSubjectGroup', verbose_name=_("Предметная область в РФ"), on_delete=models.SET_NULL, blank=True, null=True, related_name="subjects")
    discipline_ib = models.ForeignKey('curriculum.IbDiscipline', verbose_name=_("Дисциплина в IB"), on_delete=models.SET_NULL, blank=True, null=True, related_name="subjects")
    dnevnik_id = models.CharField(verbose_name=_('ID системы Дневник.РУ'), max_length=40, null=True, blank=True)
    department = models.ForeignKey('general.Department', verbose_name=_("Учебное подразделение"), on_delete=models.SET_NULL, null=True, related_name="subjects")
    level = models.CharField(verbose_name=_("Уровень образования"), choices=LevelNationChoices.choices, default=None, max_length=4)
    need_report = models.BooleanField(verbose_name=_('Необходимость репорта'), default=False)
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['level', 'name']
    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

class Curriculum(models.Model):
    """ Учебные планы """
    year = models.ForeignKey('general.AcademicYear', verbose_name=_("Учебный год"), on_delete=models.CASCADE, null=True, related_name="curricula")
    name = models.CharField(max_length=128, verbose_name=_("Название"), null=True, blank=True)
    name_short = models.CharField(max_length=32, verbose_name=_("Сокращённое название"), null=True, blank=True)
    level = models.CharField(verbose_name=_("Уровень образования"), choices=LevelNationChoices.choices, default=None, max_length=4)
    ib = models.BooleanField(verbose_name=_('Наличие компонента IB'), default=False)
    class Meta:
        verbose_name = 'Учебный план'
        verbose_name_plural = 'Учебные планы'
        ordering = ['-year', 'name']
    def __str__(self):
        return f"{self.year.number}-{self.year.number + 1}: {self.name_short}"
    
class CurriculumLoad(models.Model):
    """ Нагрузка учебных планов """
    curriculum = models.ForeignKey('curriculum.Curriculum', verbose_name=_("Учебный план"), on_delete=models.CASCADE, null=True, related_name="curriculum_loads")
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.CASCADE, null=True, related_name="curriculum_loads")
    type = models.CharField(verbose_name=_("Тип предмета"), choices=ProgramTypeChoices.choices, max_length=10, default='base')
    years = models.ManyToManyField('general.StudyYear', verbose_name=_("Параллель"), blank=True, related_name="curriculum_loads")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=1)
    class Meta:
        verbose_name = 'Учебный план - нагрузка'
        verbose_name_plural = 'Учебные планы - нагрузка'
        ordering = ['subject__name']
    def __str__(self):
        return f"{self.curriculum}: {self.subject.name} - {self.hours} ч."
    
class TeachingLoad(models.Model):
    """ Преподавательская нагрузка """
    year = models.ForeignKey('general.AcademicYear', verbose_name=_("Учебный год"), on_delete=models.CASCADE, null=True, related_name="teaching_loads")
    teacher = models.ForeignKey('general.User', verbose_name=_("Учитель"), on_delete=models.CASCADE, null=True, related_name="teaching_loads")
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.CASCADE, null=True, related_name="teaching_loads")
    groups = models.ManyToManyField('general.ClassGroup', verbose_name=_("Классы"), blank=True, related_name="teaching_loads")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Часы"), default=1)
    class Meta:
        verbose_name = 'Рабочая нагрузка учителя'
        verbose_name_plural = 'Рабочие нагрузки учителей '
        ordering = ['year', 'subject', 'teacher']
    def __str__(self):
        groups = ", ".join([f"{cl.name}" for cl in self.groups.all()])
        return f"{self.year}: {self.teacher} {self.subject.name} ({groups} классы) - {self.hours} ч."
