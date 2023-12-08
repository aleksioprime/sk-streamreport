from django.db import models
from django.utils.translation import gettext_lazy as _

class EventParticipation(models.Model):
    """ Участие в мероприятиях """
    student = models.ForeignKey('general.User', verbose_name=_("Студент"), on_delete=models.CASCADE, related_name="student_events")
    group = models.ForeignKey('general.ClassGroup', verbose_name=_("Класс"), on_delete=models.SET_NULL, null=True, related_name="events")
    author = models.ForeignKey('general.User', verbose_name=_("Автор"), on_delete=models.SET_NULL, null=True, related_name="author_events")
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    result = models.TextField(verbose_name=_("Результаты"), null=True, blank=True)
    date_start = models.DateField(verbose_name=_("Дата начала"), null=True)
    date_end = models.DateField(verbose_name=_("Дата окончания"), null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Создан"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Изменён"))
    class Meta:
        verbose_name = 'Участие в мероприятиях'
        verbose_name_plural = 'Участия в мероприятиях'
        ordering = ['group', 'student', 'title']
    def __str__(self):
        return f"{self.title}"
