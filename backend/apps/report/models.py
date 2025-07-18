from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

class LevelAchievementPrimaryChoices(models.TextChoices):
        level_a = "a", "Уровень A"
        level_b = "b", "Уровень B"
        level_c = "c", "Уровень C"
        NONE = None, "Не указан"

class LevelProfilePrimaryChoices(models.TextChoices):
        low = "low", "Слегка выражено"
        medium = "medium", "Выражено"
        high = "high", "Выражено в сильной степени"
        NONE = None, "Не указан"

class TypeReportChoices(models.TextChoices):
        teacher = "teacher", "Репорты учителя"
        mentor = "mentor", "Репорты наставника"
        extra = "extra", "Репорты службы сопровождения"

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

class ReportCriterion(models.Model):
    """ Критерии для репорта """
    name = models.CharField(max_length=128, verbose_name=_("Название критерия"), default=None, null=True)
    author = models.ForeignKey('general.User', verbose_name=_("Автор критерия"), on_delete=models.SET_NULL, null=True, related_name="report_criteria")
    years = models.ManyToManyField('general.StudyYear', verbose_name=_("Параллели"), related_name="report_criteria")
    subjects = models.ManyToManyField('curriculum.Subject', verbose_name=_("Предметы"), blank=True, related_name="report_criteria")
    type = ArrayField(
        models.CharField(max_length=7, choices=TypeReportChoices.choices),
        verbose_name=_("Тип репорта"), default=list, blank=True)
    class Meta:
        verbose_name = 'Критерий для репорта'
        verbose_name_plural = 'Критерии для репорта'
        ordering = ['name']
    def __str__(self):
        return f"{self.name}"
    
class ReportCriterionLevel(models.Model):
    """ Уровни критериев для репорта """
    criterion = models.ForeignKey('report.ReportCriterion', verbose_name=_("Критерий"), on_delete=models.CASCADE, null=True, related_name="levels")
    name = models.CharField(max_length=128, verbose_name=_("Название уровня"), default=None, null=True)
    description = models.TextField(verbose_name=_("Описание результата"), null=True, blank=True)
    point = models.PositiveSmallIntegerField(verbose_name=_("Баллы"), default=1)
    class Meta:
        verbose_name = 'Критерий для репорта: уровень'
        verbose_name_plural = 'Критерий для репорта: уровни'
        ordering = ['point', 'name']
    def __str__(self):
        return f"{self.name} ({self.point})"

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

class ReportTeacher(ReportBaseModel):
    """ Связанная модель репортов преподавателей с общими полями """
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.SET_NULL, null=True, related_name="reports")
    extra_subjects = models.ManyToManyField('curriculum.Subject', verbose_name=_("Дополнительные предметы"), blank=True, related_name="extra_reports")
    class Meta:
        ordering = ['period', 'subject', 'student', 'author']
        verbose_name = 'Репорт учителя'
        verbose_name_plural = 'Репорты учителя'

# TODO: Изменить имена базы (убрать Teacher)
class ReportCriterionAchievement(models.Model):
    criterion = models.ForeignKey('report.ReportCriterion', verbose_name=_("Чеклист"), on_delete=models.SET_NULL, null=True, related_name="reports")
    achievement = models.ForeignKey('report.ReportCriterionLevel', verbose_name=_("Достижение по критерию"), on_delete=models.SET_NULL, null=True, blank=True, related_name="reports")
    report = models.ForeignKey('report.ReportTeacher', verbose_name=_("Репорт учителя"), on_delete=models.CASCADE, null=True, related_name="criterion_achievements")
    report_mentor = models.ForeignKey('report.ReportMentor', verbose_name=_("Репорт наставника"), on_delete=models.CASCADE, null=True, related_name="criterion_achievements")
    report_extra = models.ForeignKey('report.ReportExtra', verbose_name=_("Репорт службы сопровождения"), on_delete=models.CASCADE, null=True, related_name="criterion_achievements")
    # Поля для Generic Relation
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    class Meta:
        verbose_name = 'Репорты: достижение по критерию'
        verbose_name_plural = 'Репорты: достижения по критериям'

class ReportTeacherPrimary(ReportTeacher):
    """ Репорты по предметам начальной школы """
    class Meta:
        verbose_name = 'Репорт учителя НШ'
        verbose_name_plural = 'Репорты учителя НШ'

class ReportPrimaryTopic(models.Model):
    """ Академические достижения в репорте начальной школы """
    report = models.ForeignKey('report.ReportTeacherPrimary', verbose_name=_("Репорт"), on_delete=models.CASCADE, null=True, related_name="topic_achievements")
    topic = models.ForeignKey('syllabus.CourseTopic', verbose_name=_("Тема"), on_delete=models.CASCADE, null=True, related_name="topic_achievements")
    topic_name = models.TextField(verbose_name=_("Тема (дополнительное текстовое поле)"), null=True, blank=True)
    level = models.CharField(verbose_name=_("Уровень"), choices=LevelAchievementPrimaryChoices.choices, null=True, default=None, max_length=4)
    comment = models.TextField(verbose_name=_("Комментарий"), null=True, blank=True)
    class Meta:
        verbose_name = 'Репорты учителя НШ: академические достижения'
        verbose_name_plural = 'Репорты учителя НШ: академические достижения'
        ordering = ['report', 'topic']
    def save(self, *args, **kwargs):
        if self.topic:
            self.topic_name = self.topic.name
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.topic}: {self.level}'

