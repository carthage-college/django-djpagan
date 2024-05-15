# -*- coding: utf-8 -*-

"""Signals for various events."""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from djpagan.tuition.models import Remission
from djtools.utils.mail import send_mail


@receiver(post_save, sender=Remission)
def remission_post_save_notify_approved(sender, **kwargs):
    """Send an email to the bean counters when approved."""
    remission = kwargs['instance']

    if remission.approved and not remission.approved_email:
        to_list = settings.TUITION_REMISSION_APPROVED_LIST
        if settings.DEBUG:
            remission.to_list = to_list
            to_list = [settings.MANAGERS[0][1]]

        subject = "[Tuition Remission] Approved: '{0}', {1}".format(
            remission.user.last_name, remission.user.first_name,
        )
        frum = settings.SERVER_MAIL
        sent = send_mail(
            kwargs.get('request'),
            to_list,
            subject,
            frum,
            'tuition/remission/email_approved.html',
            remission,
            reply_to=[frum,],
            [settings.MANAGERS[0][1]],
        )
        if sent:
            remission.approved_email = True
            remission.save()
