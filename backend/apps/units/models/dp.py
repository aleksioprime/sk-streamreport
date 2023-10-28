from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from apps.units.models import  (
    LevelDpChoices, 
    QuestionTypeDpChoices, 
    AimDpChoices, 
    LanguageLearningChoices, 
    TokConnectionsChoices, 
    CasConnectionsChoices, 
    LearningProcessChoices,
    DifferentiationChoices,
    PostTypeChoices
    )

class DpAim(models.Model):
    """ Цели дисциплины """
    name = models.CharField(max_length=255,verbose_name=_("Name"), null=True, blank=False)
    type = models.CharField(choices=AimDpChoices.choices, verbose_name=_("Тype (group or subject)"), max_length=12)
    discipline = models.ForeignKey('syllabus.IbDiscipline', verbose_name=_("Discipline IB"), on_delete=models.SET_NULL, null=True, related_name="dp_aims")
    class Meta:
        verbose_name = 'DP: Aim'
        verbose_name_plural = 'DP: Aims'
        ordering = ['discipline', 'name']
    def __str__(self):
        return f"{self.discipline} | {self.name[:10]}..."
    
class DpObjective(models.Model):
    """ Предметные цели """
    number = models.PositiveIntegerField(verbose_name=_("Number"), default=1)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    discipline = models.ForeignKey('syllabus.IbDiscipline', verbose_name=_("Discipline IB"), on_delete=models.SET_NULL, null=True, related_name="dp_objectives")
    class Meta:
        verbose_name = 'DP: Objective'
        verbose_name_plural = 'DP: Objectives'
        ordering = ['discipline', 'number']
    def __str__(self):
        return f"{self.number} ({self.name})"

class DpObjectiveItem(models.Model):
    """ Пункты предметных целей """
    letter = models.CharField(verbose_name=_("Letter"), max_length=1)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    objective = models.ForeignKey('units.DpObjective', verbose_name=_("Objective"), on_delete=models.SET_NULL, null=True, related_name="items")
    class Meta:
        verbose_name = 'DP: Objectives Item'
        verbose_name_plural = 'DP: Objectives Items'
        ordering = ['objective', 'letter']
    def __str__(self):
        return f"{self.letter} ({self.name})"

class CourseTopic(models.Model):
    """ Темы курса дисциплины DP """
    letter = models.CharField(verbose_name=_("Letters"), max_length=12)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    discipline = models.ForeignKey('syllabus.IbDiscipline', verbose_name=_("Discipline IB"), on_delete=models.SET_NULL, null=True, related_name="dp_topics")
    class Meta:
        verbose_name = 'DP: Course topic'
        verbose_name_plural = 'DP: Course topics'
        ordering = ['discipline', 'letter']
    def __str__(self):
        return f"{self.letter} ({self.name})"

class CourseContent(models.Model):
    """ Контент курса дисциплины DP """
    letter = models.CharField(verbose_name=_("Letters"), max_length=12)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    topic = models.ForeignKey('units.CourseTopic', verbose_name=_("Course Topic"), on_delete=models.SET_NULL, null=True, related_name="course_contents")
    class Meta:
        verbose_name = 'DP: Course content'
        verbose_name_plural = 'DP: Course contents'
        ordering = ['topic', 'letter']
    def __str__(self):
        return f"{self.letter} ({self.name})"
    
class Criterion(models.Model):
    """ Критерии оценивания """
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    letter = models.CharField(verbose_name=_("Letter"), max_length=1)
    discipline = models.ForeignKey('syllabus.IbDiscipline', verbose_name=_("Discipline IB"), on_delete=models.SET_NULL, null=True, related_name="dp_criteria")
    class Meta:
        verbose_name = 'DP: Criterion'
        verbose_name_plural = 'DP: Criteria'
        ordering = ['discipline', 'letter']
    def __str__(self):
        return f"{self.letter}. {self.name}"

class DpAtlSkill(models.Model):
    """ Навыки ATL в DP """
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True)
    cluster = models.ForeignKey('units.AtlCluster', verbose_name=_("Кластер ATL"), on_delete=models.CASCADE, null=False, related_name="dp_skills")
    class Meta:
        verbose_name = 'DP: ATL Skills'
        verbose_name_plural = 'DP: ATL Skills'
        ordering = ['cluster', 'name']
    def __str__(self):
        return f"{self.name} ({self.cluster})"

