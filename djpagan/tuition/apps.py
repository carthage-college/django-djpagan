# -*- coding: utf-8 -*-

from django.apps import AppConfig


class RemissionConfig(AppConfig):
    """Mostly used for the signal infrastructure."""

    name = 'djpagan.tuition'
    verbose_name = 'Tuition Remission'

    def ready(self):
        import djpagan.tuition.signals
