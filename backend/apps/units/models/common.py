from django.db import models
from django.utils.translation import gettext_lazy as _

class ObjectiveLetterChoices(models.TextChoices):
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

class QuestionTypeMypChoices(models.TextChoices):
        factual = "factual", "Фактический"
        conceptual = "conceptual", "Концептуальный"
        debatable = "debatable", "Дискуссионный"

class QuestionTypeDpChoices(models.TextChoices):
        factual = "factual", "Фактический"
        conceptual = "conceptual", "Концептуальный"
        skills_based = "skills-based", "Skills-based"
        content_based = "content-based", "Content-based"
        concept_based = "concept-based", "Concept-based"
        debatable = "debatable", "Дискуссионный"

class PostTypeChoices(models.TextChoices):
        prior = "prior", "Перед началом юнита"
        during = "during", "Во время юнита"
        after = "after", "После окончания юнита"

class AimDpChoices(models.TextChoices):
        group = "group", "Group"
        subject = "subject", "Subject"

class LevelDpChoices(models.TextChoices):
        standart = "SL", "Standart Level"
        high = "HL", "High Level"

class LanguageLearningChoices(models.TextChoices):
        activating_background = "Activating background knowledge", "Activating background knowledge"
        scaffolding_learning = "Scaffolding for new learning", "Scaffolding for new learning"
        through_practice = "Acquisition of new learning through practice", "Acquisition of new learning through practice"
        demonstrating_proficiency = "Demonstrating proficiency", "Demonstrating proficiency"

class TokConnectionsChoices(models.TextChoices):
        core_theme = "Core theme", "Core theme"
        optional_themes = "Optional themes", "Optional themes"
        areas_knowledge = "Areas of knowledge", "Areas of knowledge"
        key_concepts = "Key concepts", "Key concepts"

class CasConnectionsChoices(models.TextChoices):
        creativity = "Creativity", "Creativity"
        activity = "Activity", "Activity"
        service = "Service", "Service"

class LearningProcessChoices(models.TextChoices):
        lecture = "Lecture", "Lecture"
        socratic_seminar = "Socratic seminar", "Socratic seminar"
        small_group = "Small group/pair work", "Small group/pair work"
        powerpoint_lecture = "PowerPoint lecture/notes", "PowerPoint lecture/notes"
        individual_presentations = "Individual presentations", "Individual presentations"
        group_presentations = "Group presentations", "Group presentations"
        student_lecture = "Student lecture/leading", "Student lecture/leading"
        interdisciplinary_learning = "Interdisciplinary Learning", "Interdisciplinary Learning"

class DifferentiationChoices(models.TextChoices):
        affirm_identity = "Affirm identity – build self-esteem", "Affirm identity – build self-esteem"
        prior_knowledge = "Value prior knowledge", "Value prior knowledge"
        scaffold_learning = "Scaffold learning", "Scaffold learning"
        extend_learning = "Extend learning", "Extend learning"

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
