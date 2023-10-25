from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.units.models import CriterionChoices, StrandLetterChoices, QuestionTypeChoices, PostTypeChoices

class Criterion(models.Model):
    """ Критерии оценивания """
    letter = models.CharField(verbose_name=_("Символ"), choices=CriterionChoices.choices, max_length=1)
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    group = models.ForeignKey('syllabus.IbSubjectGroup', verbose_name=_("Предметная группа IB"), on_delete=models.SET_NULL, null=True, related_name="criterion")
    class Meta:
        verbose_name = 'MYP: Критерий оценивания'
        verbose_name_plural = 'MYP: Критерии оценивания'
        ordering = ['group', 'letter']
    def __str__(self):
        return "{} | {}".format(self.letter, self.group)

class Strand(models.Model):
    """ Стрэнды - аспекты образовательных достижений """
    number = models.PositiveIntegerField(verbose_name=_("Абсолютный номер"), default=1)
    letter = models.PositiveIntegerField(verbose_name=_("Метка в критерии"), choices=StrandLetterChoices.choices, default=1)
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    criterion = models.ForeignKey('units.Criterion', verbose_name=_("Критерий"), on_delete=models.SET_NULL, null=True, related_name="strand")
    class Meta:
        verbose_name = 'MYP: Стрэнд'
        verbose_name_plural = 'MYP: Стрэнды'
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
        verbose_name = 'MYP: Образовательный уровень'
        verbose_name_plural = 'MYP: Образовательные уровни'
        ordering = ['name']
    def __str__(self):
        return "{}".format(self.name)
    
class Objective(models.Model):
    """ Образовательные цели """
    name = models.CharField(max_length=255, verbose_name=_("Описание"), null=True)
    name_rus = models.CharField(max_length=255, verbose_name=_("Описание на рус. языке"), null=True)
    level = models.ForeignKey('units.EducationalLevel', verbose_name=_("Уровень в IB"), on_delete=models.SET_NULL, null=True, related_name="objective")
    strand = models.ForeignKey('units.Strand', verbose_name=_("Стрэнд"), on_delete=models.SET_NULL, null=True, related_name="objective")
    class Meta:
        verbose_name = 'MYP: Образовательная цель'
        verbose_name_plural = 'MYP: Образовательные цели'
        ordering = ['level', 'strand']
    def __str__(self):
        return "{} | {}. {}...".format(self.level, self.strand.letter, self.name[:10])
    
class AchievementLevel(models.Model):
    """ Уровни достижений образовательных целей """
    name = models.TextField(verbose_name=_("Описание"), null=True, blank=False)
    name_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    objective = models.ForeignKey('units.Objective', verbose_name=_("Образовательная цель"), on_delete=models.CASCADE, null=True, related_name="achievelevel")
    point = models.PositiveIntegerField(verbose_name=_("Баллы"), default=0)
    class Meta:
        verbose_name = 'MYP: Уровень достижений'
        verbose_name_plural = 'MYP: Уровни достижений'
        ordering = ['objective', 'point']
    def __str__(self):
        return "{}...:{}".format(self.name[:30], self.point)
    
class Aim(models.Model):
    """ Цели """
    name = models.CharField(max_length=255,verbose_name=_("Название"), null=True, blank=False)
    name_rus = models.CharField(max_length=255,verbose_name=_("Название на рус. языке"), null=True, blank=True)
    group = models.ForeignKey('syllabus.IbSubjectGroup', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL, null=True, related_name="aims")
    class Meta:
        verbose_name = 'MYP: Цель'
        verbose_name_plural = 'MYP: Цели'
        ordering = ['group', 'name']
    def __str__(self):
        return "{} | {}...".format(self.group, self.name[:10])

class MypKeyConcept(models.Model):
    """ Ключевые концепты """
    name = models.CharField(max_length=32, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=32, verbose_name=_("Название на рус. языке"), null=True)
    description = models.TextField(verbose_name=_("Описание"), null=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True)
    groups = models.ManyToManyField('syllabus.IbSubjectGroup',
                                    verbose_name=_("Рекомендуемые предметные группы"),
                                    through='units.MypKeyConceptOfSubjects',
                                    related_name="key_concepts")
    class Meta:
        verbose_name = 'MYP: Ключевой концепт'
        verbose_name_plural = 'MYP: Ключевые концепты'
        ordering = ['name']
    def __str__(self):
        return "{}".format(self.name)
    
