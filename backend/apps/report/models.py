from django.db import models
from django.utils.translation import gettext_lazy as _

class LevelAchievementPrimaryChoices(models.TextChoices):
        level_a = "A", "Уровень A"
        level_b = "B", "Уровень B"
        level_c = "C", "Уровень C"
        NONE = None, "Не указан"

class LevelProfilePrimaryChoices(models.TextChoices):
        low = "low", "Слегка выражено"
        medium = "medium", "Выражено"
        high = "high", "Выражено в сильной степени"
        NONE = None, "Не указан"

class ReportPeriod(models.Model):
    """ Периоды для заполнения репортов """
    order = models.PositiveSmallIntegerField(verbose_name=_("Номер периода"), default=1)
    name = models.CharField(max_length=128, verbose_name=_("Название периода"), default=None, null=True)
    year = models.ForeignKey('general.AcademicYear', verbose_name=_("Учебный год"), on_delete=models.CASCADE, null=True, related_name="report_period")
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    @property
    def days(self):
        days = abs((self.date_end - self.date_start).days)
        return f"{days} дней"
    class Meta:
        verbose_name = 'Период репортов'
        verbose_name_plural = 'Периоды репортов'
        ordering = ['year', 'order']
    def __str__(self):
        return f"{self.order} период ({self.year})"

class ReportBaseModel(models.Model):
    """ Абстрактная модель репортов с общими полями """
    student = models.ForeignKey('general.User', verbose_name=_("Студент"), on_delete=models.CASCADE, related_name="%(class)s_student_reports")
    author = models.ForeignKey('general.User', verbose_name=_("Автор репорта"), on_delete=models.SET_NULL, null=True, related_name="%(class)s_author_reports")
    period = models.ForeignKey('report.ReportPeriod', verbose_name=_("Период репорта"), on_delete=models.SET_NULL, null=True, related_name="%(class)s_reports")
    group = models.ForeignKey('general.ClassGroup', verbose_name=_("Класс"), on_delete=models.SET_NULL, null=True, related_name="%(class)s_reports")
    comment = models.TextField(verbose_name=_("Текст репорта"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Создан"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Изменён"))
    class Meta:
        abstract = True
        ordering = ['period', 'student', 'author']
    def __str__(self):
        return f'{self.period}: {self.student} ({self.period})'

class ReportTeacherBaseModel(ReportBaseModel):
    """ Абстрактная модель репортов преподавателей с общими полями """
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.SET_NULL, null=True, related_name="%(class)s_reports")
    class Meta:
        abstract = True
        ordering = ['period', 'subject', 'student', 'author']

class ReportTeacherPrimary(ReportTeacherBaseModel):
    """ Репорты по предметам начальной школы """
    # units = models.ManyToManyField('pyp.PypUnitPlanner', verbose_name=_("Юниты "), through='report.ReportPrimaryUnit', blank=True, related_name="reports")
    class Meta:
        verbose_name = 'Репорт начальной школы'
        verbose_name_plural = 'Репорты начальной школы'

class ReportPrimaryUnit(models.Model):
    """ Развитие профиля IB-студента """
    report = models.ForeignKey('report.ReportTeacherPrimary', verbose_name=_("Репорт"), on_delete=models.CASCADE, null=True, related_name="units")
    unit = models.ForeignKey('pyp.PypUnitPlanner', verbose_name=_("Юнит"), on_delete=models.CASCADE, null=True, related_name="reports")
    comment = models.TextField(verbose_name=_("Комментарий"), null=True, blank=True)
    class Meta:
        verbose_name = 'Репорты начальной школы: юнит'
        verbose_name_plural = 'Репорты начальной школы: юниты'
        ordering = ['report', 'unit']
    def __str__(self):
        return f'{self.report}: {self.unit}'

