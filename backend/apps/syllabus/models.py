from django.db import models
from django.utils.translation import gettext_lazy as _

class Course(models.Model):
    """ Полный курс учебного предмета """
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.CASCADE, null=True, related_name="courses")
    years = models.ManyToManyField('general.StudyYear', verbose_name=_("Параллели"), blank=True, related_name="courses")
    file = models.FileField(upload_to='courses/', verbose_name=_("Файл рабочей программы"))
    class Meta:
        verbose_name = 'Курс предмета: полный'
        verbose_name_plural = 'Курсы предмета: полные'
        ordering = ['subject']
    def __str__(self):
        return f"{self.subject}"
    
class CourseSection(models.Model):
    """ Годовой курс учебного предмета """
    course = models.ForeignKey('syllabus.Course', verbose_name=_("Предмет"), on_delete=models.CASCADE, related_name="course_sections")
    year = models.ForeignKey('general.StudyYear', verbose_name=_("Класс"), on_delete=models.SET_NULL, null=True, blank=True, related_name="course_sections")
    unit_pyp = models.ForeignKey('pyp.PypUnitPlanner', verbose_name=_("Юнит PYP"), on_delete=models.SET_NULL, null=True, blank=True, related_name="course_sections")
    unit_myp = models.ForeignKey('myp.MypUnitPlanner', verbose_name=_("Юнит MYP"), on_delete=models.SET_NULL, null=True, blank=True, related_name="course_sections")
    unit_dp = models.ForeignKey('dp.DpUnitPlanner', verbose_name=_("Юнит DP"), on_delete=models.SET_NULL, null=True, blank=True, related_name="course_sections")
    class Meta:
        verbose_name = 'Раздел курса'
        verbose_name_plural = 'Разделы курса'
        ordering = ['course', 'year']
    def __str__(self):
        return f"{self.course} ({self.year})"
    
class CourseTopic(models.Model):
    """ Темы курса """
    section = models.ForeignKey('syllabus.CourseSection', verbose_name=_("Предмет"), on_delete=models.CASCADE, related_name="topics")
    number = models.PositiveIntegerField(verbose_name=_("Номер"), default=1)
    name = models.CharField(max_length=255, verbose_name=_("Тема"))
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=0)
    class Meta:
        verbose_name = 'Тема курса'
        verbose_name_plural = 'Темы курса'
        ordering = ['section', 'number']
    def __str__(self):
        return f"{self.section}: {self.number}. {self.name}"