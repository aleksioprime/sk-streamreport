from django.db import models
from django.utils.translation import gettext_lazy as _

class CriterionChoices(models.TextChoices):
        A = "a", "Критерий A"
        B = "b", "Критерий B"
        C = "c", "Критерий C"
        D = "d", "Критерий D"

class Criterion(models.Model):
    """ Критерии оценивания """
    letter = models.CharField(verbose_name=_("Символ"), choices=CriterionChoices.choices, max_length=1)
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    group = models.ForeignKey('syllabus.SubjectGroupIb', verbose_name=_("Предметная группа IB"), on_delete=models.SET_NULL, null=True, related_name="criterion")
    class Meta:
        verbose_name = 'Критерий оценивания'
        verbose_name_plural = 'Критерии оценивания'
        ordering = ['group', 'letter']
    def __str__(self):
        return "{} | {}".format(self.letter, self.group)

class Strand(models.Model):
    """ Стрэнды - аспекты образовательных достижений """
    STRAND_LETTER = [
        (1, 'i'),
        (2, 'ii'),
        (3, 'iii'),
        (4, 'iv'),
        (5, 'v'),
    ]
    number = models.PositiveIntegerField(verbose_name=_("Абсолютный номер"), default=1)
    letter = models.PositiveIntegerField(verbose_name=_("Метка в критерии"), choices=STRAND_LETTER, default=1)
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    criterion = models.ForeignKey('units.Criterion', verbose_name=_("Критерий"), on_delete=models.SET_NULL, null=True, related_name="strand")
    class Meta:
        verbose_name = 'Стрэнд'
        verbose_name_plural = 'Стрэнды'
        ordering = ['criterion', 'number', 'letter']
    def __str__(self):
        return "{} ({}). {}... | {}".format(self.number, self.get_letter_display(), self.name[:15], self.criterion)
    
class EducationalLevel(models.Model):
    """ Образовательный уровень """
    number = models.PositiveIntegerField(verbose_name=_("Номер"), default=1)
    name = models.CharField(max_length=255, verbose_name=_("Название"), null=True)
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True)
    years = models.ManyToManyField('general.StudyYear', verbose_name=_("Года обучения"), related_name="levels")
    class Meta:
        verbose_name = 'Образовательный уровень'
        verbose_name_plural = 'Образовательные уровни'
        ordering = ['name']
    def __str__(self):
        return "{}".format(self.name)
    
class Objective(models.Model):
    """ Образовательные цели """
    name = models.CharField(max_length=255,verbose_name=_("Описание"), null=True)
    name_rus = models.CharField(max_length=255,verbose_name=_("Описание на рус. языке"), null=True)
    level = models.ForeignKey('units.EducationalLevel', verbose_name=_("Уровень в IB"), on_delete=models.SET_NULL, null=True, related_name="objective")
    strand = models.ForeignKey('units.Strand', verbose_name=_("Стрэнд"), on_delete=models.SET_NULL, null=True, related_name="objective")
    class Meta:
        verbose_name = 'Образовательная цель'
        verbose_name_plural = 'Образовательные цели'
        ordering = ['level', 'strand']
    def __str__(self):
        return "{} | {}. {}...".format(self.level, self.strand.letter, self.name[:10])