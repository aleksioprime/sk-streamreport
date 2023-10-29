from django.db import models
from django.utils.translation import gettext_lazy as _

class TransdisciplinaryTheme(models.Model):
    """ Трансдисциплинарные темы """
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True)
    description = models.TextField(verbose_name=_("Описание"), null=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True)
    class Meta:
        verbose_name = 'PYP: Трансдисциплинарная тема'
        verbose_name_plural = 'PYP: Трансдисциплинарные темы'
        ordering = ['name']
    def __str__(self):
        return f"{self.name}"
    
class PypKeyConcept(models.Model):
    """ Ключевые концепты PYP """
    name = models.CharField(max_length=32, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=32, verbose_name=_("Название на рус. языке"), null=True)
    description = models.TextField(verbose_name=_("Описание"), null=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True)
    class Meta:
        verbose_name = 'MYP: Ключевой концепт'
        verbose_name_plural = 'MYP: Ключевые концепты'
        ordering = ['name']
    def __str__(self):
        return "{}".format(self.name)

class PypAtlGroup(models.Model):
    """ Группы ATL в PYP """
    name = models.CharField(max_length=64, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    cluster = models.ForeignKey('units.AtlCluster', verbose_name=_("Кластер ATL"), on_delete=models.CASCADE, null=False, related_name="pyp_groups")
    class Meta:
        verbose_name = 'PYP: ATL группа'
        verbose_name_plural = 'PYP: ATL группы'
        ordering = ['cluster', 'name']
    def __str__(self):
        return f"{self.name} ({self.cluster})"

class PypAtlSkill(models.Model):
    """ Навыки ATL в PYP """
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True)
    group = models.ForeignKey('units.PypAtlGroup', verbose_name=_("Группа ATL"), on_delete=models.CASCADE, null=False, related_name="pyp_skills")
    class Meta:
        verbose_name = 'PYP: ATL навык'
        verbose_name_plural = 'PYP: ATL навыки'
        ordering = ['group', 'name']
    def __str__(self):
        return f"{self.name} ({self.group})"

