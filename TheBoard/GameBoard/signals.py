from django.db.models.signals import *
from django.dispatch import receiver
from django.core.mail import *
from .views import *


@receiver(post_save, sender=Comment)
def send_comment_to_email(created, instance, *args, **kwargs):
    if created:
        post_author = instance.post.author #к чьему посту пишем коммент
        subject = f'{post_author}'
        comment_user = instance.author #кто пишет коммент
        post_author_email = instance.post.author.email #кому шлем эмейл

        send_mail(
            subject=subject,
            message=f"Прветствуем, {post_author}\n"
                    f"Появился новый комментарий под Вашим постом\n"
                    f"от - {comment_user}\n",
            from_email='',
            recipient_list=[post_author_email])