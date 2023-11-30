from django.db import models
from django.utils.translation import gettext_lazy as _

class Syllabus(models.Model):
    """ Программа курсов учебного предмета """
    authors = models.ManyToManyField('general.User', verbose_name=_("Авторы"), related_name="author_syllabi")
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.SET_NULL, null=True, related_name="syllabi")
    years = models.ManyToManyField('general.StudyYear', verbose_name=_("Параллели"), blank=True, related_name="syllabi")
    file = models.FileField(upload_to='courses/', blank=True, verbose_name=_("Файл рабочей программы"))
    class Meta:
        verbose_name = 'Учебный курс: программа всего курса'
        verbose_name_plural = 'Учебный курс: программа всего курса'
        ordering = ['subject']
    def __str__(self):
        return f"{self.subject}"

class Course(models.Model):
    """ Программа курса предмета в учебном году """
    syllabus = models.ForeignKey('syllabus.Syllabus', verbose_name=_("Учебная программа"), on_delete=models.SET_NULL, null=True, related_name="courses")
    year = models.ForeignKey('general.StudyYear', verbose_name=_("Параллель"), on_delete=models.SET_NULL, null=True, related_name="courses")
    class Meta:
        verbose_name = 'Учебный курс: программа года'
        verbose_name_plural = 'Учебный курс: программа года'
        ordering = ['syllabus', 'year']
    def __str__(self):
        return f"{self.syllabus} ({self.year})"

class CourseChapter(models.Model):
    """ Разделы курса учебного предмета """
    course = models.ForeignKey('syllabus.Course', verbose_name=_("Курс"), on_delete=models.CASCADE, related_name="chapters")
    number = models.PositiveIntegerField(verbose_name=_("Номер"), default=1)
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=0)
    unit = models.ForeignKey('ibo.UnitPlanerBaseModel', verbose_name=_("Юнит"), on_delete=models.SET_NULL, null=True, blank=True, related_name="course_chapters")
    class Meta:
        verbose_name = 'Раздел курса'
        verbose_name_plural = 'Разделы курса'
        ordering = ['course', 'number']
    def __str__(self):
        return f"{self.course}: {self.number}. {self.name}"
    
class CourseTopic(models.Model):
    """ Темы курса учебного предмета """
    chapter = models.ForeignKey('syllabus.CourseChapter', verbose_name=_("Раздел"), on_delete=models.CASCADE, null=True, related_name="topics")
    number = models.PositiveIntegerField(verbose_name=_("Номер"), default=1)
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=1)
    class Meta:
        verbose_name = 'Тема курса'
        verbose_name_plural = 'Темы курса'
        ordering = ['chapter', 'number']
    def __str__(self):
        return f"{self.chapter}: {self.number}. {self.name}"