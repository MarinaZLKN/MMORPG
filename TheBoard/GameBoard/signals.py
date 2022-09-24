from django.db.models.signals import *
from django.dispatch import receiver
from django.core.mail import *
from django.template.loader import render_to_string
from .views import *


@receiver(post_save, sender=Comment)
def notify_users(created, instance, *args, **kwargs):
    print('Что у нас здесь', created, instance.is_accepted)
    if instance.is_accepted:
        print('Нажали на кнопку')
        send_reply_to_email(created, instance)
    if created:
        print('Создали коммент')
        send_comment_to_email(created, instance)


def send_comment_to_email(created, instance):
    post_author = instance.post.author
    html = render_to_string(
        'new_comment.html',
        {
            'post_author': post_author,
            'comment': instance,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Hello, {instance.post.author}',
        from_email='',
        to=[post_author.email]
    )
    msg.attach_alternative(html, 'text/html')
    msg.send()


def send_reply_to_email(created, instance):
    author = instance.author
    html = render_to_string(
        'reply.html',
        {
            'author': author,
            'comment': instance,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Hello',
        from_email='',
        to=[author.email]
    )
    msg.attach_alternative(html, 'text/html')
    msg.send()