# TODO: Подумать над добавлением фотоальбома в юнит (загрузка и хранение нескольких фотографий в одном поле через связанную таблицу)
# TODO: Подумать над добавлением набора файлов в юнит (загрузка и хранение нескольких файлов в одном поле через связанную таблицу)
class PypUnitPlanner(models.Model):
    """ ЮнитПланеры PYP """
    title = models.CharField(max_length=255, verbose_name=_("Название юнита"))
    order = models.PositiveSmallIntegerField(verbose_name=_("Номер"), default=0)
    teachers = models.ManyToManyField('general.User', verbose_name=_("Учителя"), related_name="pyp_unitplans")
    year = models.ForeignKey('general.StudyYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, related_name="pyp_unitplans")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=0)
    transdisciplinary_theme = models.ForeignKey('units.TransdisciplinaryTheme', verbose_name=_("Трансдисциплинарная тема"), on_delete=models.SET_NULL, null=True, related_name="pyp_unitplans")
    central_idea = models.TextField(verbose_name=_("Центральная идея"), null=True, blank=True)
    key_concepts = models.ManyToManyField('units.PypKeyConcept', verbose_name=_("Ключевые концепты"), blank=True, related_name="pyp_unitplans")
    action = models.TextField(verbose_name=_("Действия"), null=True, blank=True)
    reflections_initial = models.TextField(verbose_name=_("Начальная рефлексия"), null=True, blank=True)
    prior_learning = models.TextField(verbose_name=_("Предшествующий опыт"), null=True, blank=True)
    conncetions = models.TextField(verbose_name=_("Трансдисциплинарные и прошлые связи"), null=True, blank=True)
    learning_goals = models.TextField(verbose_name=_("Цели обучения и критерии успеха"), null=True, blank=True)
    questions_teacher = models.TextField(verbose_name=_("Вопросы учителя"), null=True, blank=True)
    questions_student = models.TextField(verbose_name=_("Вопросы студента"), null=True, blank=True)
    engaging_learning = models.TextField(verbose_name=_("Создание вовлечённого обучения"), null=True, blank=True)
    supporting_agency = models.TextField(verbose_name=_("Поддержание свободного волеизъявления студентов"), null=True, blank=True)
    questions_all = models.TextField(verbose_name=_("Вопросы учителя и студента"), null=True, blank=True)
    ongoing_assessment = models.TextField(verbose_name=_("Текущее оценивание"), null=True, blank=True)
    resources = models.TextField(verbose_name=_("Использование ресурсов"), null=True, blank=True)
    peer_self_assessment = models.TextField(verbose_name=_("Самооценка учащихся и отзывы сверстников"), null=True, blank=True)
    reflections_ongoing = models.TextField(verbose_name=_("Текущая рефлексия для всех учителей"), null=True, blank=True)
    reflections_additional = models.TextField(verbose_name=_("Дополнительная рефлексия по предметам"), null=True, blank=True)
    reflections_teacher = models.TextField(verbose_name=_("Рефлексия учителя"), null=True, blank=True)
    reflections_students = models.TextField(verbose_name=_("Рефлексия студентов"), null=True, blank=True)
    reflections_assessment = models.TextField(verbose_name=_("Рефлексия оценивания"), null=True, blank=True)
    notes = models.TextField(verbose_name=_("Замечания"), null=True, blank=True)
    class Meta:
        verbose_name = 'PYP: UnitPlan'
        verbose_name_plural = 'PYP: UnitPlans'
        ordering = ['year', 'order', 'title']
    def __str__(self):
        return f"{self.title} ({self.grade})"
    
class PypLinesOfInquiry(models.Model):
    """ Линии исследования в юните PYP """
    name = models.CharField(max_length=255, verbose_name=_("Линия исследования"))
    key_concept = models.ForeignKey('units.PypKeyConcept', verbose_name=_("Ключевой концепт"), on_delete=models.CASCADE, related_name="inquiry_lines")
    unit = models.ForeignKey('units.PypUnitPlanner', verbose_name=_("Юнит PYP"), on_delete=models.CASCADE, related_name="inquiry_lines")
    class Meta:
        verbose_name = 'PYP: UnitPlan - Линия исследования'
        verbose_name_plural = 'PYP: UnitPlans - Линии исследования'
        ordering = ['unit', 'key_concept', 'name']
    def __str__(self):
        return f"{self.name} ({self.key_concept})"
    
class PypRelatedConcept(models.Model):
    """ Сопутствующие понятия в юните PYP """
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    unit = models.ForeignKey('units.PypUnitPlanner', verbose_name=_("Юнит PYP"), on_delete=models.CASCADE, related_name="related_concepts")
    class Meta:
        verbose_name = 'PYP: UnitPlan - Сопутствующее понятие'
        verbose_name_plural = 'PYP: UnitPlans - Сопутствующие понятия'
        ordering = ['unit', 'name']
    def __str__(self):
        return f"{self.name} ({self.unit})"
    
class PypProfileAttribute(models.Model):
    """ Качества портрета студента в юните PYP """
    profile = models.ForeignKey('units.LearnerProfile', verbose_name=_("Профиль студента"), on_delete=models.CASCADE, related_name="pyp_profiles")
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    unit = models.ForeignKey('units.PypUnitPlanner', verbose_name=_("Юнит PYP"), on_delete=models.CASCADE, related_name="profile_attributes")
    class Meta:
        verbose_name = 'PYP: UnitPlan - Развитие профиля студента'
        verbose_name_plural = 'PYP: UnitPlans - Развитие профиля студента'
        ordering = ['unit', 'profile']
    def __str__(self):
        return f"{self.profile}"
    
class PypAtlDevelop(models.Model):
    """ Развитие ATL-навыков в юните PYP """
    atl = models.ForeignKey('units.PypAtlSkill', verbose_name=_("Навык ATL"), on_delete=models.CASCADE, related_name="atl_develops")
    action = models.TextField(verbose_name=_("Описание учебных действий"), null=True, blank=True)
    unit = models.ForeignKey('units.PypUnitPlanner', verbose_name=_("Юнит PYP"), on_delete=models.CASCADE, related_name="atl_develops")
    class Meta:
        verbose_name = 'PYP: UnitPlan - Развитие ATL'
        verbose_name_plural = 'PYP: UnitPlans - Развитие ATL'
        ordering = ['unit', 'atl']
    def __str__(self):
        return f"{self.atl} ({self.action})"