class ReportTeacherSecondary(ReportTeacher):
    """ Репорты по предметам средней школы """
    final_grade = models.SmallIntegerField(verbose_name=_("Итоговая оценка"), default=None, null=True, blank=True)
    class Meta:
        verbose_name = 'Репорт учителя СрШ'
        verbose_name_plural = 'Репорты учителя СрШ'

class ReportSecondaryLevel(models.Model):
    """ Выбор предметных целей и уровня из достижений в репорте средней школы"""
    report = models.ForeignKey('report.ReportTeacherSecondary', verbose_name=_("Репорт"), on_delete=models.CASCADE, null=True, related_name="objective_levels")
    strand = models.ForeignKey('myp.StrandLevel', verbose_name=_("Предметная цель"), on_delete=models.CASCADE, null=True, related_name="report_levels")
    level = models.ForeignKey('myp.StrandLevelAchievement', verbose_name=_("Уровень достижений"), on_delete=models.CASCADE, blank=True, null=True, related_name="report_levels")
    class Meta:
        verbose_name = 'Репорты учителя СрШ: уровнень достижений'
        verbose_name_plural = 'Репорты учителя СрШ: уровни достижений'
        ordering = ['strand']
    def __str__(self):
        return '{}: {}'.format(self.strand, self.level)

class ReportSecondaryCriterion(models.Model):
    """ Баллы по критериям в репорте средней школы """
    report = models.ForeignKey('report.ReportTeacherSecondary', verbose_name=_("Репорт"), on_delete=models.CASCADE, null=True, related_name="criterion_marks")
    criterion = models.ForeignKey('myp.MypObjective', verbose_name=_("Критерий"), on_delete=models.SET_NULL, null=True, related_name="criterion_marks")
    mark = models.SmallIntegerField(verbose_name=_("Балл"), default=None, null=True)
    class Meta:
        verbose_name = 'Репорты учителя СрШ: баллы по критериям'
        verbose_name_plural = 'Репорты учителя СрШ: баллы по критериям'
        ordering = ['report', 'criterion']
    def __str__(self):
        return f'{self.report}: {self.criterion}'

class ReportTeacherHigh(ReportTeacher):
    """ Репорты по предметам старшей школы """
    final_grade = models.SmallIntegerField(verbose_name=_("Итоговая оценка (2-5)"), default=None, null=True, blank=True)
    final_grade_ib = models.SmallIntegerField(verbose_name=_("Итоговая оценка (1-7)"), default=None, null=True, blank=True)
    class Meta:
        verbose_name = 'Репорт учителя СтШ'
        verbose_name_plural = 'Репорты учителя СтШ'

class ReportMentor(ReportBaseModel):
    """ Репорты наставника класса """
    class Meta:
        verbose_name = 'Репорт наставника'
        verbose_name_plural = 'Репорты наставника'

class ReportIbProfile(models.Model):
    """ Развитие профиля IB-студента """
    report = models.ForeignKey('report.ReportMentor', verbose_name=_("Репорт наставника"), on_delete=models.CASCADE, null=True, related_name="profiles")
    profile = models.ForeignKey('ibo.LearnerProfile', verbose_name=_("Профиль студента"), on_delete=models.CASCADE, null=True, related_name="reports")
    level = models.CharField(verbose_name=_("Уровень"), choices=LevelProfilePrimaryChoices.choices, default=None, null=True, blank=True, max_length=6)
    class Meta:
        verbose_name = 'Репорты наставника: профили студента IB'
        verbose_name_plural = 'Репорты наставника: профиль студента IB'
        ordering = ['report', 'profile']
    def __str__(self):
        return f'{self.profile}: {self.level}'

class ReportMentorPrimary(ReportMentor):
    """ Репорты наставника начальных класса """
    class Meta:
        verbose_name = 'Репорт наставника НШ'
        verbose_name_plural = 'Репорты наставника НШ'

class ReportPrimaryUnit(models.Model):
    """ Результаты исследования в PYP-юнитах """
    report = models.ForeignKey('report.ReportMentorPrimary', verbose_name=_("Репорт наставника НШ"), on_delete=models.CASCADE, null=True, related_name="pyp_units")
    unit = models.ForeignKey('pyp.PypUnitPlanner', verbose_name=_("Юнит"), on_delete=models.CASCADE, null=True, related_name="pyp_reports")
    comment = models.TextField(verbose_name=_("Комментарий"), null=True, blank=True)
    class Meta:
        verbose_name = 'Репорты наставника НШ: юнит PYP'
        verbose_name_plural = 'Репорты наставника НШ: юниты PYP'
        ordering = ['report', 'unit']
    def __str__(self):
        return f'{self.report}: {self.unit}'

class ReportExtra(ReportBaseModel):
    """ Репорты сотрудников службы сопрождения """
    role = models.CharField(verbose_name=_("Укажите свою роль"), max_length=255, default=None, null=True)
    class Meta:
        verbose_name = 'Репорт службы сопрождения'
        verbose_name_plural = 'Репорты службы сопровождения'