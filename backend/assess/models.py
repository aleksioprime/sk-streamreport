from django.db import models
from django.utils.translation import ugettext_lazy as _

class StudyYear(models.Model):
    """ Учебные года """
    name = models.CharField(max_length=32, verbose_name=_("Учебный год"))
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    class Meta:
        verbose_name = 'Учебный год'
        verbose_name_plural = 'Учебные года'
        ordering = ['date_start']
    def __str__(self):
        return "{}".format(self.name)

class ClassGroup(models.Model):
    """ Учебные классы """
    study_year = models.ForeignKey('assess.StudyYear', verbose_name=_("Учебный год"), on_delete=models.CASCADE, 
                                   null=True, blank=True, related_name="classgroup")
    class_year = models.PositiveSmallIntegerField(verbose_name=_("Год обучения"), default=1)
    letter = models.CharField(max_length=1, verbose_name=_("Литера класса"), null=True, blank=True)
    id_dnevnik = models.CharField(max_length=255, verbose_name=_('ID системы Дневник.РУ'), blank=True, null=True)
    class Meta:
        verbose_name = 'Учебный класс'
        verbose_name_plural = 'Учебные классы'
        ordering = ['class_year', 'letter']
    def __str__(self):
        return "{}{} класс".format(self.class_year, self.letter)

class StudyPeriod(models.Model):
    """ Учебные периоды в году """
    PERIOD_TYPE = [
        ('trimester', 'триместр'),
        ('halfyear', 'полугодие'),
    ]
    study_year = models.ForeignKey('assess.StudyYear', verbose_name=_("Учебный год"), on_delete=models.SET_NULL, \
        null=True, blank=True, related_name="period")
    number = models.PositiveSmallIntegerField(verbose_name=_("Номер периода"), default=1)
    type = models.CharField(max_length=16, choices=PERIOD_TYPE, verbose_name=_("Тип периода"))
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    id_dnevnik = models.CharField(max_length=255, verbose_name=_('ID системы Дневник.РУ'), blank=True, null=True)
    @property
    def days(self):
        days = abs((self.date_end - self.date_start).days)
        return "{} дней".format(days)
    class Meta:
        verbose_name = 'Учебный период'
        verbose_name_plural = 'Учебные периоды'
        ordering = ['study_year', 'type', 'number']
    def __str__(self):
        return "{} | {} {}".format(self.study_year, self.number, self.get_type_display())

class SummativeWork(models.Model):
    """ Работы итогового оценивания """
    title = models.CharField(max_length=255, verbose_name=_("Название итоговой работы"))
    unit = models.ForeignKey('curriculum.UnitPlannerMYP', verbose_name=_("Юнит"), on_delete=models.SET_NULL,
                                null=True, related_name="sumwork")
    period = models.ForeignKey('assess.StudyPeriod', verbose_name=_("Период обучения"), on_delete=models.SET_NULL,
                               null=True, related_name="sumwork")
    date = models.DateField(verbose_name=_("Дата проведения"))
    lesson = models.PositiveSmallIntegerField(verbose_name=_("Номер урока"), default=1)
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Учебный предмет"), on_delete=models.SET_NULL,
                                null=True, blank=False, related_name="sumwork")
    teacher = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Учитель"), on_delete=models.SET_NULL,
                                null=True, related_name="sumwork")
    class_groups = models.ManyToManyField('assess.ClassGroup', verbose_name=_("Классы"),
                                          blank=True, related_name="sumwork")
    criteria = models.ManyToManyField('curriculum.Criterion', verbose_name=_("Критерии оценки"),
                                      blank=True, related_name="sumwork")
    class Meta:
        verbose_name = 'Итоговая работ'
        verbose_name_plural = 'Итоговые работы'
        ordering = ['period', 'subject', 'title']
    def __str__(self):
        return '{}: {}'.format(self.subject, self.title)
    
class WorkAssessment(models.Model):
    """ Журналы оценок по итоговым работам """
    work = models.ForeignKey('assess.SummativeWork', verbose_name=_("Юнит"), on_delete=models.CASCADE, null=True, related_name="workassess")
    student = models.ForeignKey('member.ProfileStudent', verbose_name=_("Студент"), on_delete=models.SET_NULL, null=True, related_name="workassess")
    criteria_marks = models.ManyToManyField('curriculum.Criterion', through='assess.WorkCriteriaMark', blank=True, related_name="workassess")
    class Meta:
        verbose_name = 'Оценка в итоговой работы'
        verbose_name_plural = 'Оценки в итоговых работых'
        ordering = ['work', 'student']
    def __str__(self):
        return '{} - {}'.format(self.work, self.student)

class WorkCriteriaMark(models.Model):
    """ Выбор критериев в журнале итоговых работ для выставление баллов студенту"""
    work_assessment = models.ForeignKey('assess.WorkAssessment', verbose_name=_("Позиция оценки в юните"), on_delete=models.CASCADE,
                                null=True, related_name="unit_assess_selected")
    criterion = models.ForeignKey('curriculum.Criterion', verbose_name=_("Критерий оценки"), on_delete=models.SET_NULL,
                             null=True, related_name="unit_criterion_selected")
    mark = models.SmallIntegerField(verbose_name=_("Оценка по критерию"), default=0)
    class Meta:
        verbose_name = 'Выбор критериев и оценка'
        verbose_name_plural = 'Выборы критериев и оценка'
        ordering = ['work_assessment', 'criterion']
    def __str__(self):
        return '{}: {} ({})'.format(self.work_assessment, self.criterion, self.mark)