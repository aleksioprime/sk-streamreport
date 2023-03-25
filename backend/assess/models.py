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
    class_year = models.ManyToManyField('curriculum.ClassYear', verbose_name=_("Год обучения"), blank=True, related_name="period")
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
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Учебный предмет"), on_delete=models.SET_NULL,
                                null=True, blank=False, related_name="sumwork")
    teacher = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Учитель"), on_delete=models.SET_NULL,
                                null=True, related_name="sumwork")
    groups = models.ManyToManyField('assess.ClassGroup', verbose_name=_("Классы"), through='assess.WorkGroupDate',
                                          blank=True, related_name="sumwork")
    criteria = models.ManyToManyField('curriculum.Criterion', verbose_name=_("Критерии оценки"),
                                      blank=True, related_name="sumwork")
    class Meta:
        verbose_name = 'Итоговая работ'
        verbose_name_plural = 'Итоговые работы'
        ordering = ['period', 'subject', 'title']
    def __str__(self):
        return '{}: {}'.format(self.subject, self.title)
    
class WorkGroupDate(models.Model):
    """ Даты итоговых работ """
    work = models.ForeignKey('assess.SummativeWork', verbose_name=_("Юнит"), on_delete=models.CASCADE, null=True, related_name="workgroup")
    group = models.ForeignKey('assess.ClassGroup', verbose_name=_("Класс"), on_delete=models.CASCADE, blank=True, related_name="workgroup")
    date = models.DateField(verbose_name=_("Дата проведения"))
    lesson = models.PositiveSmallIntegerField(verbose_name=_("Номер урока"), default=1)
    class Meta:
        verbose_name = 'Дата итоговой работы'
        verbose_name_plural = 'Даты итоговых работ'
        ordering = ['work', 'group', 'date']
    def __str__(self):
        return '{}: {}'.format(self.work, self.group)
    
class WorkAssessment(models.Model):
    """ Журналы оценок по итоговым работам """
    work = models.ForeignKey('assess.SummativeWork', verbose_name=_("Итоговая работа"), on_delete=models.CASCADE, null=True, related_name="workassess")
    student = models.ForeignKey('member.ProfileStudent', verbose_name=_("Студент"), on_delete=models.SET_NULL, null=True, related_name="workassess")
    criteria_marks = models.ManyToManyField('curriculum.Criterion', through='assess.WorkCriteriaMark', blank=True, related_name="workassess")
    grade = models.SmallIntegerField(verbose_name=_("Оценка"), default=0)
    class Meta:
        verbose_name = 'Оценка в итоговой работы'
        verbose_name_plural = 'Оценки в итоговых работых'
        ordering = ['work', 'student']
    def __str__(self):
        return '{} - {}'.format(self.work, self.student)

class WorkCriteriaMark(models.Model):
    """ Выбор критериев в журнале итоговых работ для выставление баллов студенту"""
    work_assess = models.ForeignKey('assess.WorkAssessment', verbose_name=_("Позиция оценки в юните"), on_delete=models.CASCADE,
                                null=True, related_name="work_criteria_mark")
    criterion = models.ForeignKey('curriculum.Criterion', verbose_name=_("Критерий оценки"), on_delete=models.SET_NULL,
                             null=True, related_name="work_criteria_mark")
    mark = models.SmallIntegerField(verbose_name=_("Оценка по критерию"), default=0)
    class Meta:
        verbose_name = 'Выбор критериев и оценка'
        verbose_name_plural = 'Выборы критериев и оценка'
        ordering = ['work_assess', 'criterion']
    def __str__(self):
        return '{}: {} ({})'.format(self.work_assess, self.criterion, self.mark)
    
class PeriodAssessment(models.Model):
    """ Журналы оценок за учебный период """
    student = models.ForeignKey('member.ProfileStudent', verbose_name=_("Студент"), on_delete=models.SET_NULL, null=True, related_name="periodassess")
    period = models.ForeignKey('assess.StudyPeriod', verbose_name=_("Период"), on_delete=models.SET_NULL, null=True, related_name="periodassess")
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.SET_NULL, null=True, related_name="periodassess")
    class_year = models.ForeignKey('curriculum.ClassYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, related_name="periodassess")
    criteria_marks = models.ManyToManyField('curriculum.Criterion', through='assess.PeriodCriteriaMark', blank=True, related_name="periodassess")
    form_grade = models.DecimalField(verbose_name=_("Средняя оценка за текущие работы"), max_digits=3, decimal_places=2)
    final_grade = models.SmallIntegerField(verbose_name=_("Итоговая оценка"), default=0)
    class Meta:
        verbose_name = 'Журнал оценок за уч. период'
        verbose_name_plural = 'Журналы оценок за уч. период'
        ordering = ['period', 'student']
    def __str__(self):
        return '{} - {}'.format(self.period, self.student)
    
class PeriodCriteriaMark(models.Model):
    """ Выставление оценок по критериям в журнале учебных периодов """
    period_assess = models.ForeignKey('assess.PeriodAssessment', verbose_name=_("Позиция оценки в уч. периоде"), on_delete=models.SET_NULL,
                                null=True, related_name="period_criteria_mark")
    criterion = models.ForeignKey('curriculum.Criterion', verbose_name=_("Критерий оценки"), on_delete=models.SET_NULL,
                             null=True, related_name="period_criteria_mark")
    mark = models.SmallIntegerField(verbose_name=_("Оценка по критерию"), default=0)
    class Meta:
        verbose_name = 'Оценка по выбранным критериям в периоде'
        verbose_name_plural = 'Оценки по выбранным критериям в период'
        ordering = ['period_assess', 'criterion']
    def __str__(self):
        return '{}: {} ({})'.format(self.period_assess, self.criterion, self.mark)