class ReportPrimaryIbProfile(models.Model):
    """ Развитие профиля IB-студента """
    report = models.ForeignKey('report.ReportTeacherPrimary', verbose_name=_("Репорт"), on_delete=models.CASCADE, null=True, related_name="profiles")
    profile = models.ForeignKey('ibo.LearnerProfile', verbose_name=_("Профиль студента"), on_delete=models.CASCADE, null=True, related_name="reports")
    level = models.CharField(verbose_name=_("Уровень"), choices=LevelProfilePrimaryChoices.choices, default=None, max_length=6)
    class Meta:
        verbose_name = 'Репорты начальной школы: профили студента IB'
        verbose_name_plural = 'Репорты начальной школы: профиль студента IB'
        ordering = ['report', 'profile']
    def __str__(self):
        return f'{self.profile}: {self.level}'

class ReportPrimaryAchievement(models.Model):
    """ Академические достижения в репорте начальной школы """
    report = models.ForeignKey('report.ReportTeacherPrimary', verbose_name=_("Репорт"), on_delete=models.CASCADE, null=True, related_name="achievements")
    topic = models.ForeignKey('syllabus.CourseTopic', verbose_name=_("Тема"), on_delete=models.CASCADE, null=True, related_name="achievements")
    level = models.CharField(verbose_name=_("Уровень"), choices=LevelAchievementPrimaryChoices.choices, default=None, max_length=4)
    comment = models.TextField(verbose_name=_("Комментарий"), null=True, blank=True)
    class Meta:
        verbose_name = 'Репорты начальной школы: академические достижения'
        verbose_name_plural = 'Репорты начальной школы: академические достижения'
        ordering = ['report', 'topic']
    def __str__(self):
        return f'{self.topic}: {self.level}'

class ReportTeacherSecondary(ReportTeacherBaseModel):
    """ Репорты по предметам средней школы """
    criteria = models.ManyToManyField('myp.MypObjective', verbose_name=_("Критерии "), through='report.ReportSecondaryCriteria', blank=True, related_name="reports")
    achievements = models.ManyToManyField('myp.AchievementLevel', verbose_name=_("Уровни достижений"), blank=True, related_name="reports")
    final_grade = models.SmallIntegerField(verbose_name=_("Итоговая оценка"), default=None, null=True, blank=True)
    class Meta:
        verbose_name = 'Репорт средней школы'
        verbose_name_plural = 'Репорты средней школы'

class ReportSecondaryCriteria(models.Model):
    """ Баллы по критериям в репорте средней школы """
    report = models.ForeignKey('report.ReportTeacherSecondary', verbose_name=_("Репорт"), on_delete=models.CASCADE, null=True, related_name="mark_criteria")
    criterion = models.ForeignKey('myp.MypObjective', verbose_name=_("Критерий"), on_delete=models.SET_NULL, null=True, related_name="mark_reports")
    mark = models.SmallIntegerField(verbose_name=_("Балл"), default=None, null=True)
    class Meta:
        verbose_name = 'Репорты средней школы: баллы по критериям'
        verbose_name_plural = 'Репорты средней школы: баллы по критериям'
        ordering = ['report', 'criterion']
    def __str__(self):
        return f'{self.report}: {self.criterion}'

class ReportTeacherHigh(ReportTeacherBaseModel):
    """ Репорты по предметам старшей школы """
    final_grade = models.SmallIntegerField(verbose_name=_("Итоговая оценка (2-5)"), default=None, null=True, blank=True)
    final_grade_ib = models.SmallIntegerField(verbose_name=_("Итоговая оценка (1-7)"), default=None, null=True, blank=True)
    class Meta:
        verbose_name = 'Репорт старшей школы'
        verbose_name_plural = 'Репорты старшей школы'

class ReportMentor(ReportBaseModel):
    """ Репорты наставника класса """
    class Meta:
        verbose_name = 'Репорт наставника'
        verbose_name_plural = 'Репорты наставника'

class ReportExtra(ReportBaseModel):
    """ Репорты сотрудников службы сопрождения """
    role = models.CharField(verbose_name=_("Укажите свою роль"), max_length=255, default=None, null=True)
    class Meta:
        verbose_name = 'Репорт службы сопрождения'
        verbose_name_plural = 'Репорты службы сопровождения'