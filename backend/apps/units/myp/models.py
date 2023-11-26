from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.ibo.models import (
    UnitPlanerBaseModel
)

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

class EducationalLevelChoices(models.TextChoices):
        level_1 = "first", "Year 1 / Emergent"
        level_2 = "second", "Year 3 / Capable"
        level_3 = "third", "Year 5 / Proficient"
        level_all = None, "Year All"

class MypObjective(models.Model):
    """ Предметные цели/критерии оценивания """
    letter = models.CharField(verbose_name=_("Символ"), choices=ObjectiveLetterChoices.choices, max_length=1)
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    group = models.ForeignKey('curriculum.IbSubjectGroup', verbose_name=_("Предметная группа IB"), on_delete=models.SET_NULL, null=True, related_name="myp_objectives")
    class Meta:
        verbose_name = 'MYP: Предметная цель'
        verbose_name_plural = 'MYP: Предметные цели'
        ordering = ['group', 'letter']
    def __str__(self):
        return f"{self.letter} | {self.group}"

class Strand(models.Model):
    """ Стрэнды предметных целей """
    number = models.PositiveIntegerField(verbose_name=_("Абсолютный номер"), default=1)
    letter = models.PositiveIntegerField(verbose_name=_("Метка в критерии"), choices=StrandLetterChoices.choices, default=1)
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    objective = models.ForeignKey('myp.MypObjective', verbose_name=_("Предметная цель"), on_delete=models.SET_NULL, null=True, related_name="strands")
    class Meta:
        verbose_name = 'MYP: Стрэнд'
        verbose_name_plural = 'MYP: Стрэнды'
        ordering = ['objective', 'number', 'letter']
    def __str__(self):
        return f"{self.number} ({self.get_letter_display()}). {self.name[:15]}..."
 
class StrandLevel(models.Model):
    """ Предметные цели по уровням и годам обучения """
    name = models.CharField(max_length=255, verbose_name=_("Описание"), null=True)
    name_rus = models.CharField(max_length=255, verbose_name=_("Описание на рус. языке"), null=True)
    level = models.CharField(verbose_name=_("Образовательный уровень"), null=True, choices=ObjectiveLetterChoices.choices, max_length=12)
    strand = models.ForeignKey('myp.Strand', verbose_name=_("Стрэнд"), on_delete=models.SET_NULL, null=True, related_name="strand_levels")
    class Meta:
        verbose_name = 'MYP: Предметная цель на уровне'
        verbose_name_plural = 'MYP: Предметные цели на уровне'
        ordering = ['level', 'strand']
    def __str__(self):
        return f"{self.level} | {self.strand.letter}. {self.name[:10]}..."
    
class StrandLevelAchievement(models.Model):
    """ Уровни достижений образовательных целей """
    name = models.TextField(verbose_name=_("Описание"), null=True, blank=False)
    name_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    level = models.ForeignKey('myp.StrandLevel', verbose_name=_("Предметная цель"), on_delete=models.CASCADE, null=True, related_name="achieve_levels")
    point = models.PositiveIntegerField(verbose_name=_("Баллы"), default=0)
    class Meta:
        verbose_name = 'MYP: Уровень достижений'
        verbose_name_plural = 'MYP: Уровни достижений'
        ordering = ['level', 'point']
    def __str__(self):
        return  f"{self.name[:30]}...:{self.point}"
    
class MypAim(models.Model):
    """ Цели предметной группы """
    name = models.CharField(max_length=255,verbose_name=_("Название"), null=True, blank=False)
    name_rus = models.CharField(max_length=255,verbose_name=_("Название на рус. языке"), null=True, blank=True)
    group = models.ForeignKey('curriculum.IbSubjectGroup', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL, null=True, related_name="myp_aims")
    class Meta:
        verbose_name = 'MYP: Цель'
        verbose_name_plural = 'MYP: Цели'
        ordering = ['group', 'name']
    def __str__(self):
        return f"{self.group} | {self.name[:10]}..."

class MypKeyConcept(models.Model):
    """ Ключевые концепты """
    name = models.CharField(max_length=32, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=32, verbose_name=_("Название на рус. языке"), null=True)
    description = models.TextField(verbose_name=_("Описание"), null=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True)
    groups = models.ManyToManyField('curriculum.IbSubjectGroup',
                                    verbose_name=_("Рекомендуемые предметные группы"),
                                    through='myp.MypKeyConceptOfSubjects',
                                    related_name="key_concepts")
    class Meta:
        verbose_name = 'MYP: Ключевой концепт'
        verbose_name_plural = 'MYP: Ключевые концепты'
        ordering = ['name']
    def __str__(self):
        return f"{self.name}"
    