class DpUnitPlanner(models.Model):
    """ ЮнитПланеры DP """
    title = models.CharField(max_length=255, verbose_name=_("Title unit"))
    order = models.PositiveSmallIntegerField(verbose_name=_("Number"), default=0)
    year = models.ForeignKey('general.StudyYear', verbose_name=_("Study year"), on_delete=models.SET_NULL, null=True, related_name="dp_unitplans")
    subject = models.ForeignKey('syllabus.Subject', verbose_name=_("Subject"), on_delete=models.SET_NULL, null=True, related_name="dp_unitplans")
    authors = models.ManyToManyField('general.User', verbose_name=_("Authors"), related_name="dp_authors")
    teachers = models.ManyToManyField('general.User', verbose_name=_("Teachers"), related_name="dp_teachers")
    levels = ArrayField(
        models.CharField(max_length=5, choices=LevelDpChoices.choices),
        verbose_name=_("Levels"), default=list, blank=True)
    hours = models.PositiveSmallIntegerField(verbose_name=_("Hours"), default=0)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    transfer_goals = models.TextField(verbose_name=_("Transfer goals"), null=True, blank=True)
    essential_understandings = models.TextField(verbose_name=_("Essential Understandings"), null=True, blank=True)
    misunderstandings = models.TextField(verbose_name=_("Missed concepts/misunderstandings"), null=True, blank=True)
    aims = models.ManyToManyField('units.DpAim', verbose_name=_("Aims"), blank=True, related_name="dp_unitplans")
    objectives = models.ManyToManyField('units.DpObjective', verbose_name=_("Objectives"), blank=True, related_name="dp_unitplans")
    syllabus_content = models.ManyToManyField('units.CourseContent', verbose_name=_("Syllabus Content"), blank=True, related_name="dp_unitplans")
    content = models.TextField(verbose_name=_("Content"), null=True, blank=True)
    skills = models.TextField(verbose_name=_("Skills"), null=True, blank=True)
    concepts = models.TextField(verbose_name=_("Concepts"), null=True, blank=True)
    international_mindedness = models.TextField(verbose_name=_("International Mindedness"), null=True, blank=True)
    academic_integrity = models.TextField(verbose_name=_("Academic Integrity"), null=True, blank=True)
    infocom_technology = models.TextField(verbose_name=_("Information Communication Technology"), null=True, blank=True)
    language_learning = ArrayField(
        models.CharField(max_length=64, choices=LanguageLearningChoices.choices),
        verbose_name=_("Language and learning"), default=list, blank=True)
    language_learning_text = models.TextField(verbose_name=_("Language and learning description"), null=True, blank=True)
    ee_connections = models.TextField(verbose_name=_("EE / Individual project connections"), null=True, blank=True)
    tok_connections = ArrayField(
        models.CharField(max_length=64, choices=TokConnectionsChoices.choices),
        verbose_name=_("TOK Connections"), default=list, blank=True)
    tok_connections_text = models.TextField(verbose_name=_("TOK Connections description"), null=True, blank=True)
    cas_connections = ArrayField(
        models.CharField(max_length=64, choices=CasConnectionsChoices.choices),
        verbose_name=_("CAS Connections"), default=list, blank=True)
    cas_connections_text = models.TextField(verbose_name=_("CAS Connections description"), null=True, blank=True)
    formative_assessment = models.TextField(verbose_name=_("Formative assessment"), null=True, blank=True)
    summative_assessment = models.TextField(verbose_name=_("Summative assessment"), null=True, blank=True)
    internal_assessment =  models.TextField(verbose_name=_("Internal assessment"), null=True, blank=True)
    peer_self_assessment = models.TextField(verbose_name=_("Peer and self assessment"), null=True, blank=True)
    criteria = models.ManyToManyField('units.Criterion', verbose_name=_("Assessment criteria"), blank=True, related_name="dp_unitplans")
    criteria_text = models.TextField(verbose_name=_("Assessment criteria description"), null=True, blank=True)
    prior_experiences = models.TextField(verbose_name=_("Prior learning experience"), null=True, blank=True)
    pedagogical_approaches = models.TextField(verbose_name=_("Pedagogical approaches"), null=True, blank=True)
    student_expectations = models.TextField(verbose_name=_("Student expectations"), null=True, blank=True)
    feedback = models.TextField(verbose_name=_("Feedback"), null=True, blank=True)
    learning_process = ArrayField(
        models.CharField(max_length=64, choices=LearningProcessChoices.choices),
        verbose_name=_("Learning Process"), default=list, blank=True)
    learning_process_text = models.TextField(verbose_name=_("Learning Process description"), null=True, blank=True)
    differentiation = ArrayField(
        models.CharField(max_length=64, choices=DifferentiationChoices.choices),
        verbose_name=_("Differentiation"), default=list, blank=True)
    differentiation_text = models.TextField(verbose_name=_("Differentiation description"), null=True, blank=True)
    learning_experiences = models.TextField(verbose_name=_("Learning experiences and strategies"), null=True, blank=True)
    resources = models.TextField(verbose_name=_("Resources"), null=True, blank=True)
    cross_curricular_links = models.TextField(verbose_name=_("Cross-curricular links"), null=True, blank=True)
    co_curricular_links = models.TextField(verbose_name=_("Co-curricular links"), null=True, blank=True)
    work_well = models.TextField(verbose_name=_("What worked well?"), null=True, blank=True)
    work_well_not = models.TextField(verbose_name=_("What didn’t work well?"), null=True, blank=True)
    notes = models.TextField(verbose_name=_("Notes/changes/suggestions"), null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Update date"), auto_now=True)
    class Meta:
        verbose_name = 'DP: UnitPlan'
        verbose_name_plural = 'DP: UnitPlans'
        ordering = ['year', 'subject', 'order', 'title']
    def __str__(self):
        return f"{self.title} ({self.year})"
    
class DpInquiryQuestion(models.Model):
    """ Исследовательские вопросы в юните DP """
    question = models.CharField(max_length=255, verbose_name=_("Inquiry Question"))
    type = models.CharField(choices=QuestionTypeDpChoices.choices, verbose_name=_("Type"), default='Factual', max_length=16)
    unit = models.ForeignKey('units.DpUnitPlanner', verbose_name=_("Unit DP"), on_delete=models.CASCADE, related_name="inquiry_questions")
    class Meta:
        verbose_name = 'DP: UnitPlan - Inquiry Question'
        verbose_name_plural = 'DP: UnitPlans - Inquiry Questions'
        ordering = ['unit', 'type', 'question']
    def __str__(self):
        return f"{self.question} ({self.type})"
    
class DpAtlDevelop(models.Model):
    """ Развитие ATL-навыков в юните DP """
    atl = models.ForeignKey('units.DpAtlSkill', verbose_name=_("ATL Skill"), on_delete=models.SET_NULL, null=True, related_name="atl_develops")
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    unit = models.ForeignKey('units.DpUnitPlanner', verbose_name=_("Unit DP"), on_delete=models.CASCADE, related_name="atl_develops")
    class Meta:
        verbose_name = 'DP: UnitPlan - Approaches to Learning'
        verbose_name_plural = 'DP: UnitPlans - Approaches to Learning'
        ordering = ['unit', 'atl']
    def __str__(self):
        return f"{self.atl} ({self.description})"
    
class DpProfileDevelop(models.Model):
    """ Развитие профиля студента в юните DP """
    profile = models.ForeignKey('units.LearnerProfile', verbose_name=_("IB Learner Profile"), on_delete=models.CASCADE, related_name="dp_profiles")
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    unit = models.ForeignKey('units.DpUnitPlanner', verbose_name=_("Unit DP"), on_delete=models.CASCADE, related_name="profile_develops")
    class Meta:
        verbose_name = 'DP: UnitPlan - Learner Profile'
        verbose_name_plural = 'DP: UnitPlans - Learner Profile'
        ordering = ['unit', 'profile']
    def __str__(self):
        return f"{self.profile}"
    
class DpReflectionPost(models.Model):
    """ Посты рефлексии по планеру DP """
    post = models.TextField(verbose_name=_("Post"), null=True, blank=True)
    type = models.CharField(choices=PostTypeChoices.choices, verbose_name=_("Type"), max_length=6)
    author = models.ForeignKey('general.User', verbose_name=_("Author"), on_delete=models.SET_NULL, null=True, related_name="dp_reflections")
    unit = models.ForeignKey('units.DpUnitPlanner', verbose_name=_("Unit DP"), on_delete=models.CASCADE, related_name="reflection_posts")
    class Meta:
        verbose_name = 'DP: UnitPlan - Reflection Post'
        verbose_name_plural = 'DP: UnitPlans - Reflection Posts'
        ordering = ['unit', 'type', 'post']
    def __str__(self):
        return f"{self.type}: {self.post[:15]}"