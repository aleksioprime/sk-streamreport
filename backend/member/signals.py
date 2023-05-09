from member.models import User, ProfileStudent, ProfileTeacher
from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=ProfileStudent)
def delete_student_profile(instance, **kwargs):
    User.objects.filter(pk=instance.user.pk).delete()
@receiver(post_delete, sender=ProfileTeacher)
def delete_student_profile(instance, **kwargs):
    User.objects.filter(pk=instance.user.pk).delete()