class MypKeyConceptOfSubjects(models.Model):
    """ Рекомендуемые предметы для ключевых концептов с описанием """
    key_concept = models.ForeignKey('myp.MypKeyConcept', verbose_name=_("Ключевой концепт"), on_delete=models.SET_NULL, null=True, related_name="subjects_recomends")
    group = models.ForeignKey('curriculum.IbSubjectGroup', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL, null=True, related_name="key_concepts_recomends")
    comment = models.TextField(verbose_name=_("Комментарии"), null=True, blank=True)
    comment_rus = models.TextField(verbose_name=_("Комментарии на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'MYP: Ключевые концепции - Рекомендуемый предмет'
        verbose_name_plural = 'MYP: Ключевые концепции - Рекомендуемые предметы'
        ordering = ['group', 'key_concept']
    def __str__(self):
        return f"{self.key_concept} - {self.group}"

class MypRelatedConcept(models.Model):
    """ Сопутствующие концепты """
    name = models.CharField(max_length=64, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    disciplines = models.ManyToManyField('curriculum.IbDiscipline', verbose_name=_("Специальные дисциплины"), related_name="related_concepts")
    class Meta:
        verbose_name = 'MYP: Сопутствующий концепт'
        verbose_name_plural = 'MYP: Сопутствующие концепты'
        ordering = ['id', 'name']
    def __str__(self):
        return f"{self.name}"

class GlobalContext(models.Model):
    """ Глобальные контексты """
    name = models.CharField(max_length=64, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True)
    description = models.TextField(verbose_name=_("Описание"), null=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True)
    class Meta:
        verbose_name = 'MYP: Глобальный контекст'
        verbose_name_plural = 'MYP: Глобальные контексты'
        ordering = ['id']
    def __str__(self):
        return f"{self.name}"

class GlobalContextExploration(models.Model):
    """ Линии исследования глобальных контекстов """
    name = models.CharField(max_length=64, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True)
    global_context = models.ForeignKey('myp.GlobalContext', verbose_name=_("Глобальный контекст"), on_delete=models.CASCADE, null=True, related_name="explorations")
    class Meta:
        verbose_name = 'MYP: Глобальный контекст - Линия исследования'
        verbose_name_plural = 'MYP: Глобальный контекст - Линии исследований'
        ordering = ['global_context', 'name']
    def __str__(self):
        return f"{self.name} ({self.global_context})"

class MypAtlSkill(models.Model):
    """ Навыки ATL в MYP """
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True)
    cluster = models.ForeignKey('ibo.AtlCluster', verbose_name=_("Кластер ATL"), on_delete=models.CASCADE, null=False, related_name="myp_skills")
    class Meta:
        verbose_name = 'MYP: Навык ATL'
        verbose_name_plural = 'MYP: Навыки ATL'
        ordering = ['cluster', 'name']
    def __str__(self):
        return f"{self.name} ({self.cluster})"
    
class MypUnitPlanner(UnitPlanerBaseModel):
    """ ЮнитПланеры MYP """
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.SET_NULL, null=True, related_name="myp_unitplans")
    level = models.CharField(verbose_name=_("Образовательный уровень"), choices=ObjectiveLetterChoices.choices, max_length=12, null=True)
    key_concept = models.ForeignKey('myp.MypKeyConcept', verbose_name=_("Ключевой концепт"), null=True, blank=True, on_delete=models.SET_NULL, related_name="myp_unitplans")
    related_concepts = models.ManyToManyField('myp.MypRelatedConcept', verbose_name=_("Сопутствующие концепты"), blank=True, related_name="myp_unitplans")
    conceptual_understanding = models.TextField(verbose_name=_("Концептуальное понимание"), null=True, blank=True)
    global_context = models.ForeignKey('myp.GlobalContext', verbose_name=_("Глобальный контекст"), on_delete=models.SET_NULL, null=True, blank=True, related_name="myp_unitplans")
    explorations = models.ManyToManyField('myp.GlobalContextExploration', verbose_name=_("Линии исследования"), blank=True, related_name="myp_unitplans")
    statement_inquiry = models.TextField(verbose_name=_("Формулировка исследования"), null=True, blank=True)
    aims = models.ManyToManyField('myp.MypAim', verbose_name=_("Цели"), blank=True, related_name="myp_unitplans")
    strands = models.ManyToManyField('myp.Strand', verbose_name=_("Стренды"), blank=True, related_name="myp_unitplans")
    content = models.TextField(verbose_name=_("Содержание (темы, знания и умения)"), null=True, blank=True)
    skills = models.TextField(verbose_name=_("Умения"), null=True, blank=True)
    international_mindedness = models.TextField(verbose_name=_("Межкультурное понимание"), null=True, blank=True)
    academic_integrity = models.TextField(verbose_name=_("Академическая честность"), null=True, blank=True)
    language_development = models.TextField(verbose_name=_("Языковое развитие"), null=True, blank=True)
    infocom_technology = models.TextField(verbose_name=_("Использование средств ИКТ"), null=True, blank=True)
    service_as_action = models.TextField(verbose_name=_("Служение как действие"), null=True, blank=True)
    objectives = models.ManyToManyField('myp.MypObjective', verbose_name=_("Предметные цели / Критерии оценки"), blank=True, related_name="myp_unitplans")
    formative_assessment = models.TextField(verbose_name=_("Формирующее оценивание"), null=True, blank=True)
    summative_assessment_task = models.TextField(verbose_name=_("Итоговое оценивание (задачи)"), null=True, blank=True)
    summative_assessment_soi = models.TextField(verbose_name=_("Итоговое оценивание (взаимосвязь с SOI)"), null=True, blank=True)
    peer_self_assessment = models.TextField(verbose_name=_("Взаимное и самооценивание"), null=True, blank=True)
    standardization_moderation = models.TextField(verbose_name=_("Стандартизация и модерация"), null=True, blank=True)
    prior_experiences = models.TextField(verbose_name=_("Предыдущий опыт обучения"), null=True, blank=True)
    learning_experiences = models.TextField(verbose_name=_("Учебная деятельность"), null=True, blank=True)
    teaching_strategies = models.TextField(verbose_name=_("Стратегии преподавания"), null=True, blank=True) 
    student_expectations = models.TextField(verbose_name=_("Ожидания студентов"), null=True, blank=True)
    feedback = models.TextField(verbose_name=_("Обратная связь"), null=True, blank=True)
    differentiation = models.TextField(verbose_name=_("Дифференцированный подход"), null=True, blank=True)
    resources = models.TextField(verbose_name=_("Ресурсы"), null=True, blank=True)
    interdisciplinary = models.ForeignKey('myp.MypUnitPlannerId', verbose_name=_("Междисциплинарный юнит"), on_delete=models.SET_NULL, null=True, blank=True, related_name="myp_unitplans")
    class Meta:
        verbose_name = 'MYP: UnitPlan'
        verbose_name_plural = 'MYP: UnitPlans'
        ordering = ['year', 'subject', 'order', 'title']
    def __str__(self):
        return f"{self.title} ({self.year}, {self.subject})"
    
class MypInquiryQuestion(models.Model):
    """ Исследовательские вопросы юните MYP """
    question = models.CharField(max_length=255, verbose_name=_("Исследовательский вопрос"))
    type = models.CharField(choices=QuestionTypeMypChoices.choices, verbose_name=_("Тип вопроса"), default='Factual', max_length=12)
    line = models.CharField(max_length=255, verbose_name=_("Линия исследования"), null=True)
    unit = models.ForeignKey('myp.MypUnitPlanner', verbose_name=_("Юнит MYP"), on_delete=models.CASCADE, related_name="inquiry_questions")
    class Meta:
        verbose_name = 'MYP: UnitPlan - Исследовательский вопрос'
        verbose_name_plural = 'MYP: UnitPlans - Исследовательские вопросы'
        ordering = ['type', 'question']
    def __str__(self):
        return f"{self.question} ({self.type})"
    
class MypAtlDevelop(models.Model):
    """ Развитие ATL-навыков в юните MYP """
    atl = models.ForeignKey('myp.MypAtlSkill', verbose_name=_("Навык ATL"), on_delete=models.CASCADE, related_name="atl_develops")
    strand = models.ForeignKey('myp.Strand', verbose_name=_("Предметный стрэнд"), on_delete=models.CASCADE, related_name="atl_develops")
    action = models.TextField(verbose_name=_("Описание учебных действий"), null=True, blank=True)
    unit = models.ForeignKey('myp.MypUnitPlanner', verbose_name=_("Юнит MYP"), on_delete=models.CASCADE, related_name="atl_develops")
    class Meta:
        verbose_name = 'MYP: UnitPlan - Развитие ATL'
        verbose_name_plural = 'MYP: UnitPlans - Развитие ATL'
        ordering = ['strand']
    def __str__(self):
        return f"{self.atl} ({self.action})"
    
class MypUnitPlannerId(UnitPlanerBaseModel):
    """ Дополнение для междисциплинарных планеров MYP """
    real_world_issue = models.TextField(verbose_name=_("Проблема реального мира"), null=True, blank=True)
    integrated_purpose = models.TextField(verbose_name=_("Цель интеграции"), null=True, blank=True)
    synthesis = models.TextField(verbose_name=_("Синтез"), null=True, blank=True)
    key_concepts = models.ManyToManyField('myp.MypKeyConcept', verbose_name=_("Ключевые концепты"), blank=True, related_name="myp_iduplans")
    conceptual_understanding = models.TextField(verbose_name=_("Концептуальное понимание"), null=True, blank=True)
    global_context = models.ForeignKey('myp.GlobalContext', verbose_name=_("Глобальный контекст"), on_delete=models.SET_NULL, null=True, blank=True, related_name="myp_iduplans")
    explorations = models.ManyToManyField('myp.GlobalContextExploration', verbose_name=_("Линии исследования"), blank=True, related_name="myp_iduplans")
    statement_inquiry = models.TextField(verbose_name=_("Формулировка исследования"), null=True, blank=True)
    objectives = models.ManyToManyField('myp.MypObjective', verbose_name=_("Критерии оценки"), blank=True, related_name="myp_iduplans")
    strands = models.ManyToManyField('myp.Strand', verbose_name=_("Предметные цели (стренды)"), blank=True, related_name="myp_iduplans")
    tasks = models.TextField(verbose_name=_("Задания"), null=True, blank=True)
    introduction = models.TextField(verbose_name=_("Введение в МДП"), null=True, blank=True)
    learning_teaching = models.TextField(verbose_name=_("Учебная деятельность"), null=True, blank=True)
    summative_assessment = models.TextField(verbose_name=_("Итоговое оценивание"), null=True, blank=True)
    differentiation = models.TextField(verbose_name=_("Дифференцированный подход"), null=True, blank=True)
    resources = models.TextField(verbose_name=_("Ресурсы"), null=True, blank=True)
    class Meta:
        verbose_name = 'MYP IDU: UnitPlan - Междисциплинарный юнит'
        verbose_name_plural = 'MYP IDU: UnitPlans - Междисциплинарные юниты'
        ordering = ['year', 'title']
    def __str__(self):
        return f"{self.title} ({self.year})"
    
class MypInquiryQuestionIdu(models.Model):
    """ Исследовательские вопросы междисциплинарного юнита MYP """
    question = models.CharField(max_length=255, verbose_name=_("Исследовательский вопрос"))
    type = models.CharField(choices=QuestionTypeMypChoices.choices, verbose_name=_("Тип вопроса"), default='Factual', max_length=12)
    line = models.CharField(max_length=255, verbose_name=_("Линия исследования"), null=True)
    unit = models.ForeignKey('myp.MypUnitPlannerId', verbose_name=_("Междисциплинарный юнит MYP"), on_delete=models.CASCADE, related_name="inquiry_questions")
    class Meta:
        verbose_name = 'MYP IDU: UnitPlan - Исследовательский вопрос'
        verbose_name_plural = 'MYP IDU: UnitPlans - Исследовательские вопросы'
        ordering = ['type', 'question']
    def __str__(self):
        return f"{self.question} ({self.type})"

class MypAtlDevelopIdu(models.Model):
    """ Развитие ATL-навыков в междисциплинарном юните MYP """
    atl = models.ForeignKey('myp.MypAtlSkill', verbose_name=_("Навык ATL"), on_delete=models.CASCADE, related_name="idu_atl_develops")
    strand = models.ForeignKey('myp.Strand', verbose_name=_("Предметный стрэнд"), on_delete=models.CASCADE, related_name="idu_atl_develops")
    action = models.TextField(verbose_name=_("Описание учебных действий"), null=True, blank=True)
    unit = models.ForeignKey('myp.MypUnitPlannerId', verbose_name=_("Междисциплинарный юнит MYP"), on_delete=models.CASCADE, related_name="atl_develops")
    class Meta:
        verbose_name = 'MYP IDU: UnitPlan - Развитие ATL'
        verbose_name_plural = 'MYP IDU: UnitPlans - Развитие ATL'
        ordering = ['strand']
    def __str__(self):
        return f"{self.atl} ({self.action})"