class MypKeyConceptOfSubjects(models.Model):
    """ Рекомендуемые предметы для ключевых концептов с описанием """
    key_concept = models.ForeignKey('units.MypKeyConcept', verbose_name=_("Ключевой концепт"), on_delete=models.SET_NULL, null=True, related_name="recomended_subjects")
    group = models.ForeignKey('syllabus.IbSubjectGroup', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL, null=True, related_name="recomended_keyconcepts")
    comment = models.TextField(verbose_name=_("Комментарии"), null=True, blank=True)
    comment_rus = models.TextField(verbose_name=_("Комментарии на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'MYP: Ключевые концепции - Рекомендуемый предмет'
        verbose_name_plural = 'MYP: Ключевые концепции - Рекомендуемые предметы'
        ordering = ['group', 'key_concept']

class RelatedConcept(models.Model):
    """ Сопутствующие концепты """
    name = models.CharField(max_length=64, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    disciplines = models.ManyToManyField('syllabus.IbDisciplines', verbose_name=_("Специальные дисциплины"), related_name="related_concepts")
    class Meta:
        verbose_name = 'MYP: Сопутствующий концепт'
        verbose_name_plural = 'MYP: Сопутствующие концепты'
        ordering = ['id', 'name']
    def __str__(self):
        return "{}".format(self.name)

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
        return "{}".format(self.name)

class GlobalContextExploration(models.Model):
    """ Линии исследования глобальных контекстов """
    name = models.CharField(max_length=64, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True)
    global_context = models.ForeignKey('units.GlobalContext', verbose_name=_("Глобальный контекст"), on_delete=models.CASCADE, null=True, related_name="explorations")
    class Meta:
        verbose_name = 'MYP: Глобальный контекст - Линия исследования'
        verbose_name_plural = 'MYP: Глобальный контекст - Линии исследований'
        ordering = ['global_context', 'name']
    def __str__(self):
        return "{} ({})".format(self.name, self.global_context)

class MypAtlSkill(models.Model):
    """ Навыки ATL в MYP """
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True)
    cluster = models.ForeignKey('units.AtlCluster', verbose_name=_("Кластер ATL"), on_delete=models.CASCADE, null=False, related_name="myp_skills")
    class Meta:
        verbose_name = 'MYP: Навык ATL'
        verbose_name_plural = 'MYP: Навыки ATL'
        ordering = ['cluster', 'name']
    def __str__(self):
        return "{} ({})".format(self.name, self.cluster)
    
class MypUnitPlanner(models.Model):
    """ ЮнитПланеры MYP """
    title = models.CharField(max_length=255, verbose_name=_("Название юнита"))
    order = models.PositiveSmallIntegerField(verbose_name=_("Номер"), default=0)
    subject = models.ForeignKey('syllabus.Subject', verbose_name=_("Предмет"), on_delete=models.SET_NULL, null=True, related_name="myp_unitplans")
    level = models.ForeignKey('units.EducationalLevel', verbose_name=_("Образовательный уровень"), on_delete=models.SET_NULL, null=True, related_name="myp_unitplans")
    authors = models.ManyToManyField('general.User', verbose_name=_("Авторы"), related_name="myp_unitplans")
    year = models.ForeignKey('general.StudyYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, related_name="myp_unitplans")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=0)
    key_concepts = models.ManyToManyField('units.MypKeyConcept', verbose_name=_("Ключевые концепты"), blank=True, related_name="myp_unitplans")
    related_concepts = models.ManyToManyField('units.RelatedConcept', verbose_name=_("Сопутствующие концепты"), blank=True, related_name="myp_unitplans")
    conceptual_understanding = models.TextField(verbose_name=_("Концептуальное понимание"), null=True, blank=True)
    global_context = models.ForeignKey('units.GlobalContext', verbose_name=_("Глобальный контекст"), on_delete=models.SET_NULL, null=True, blank=True, related_name="myp_unitplans")
    explorations = models.ManyToManyField('units.GlobalContextExploration', verbose_name=_("Линии исследования"), blank=True, related_name="myp_unitplans")
    statement_inquiry = models.TextField(verbose_name=_("Формулировка исследования"), null=True, blank=True)
    aims = models.ManyToManyField('units.Aim', verbose_name=_("Цели"), blank=True, related_name="myp_unitplans")
    strands = models.ManyToManyField('units.Strand', verbose_name=_("Стренды предметной группы"), blank=True, related_name="myp_unitplans")
    content = models.TextField(verbose_name=_("Содержание (темы, знания и умения)"), null=True, blank=True)
    skills = models.TextField(verbose_name=_("Умения"), null=True, blank=True)
    international_mindedness = models.TextField(verbose_name=_("Межкультурное понимание"), null=True, blank=True)
    academic_integrity = models.TextField(verbose_name=_("Академическая честность"), null=True, blank=True)
    language_development = models.TextField(verbose_name=_("Языковое развитие"), null=True, blank=True)
    infocom_technology = models.TextField(verbose_name=_("Использование средств ИКТ"), null=True, blank=True)
    service_as_action = models.TextField(verbose_name=_("Служение как действие"), null=True, blank=True)
    criteria = models.ManyToManyField('units.Criterion', verbose_name=_("Критерии оценки"), blank=True, related_name="myp_unitplans")
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
    interdisciplinary = models.ForeignKey('units.MypUnitPlannerInterdisciplinary', verbose_name=_("Междисциплинарный юнит"), on_delete=models.SET_NULL, null=True, blank=True, related_name="myp_unitplans")
    class Meta:
        verbose_name = 'MYP: UnitPlan'
        verbose_name_plural = 'MYP: UnitPlans'
        ordering = ['year', 'subject', 'order', 'title']
    def __str__(self):
        return "{} ({})".format(self.title, self.year)
    
class MypInquiryQuestion(models.Model):
    """ Исследовательские вопросы в рамках юнита """
    question = models.CharField(max_length=255, verbose_name=_("Исследовательский вопрос"))
    type = models.CharField(choices=QuestionTypeChoices.choices, verbose_name=_("Тип вопроса"), default='Factual', max_length=12)
    line = models.CharField(max_length=255, verbose_name=_("Линия исследования"), null=True)
    unit = models.ForeignKey('units.MypUnitPlanner', verbose_name=_("Юнит MYP"), on_delete=models.CASCADE, related_name="inquiry_questions")
    idu = models.ForeignKey('units.MypUnitPlannerInterdisciplinary', verbose_name=_("Междисциплинарный юнит MYP"), on_delete=models.CASCADE, related_name="inquiry_questions")
    class Meta:
        verbose_name = 'MYP: UnitPlan - Исследовательский вопрос'
        verbose_name_plural = 'MYP: UnitPlans - Исследовательские вопросы'
        ordering = ['type', 'question']
    def __str__(self):
        return "{} ({})".format(self.question, self.type)
    
class MypAtlDevelop(models.Model):
    """ Развитие ATL-навыков в рамках юнита """
    atl = models.ForeignKey('units.MypAtlSkill', verbose_name=_("Навык ATL"), on_delete=models.CASCADE, related_name="atl_develops")
    strand = models.ForeignKey('units.Strand', verbose_name=_("Предметный стрэнд"), on_delete=models.CASCADE, related_name="atl_develops")
    action = models.TextField(verbose_name=_("Описание учебных действий"), null=True, blank=True)
    unit = models.ForeignKey('units.MypUnitPlanner', verbose_name=_("Юнит MYP"), on_delete=models.CASCADE, related_name="atl_develops")
    class Meta:
        verbose_name = 'MYP: UnitPlan - Развитие ATL'
        verbose_name_plural = 'MYP: UnitPlans - Развитие ATL'
        ordering = ['strand']
    def __str__(self):
        return "{} ({})".format(self.atl, self.action)

class MypProfileDevelop(models.Model):
    """ Развитие профиля студента MYP в рамках юнита """
    profile = models.ForeignKey('units.LearnerProfile', verbose_name=_("Профиль студента"), on_delete=models.CASCADE, related_name="profile_develops")
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    unit = models.ForeignKey('units.MypUnitPlanner', verbose_name=_("Юнит MYP"), on_delete=models.CASCADE, related_name="profile_develops")
    class Meta:
        verbose_name = 'MYP: UnitPlan - Развитие профиля студента'
        verbose_name_plural = 'MYP: UnitPlans - Развитие профиля студента'
        ordering = ['profile']
    def __str__(self):
        return "{}".format(self.profile)
    
class MypReflectionPost(models.Model):
    """ Посты рефлексии по планеру MYP """
    post = models.TextField(verbose_name=_("Содержание рефлексии"), null=True, blank=True)
    type = models.CharField(choices=PostTypeChoices.choices, verbose_name=_("Тип рефлексии"), max_length=6)
    author = models.ForeignKey('general.User', verbose_name=_("Автор поста"), on_delete=models.SET_NULL, null=True, related_name="reflection_posts")
    unit = models.ForeignKey('units.MypUnitPlanner', verbose_name=_("Юнит MYP"), on_delete=models.CASCADE, related_name="reflection_posts")
    idu = models.ForeignKey('units.MypUnitPlannerInterdisciplinary', verbose_name=_("Междисциплинарный юнит MYP"), on_delete=models.CASCADE, related_name="reflection_posts")
    class Meta:
        verbose_name = 'MYP: UnitPlan - Пост рефлексии'
        verbose_name_plural = 'MYP: UnitPlans - Посты рефлексии'
        ordering = ['type', 'post']
    def __str__(self):
        return "{}: {}".format(self.type, self.post[:15])
    
class MypUnitPlannerInterdisciplinary(models.Model):
    """ Дополнение для междисциплинарных планеров MYP """
    title = models.CharField(max_length=255, verbose_name=_("Название междисциплинарного юнита"))
    year = models.ForeignKey('general.StudyYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, blank=False, related_name="myp_idunitplans")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=0)
    purpose_integration = models.TextField(verbose_name=_("Цель интеграции"), null=True, blank=True)
    key_concepts = models.ManyToManyField('units.MypKeyConcept', verbose_name=_("Ключевые концепты"), blank=True, related_name="myp_idunitplans")
    related_concepts = models.ManyToManyField('units.RelatedConcept', verbose_name=_("Сопутствующие концепты"), blank=True, related_name="myp_idunitplans")
    conceptual_understanding = models.TextField(verbose_name=_("Концептуальное понимание"), null=True, blank=True)
    global_context = models.ForeignKey('units.GlobalContext', verbose_name=_("Глобальный контекст"), on_delete=models.SET_NULL, null=True, blank=True, related_name="myp_idunitplans")
    explorations = models.ManyToManyField('units.GlobalContextExploration', verbose_name=_("Линии исследования"), blank=True, related_name="myp_idunitplans")
    statement_inquiry = models.TextField(verbose_name=_("Формулировка исследования"), null=True, blank=True)
    aims = models.ManyToManyField('units.Aim', verbose_name=_("Цели"), blank=True, related_name="myp_idunitplans")
    criteria = models.ManyToManyField('units.Criterion', verbose_name=_("Критерии оценки"), blank=True, related_name="myp_idunitplans")
    strands = models.ManyToManyField('units.Strand', verbose_name=_("Образовательные цели"), blank=True, related_name="myp_idunitplans")
    tasks = models.TextField(verbose_name=_("Задания"), null=True, blank=True)
    introduction = models.TextField(verbose_name=_("Введение в МДП"), null=True, blank=True)
    learning_teaching = models.TextField(verbose_name=_("Учебная деятельность"), null=True, blank=True)
    formative_assessment = models.TextField(verbose_name=_("Формирующее оценивание"), null=True, blank=True)
    summative_assessment = models.TextField(verbose_name=_("Итоговое оценивание"), null=True, blank=True)
    differentiation = models.TextField(verbose_name=_("Дифференцированный подход"), null=True, blank=True)
    class Meta:
        verbose_name = 'MYP: UnitPlan - Междисциплинарный юнит'
        verbose_name_plural = 'MYP: UnitPlans - Междисциплинарные юниты'
        ordering = ['year', 'title']
    def __str__(self):
        return "{}".format(self.title)