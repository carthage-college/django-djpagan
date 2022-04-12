# -*- coding: utf-8 -*-

"""Data models."""

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


LOCATION_CHOICES = (
    ('Reggie 1', 'Reggie 1'),
    ('Reggie 2', 'Reggie 2'),
    ('Reggie 3', 'Reggie 3'),
)


class MealPlan(models.Model):
    """Mean Plan Data."""

    user = models.ForeignKey(
        User,
        related_name='student',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    level = models.CharField(max_length=128)
    status = models.BooleanField(
        verbose_name='Is the plan active?',
        default=True,
    )
    location = models.CharField(
        max_length=128,
        choices=LOCATION_CHOICES,
    )

    class Meta:
        """Information about the data class model."""

        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self):
        """Default data for display."""
        return "{0}, {1} ({2}): {3}".format(
            self.user.last_name,
            self.user.first_name,
            self.user.username,
            self.user.id,
        )

    def get_absolute_url(self):
        """Returns the FQDN URL."""
        return 'https://{0}{1}'.format(
            settings.SERVER_URL,
            reverse('admin:forage_mealplan_change', args=(self.id,)),
        )
