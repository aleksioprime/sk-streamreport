from django.db import models
from django.utils.translation import gettext_lazy as _

class UnitReflectionChoices(models.TextChoices):
        teacher = "teacher", "Рефлексия учителя"
        students = "students", "Рефлексия студентов"
        assessment = "assessment", "Рефлексия оценивания"
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
    category = models.ForeignKey('ibo.AtlCategory', verbose_name=_("Категория ATL"), on_delete=models.CASCADE, related_name="clusters")
    class Meta:
        verbose_name = 'IB: ATL кластер'
        verbose_name_plural = 'IB: ATL кластеры'
        ordering = ['category', 'id']
    def __str__(self):
        return "{} ({})".format(self.name, self.category)


# TODO: Подумать над добавлением фотоальбома в юнит (загрузка и хранение нескольких фотографий в одном поле через связанную таблицу)
# TODO: Подумать над добавлением набора файлов в юнит (загрузка и хранение нескольких файлов в одном поле через связанную таблицу)
class UnitPlanerBaseModel(models.Model):
    """ Общая модель юнитов """
    title = models.CharField(max_length=255, verbose_name=_("Название юнита"))
    order = models.PositiveSmallIntegerField(verbose_name=_("Номер"), default=0)
    teachers = models.ManyToManyField('general.User', verbose_name=_("Учителя"), related_name="teacher_unitplans")
    authors = models.ManyToManyField('general.User', verbose_name=_("Авторы"), through='ibo.UnitTeacherRoles', related_name="author_unitplans")
    year = models.ForeignKey('general.StudyYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, related_name="unitplans")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=0)
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Создан"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Изменён"))
    class Meta:
        verbose_name = 'UnitPlan'
        verbose_name_plural = 'UnitPlans'
        ordering = ['year', 'order']
    def __str__(self):
        return f''
    
class UnitTeacherRoles(models.Model):
    """ Роли авторов юнита PYP """
    unit = models.ForeignKey('ibo.UnitPlanerBaseModel', verbose_name=_("Юнит"), on_delete=models.CASCADE, related_name="teacher_roles")
    user = models.ForeignKey('general.User', verbose_name=_("Пользователь"), on_delete=models.CASCADE, related_name="unit_roles")
    role = models.CharField(max_length=32, verbose_name=_("Роль"), blank=True, null=True)
    class Meta:
        verbose_name = 'UnitPlan: Роль автора юнита'
        verbose_name_plural = 'UnitPlan: Роли автора юнита'
        ordering = ['unit', 'user', 'role']
    def __str__(self):
        return f"{self.user} ({self.role})"

class IbProfileDevelop(models.Model):
    """ Качества портрета студента в юните """
    profile = models.ForeignKey('ibo.LearnerProfile', verbose_name=_("Профиль студента"), on_delete=models.CASCADE, related_name="units")
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    unit = models.ForeignKey('ibo.UnitPlanerBaseModel', verbose_name=_("Юнит PYP"), on_delete=models.CASCADE, related_name="ibprofiles")
    class Meta:
        verbose_name = 'UnitPlan: Развитие профиля студента'
        verbose_name_plural = 'UnitPlans: Развитие профиля студента'
        ordering = ['unit', 'profile']
    def __str__(self):
        return f"{self.profile}"
    
class UnitReflectionPost(models.Model):
    """ Посты рефлексии по юниту """
    post = models.TextField(verbose_name=_("Пост"), null=True, blank=True)
    type = models.CharField(choices=UnitReflectionChoices.choices, verbose_name=_("Type"), max_length=12)
    author = models.ForeignKey('general.User', verbose_name=_("Автор"), on_delete=models.SET_NULL, null=True, related_name="author_reflections")
    unit = models.ForeignKey('ibo.UnitPlanerBaseModel', verbose_name=_("Юнит DP"), on_delete=models.CASCADE, related_name="reflection_posts")
    class Meta:
        verbose_name = 'UnitPlan: Пост рефлексии'
        verbose_name_plural = 'UnitPlans: Посты рефлексии'
        ordering = ['unit', 'type', 'post']
    def __str__(self):
        return f"{self.type}: {self.post[:15]}"