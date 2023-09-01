from django.db import models
from django.utils.translation import gettext_lazy as _
from general.models import (
    LevelNationChoices,
    ProgramIbChoices
)

class ProgramTypeChoices(models.TextChoices):
        BASE = "base", "Обязательная часть ФГОС"
        BASE_FGOS = "base_fgos", "Обязательная часть ФГОС в IB"
        BASE_IB = "base_ib", "Обязательная часть IB"
        EXTRA = "extra", "Внеурочная деятельность"
        NONE = None, 'Не выбрано'

class SubjectTypeChoices(models.TextChoices):
        AREA = "area", "Предметная область"
        DIRECTION = "direction", "Направление"
        NONE = None, 'Не выбрано'

class SubjectGroupFgos(models.Model):
    """ Предметная группа ФГОС """
    name = models.CharField(max_length=128, verbose_name=_("Название"))
    type = models.CharField(choices=SubjectTypeChoices.choices, max_length=9, default='area', verbose_name=_("Тип группы"))
    class Meta:
        verbose_name = 'Предметная группа ФГОС'
        verbose_name_plural = 'Предметные группы ФГОС'
        ordering = ['type', 'name']
    def __str__(self):
        return f"{self.name}"

class SubjectGroupIb(models.Model):
    """ Предметные группы IB """
    name = models.CharField(max_length=128, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=128, verbose_name=_("Название на рус. языке"), null=True)
    logo = models.ImageField(upload_to='subjectgroup_logos', verbose_name=_("Логотип"), null=True)
    program = models.CharField(choices=ProgramIbChoices.choices, null=True, default=None, max_length=4)
    class Meta:
        verbose_name = 'Предметная группа IB'
        verbose_name_plural = 'Предметные группы IB'
        ordering = ['program', 'name']
    def __str__(self):
        return "{} ({})".format(self.name, self.program)

class Subject(models.Model):
    """ Учебные дисциплины """
    name = models.CharField(max_length=128, verbose_name=_("Название"))
    name_eng = models.CharField(max_length=128, verbose_name=_("Название на англ. языке"), null=True)
    group_ib = models.ForeignKey('syllabus.SubjectGroupIb', verbose_name=_("Предметная группа в IB"), on_delete=models.SET_NULL, null=True, related_name="subject")
    group_fgos = models.ForeignKey('syllabus.SubjectGroupFgos', verbose_name=_("Предметная область в РФ"), on_delete=models.SET_NULL, null=True, related_name="subject")
    type = models.CharField(verbose_name=_("Тип предмета"), choices=ProgramTypeChoices.choices, max_length=10, default='base')
    dnevnik_id = models.CharField(verbose_name=_('ID системы Дневник.РУ'), max_length=40, null=True)
    department = models.ForeignKey('general.Department', verbose_name=_("Учебное подразделение"), on_delete=models.SET_NULL, null=True, related_name="subject")
    level = models.CharField(verbose_name=_("Уровень образования"), choices=LevelNationChoices.choices, default=None, max_length=4)
    need_report = models.BooleanField(verbose_name=_('Необходимость репорта'), default=False)
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['type', 'group_ib', 'name']
    def __str__(self):
        return "{} ({}, {})".format(self.name, self.get_level_display(), self.get_type_display())

class Syllabus(models.Model):
    """ Учебные планы """
    year = models.ForeignKey('general.AcademicYear', verbose_name=_("Учебный год"), on_delete=models.CASCADE, null=True, related_name="academic_plan")
    name = models.CharField(max_length=128, verbose_name=_("Название"), null=True, blank=True)
    name_short = models.CharField(max_length=128, verbose_name=_("Сокращённое название"), null=True, blank=True)
    level = models.CharField(verbose_name=_("Уровень образования"), choices=LevelNationChoices.choices, default=None, max_length=4)
    class Meta:
        verbose_name = 'Учебный план'
        verbose_name_plural = 'Учебные планы'
        ordering = ['year', 'name']
    def __str__(self):
        return f"{self.year} {self.name}"
    
class SyllabusSubjectHours(models.Model):
    """ Нагрузка учебных планов """
    academic_plan = models.ForeignKey('syllabus.Syllabus', verbose_name=_("Учебный план"), on_delete=models.CASCADE, null=True, related_name="syllabus_subject_hours")
    subject = models.ForeignKey('syllabus.Subject', verbose_name=_("Предмет"), on_delete=models.CASCADE, null=True, related_name="syllabus_subject_hours")
    years = models.ManyToManyField('general.StudyYear', verbose_name=_("Параллель"), related_name="syllabus_subject_hours")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=1)
    class Meta:
        verbose_name = 'Учебный план - нагрузка'
        verbose_name_plural = 'Учебные планы - нагрузка'
        ordering = ['subject__name', 'years__number']
    def __str__(self):
        return f"{self.academic_plan} ({self.subject} - {self.hours})"
    
class TeachingLoad(models.Model):
    """ Преподавательская нагрузка """
    year = models.ForeignKey('general.AcademicYear', verbose_name=_("Учебный год"), on_delete=models.CASCADE, null=True, related_name="teaching_load")
    teacher = models.ForeignKey('general.User', verbose_name=_("Учитель"), on_delete=models.CASCADE, null=True, blank=True, related_name="teaching_load")
    subject = models.ForeignKey('syllabus.Subject', verbose_name=_("Предмет"), on_delete=models.CASCADE, null=True, related_name="teaching_load")
    groups = models.ManyToManyField('general.ClassGroup', verbose_name=_("Классы"), blank=True, related_name="teaching_load")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Часы"), default=1)
    class Meta:
        verbose_name = 'Рабочая нагрузка учителя'
        verbose_name_plural = 'Рабочие нагрузки учителей'
        ordering = ['year', 'subject', 'groups__year_study', 'groups__year_study', 'teacher']
    def __str__(self):
        return '{} ({} - {} ч.)'.format(self.teacher, self.subject, self.hours)
