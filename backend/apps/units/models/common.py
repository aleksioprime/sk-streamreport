from django.db import models
from django.utils.translation import gettext_lazy as _

class CriterionChoices(models.TextChoices):
        A = "a", "Критерий A"
        B = "b", "Критерий B"
        C = "c", "Критерий C"
        D = "d", "Критерий D"

class StrandLetterChoices(models.TextChoices):
        one = 1, "i"
        two = 2, "ii"
        three = 3, "iii"
        four = 4, "iv"
        five = 5, "v"

class QuestionTypeChoices(models.TextChoices):
        factual = "factual", "Фактический"
        conceptual = "conceptual", "Концептуальный"
        debatable = "debatable", "Дискуссионный"

class PostTypeChoices(models.TextChoices):
        prior = "prior", "Перед началом юнита"
        during = "during", "Во время юнита"
        after = "after", "После окончания юнита"

class LearnerProfile(models.Model):
    """ Профили студента IB """
    name = models.CharField(max_length=64,verbose_name=_("Название"))
    name_rus = models.CharField(max_length=64,verbose_name=_("Название на рус. языке"), null=True)
    description = models.TextField(verbose_name=_("Описание"), null=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True)
    class Meta:
        verbose_name = 'IB: Профиль студента'
        verbose_name_plural = 'IB: Профили студента'
        ordering = ['name']
    def __str__(self):
        return "{}".format(self.name)
    
class AtlCategory(models.Model):
    """ Категории ATL """
    name = models.CharField(max_length=64, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'IB: ATL категория'
        verbose_name_plural = 'IB: ATL категории'
        ordering = ['id']
    def __str__(self):
        return "{}".format(self.name)

class AtlCluster(models.Model):
    """ Кластеры ATL """
    name = models.CharField(max_length=64, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    category = models.ForeignKey('units.AtlCategory', verbose_name=_("Категория ATL"), on_delete=models.CASCADE, related_name="clusters")
    class Meta:
        verbose_name = 'IB: ATL кластер'
        verbose_name_plural = 'IB: ATL кластеры'
        ordering = ['category', 'id']
    def __str__(self):
        return "{} ({})".format(self.name, self.category)
