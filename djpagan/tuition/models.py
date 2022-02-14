# -*- coding: utf-8 -*-

"""Data models."""

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from djtools.fields import BINARY_CHOICES
from taggit.managers import TaggableManager


RELATIONSHIP_CHOICES = (
    ('', '--select--'),
    ('Self', 'Self'),
    ('Spouse', 'Spouse'),
    ('Domestic Partner', 'Domestic Partner'),
    ('Dependent Child', 'Dependent Child'),
)
DEGREE_CHOICES = (
    ('', '--select--'),
    ('Bachelor', 'Bachelor'),
    ("Master's in Education", "Master's in Education"),
    ('Teaching Certification', 'Teaching Certification'),
    ('Non-Degree Seeking', 'Non-Degree Seeking'),
)
ENROLLMENT_CHOICES = (
    ('', '--select--'),
    ('Full-time', 'Full-time'),
    ('At least half-time', 'At least half-time'),
    ('Less than half-time', 'Less than half-time'),
)
ACADEMIC_YEARS = [
    (('{0}-{1}'.format(year, year + 1)), ('{0}-{1}'.format(year, year + 1)))
    for year in range(datetime.date.today().year, datetime.date.today().year + 10)
]
ACADEMIC_YEARS.insert(0, ('', '---select---'))
CLASSIFICATION_CHOICES = (
    ('', '--select--'),
    ('First Time Freshman', 'First Time Freshman'),
    ('Transfer', 'Transfer'),
    ('Returning', 'Returning'),
    ('Graduate', 'Graduate'),
    ('Non-Degree Seeking', 'Non-Degree Seeking'),
)


class GenericChoice(models.Model):
    """For making choices for select fields in forms."""

    name = models.CharField(unique=True, max_length=255)
    value = models.CharField(max_length=255)
    ranking = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text='A number from 0 to 999 to rank the position in a list.',
    )
    active = models.BooleanField(
        help_text='Do you want the field to be visable on your form?',
        verbose_name='Is active?',
        default=True,
    )
    tags = TaggableManager()

    def __str__(self):
        return self.name

    def tag_list(self):
        return ', '.join(o.name for o in self.tags.all())

    class Meta:
        ordering = ['ranking']


class Remission(models.Model):
    """Tuition assistance data class model."""

    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
    )
    updated_by = models.ForeignKey(
        User,
        related_name='updated_by',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Date Updated", auto_now=True)
    approved = models.BooleanField(default=False, verbose_name="Approved")
    percentage = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text='Percentage for Tuition Remission.',
    )
    approved_email = models.BooleanField(
        default=False,
        verbose_name="Approved email sent",
        editable=settings.DEBUG,
    )
    income = models.CharField(
        "Is the employee's adjusted gross income greater than 60,000?",
        max_length=4,
        choices=BINARY_CHOICES,
        help_text="If no, the employee will be required to complete a FAFSA.",
    )
    first_name = models.CharField("Student's First Name", max_length=128)
    middle_initital = models.CharField("Student's Middle Initial", max_length=1)
    last_name = models.CharField("Student's Last Name", max_length=128)
    sid = models.CharField("Student ID Number (if applicable)", max_length=16)
    relationship = models.CharField(max_length=128, choices=RELATIONSHIP_CHOICES)
    phone = models.CharField("Student Phone Number", max_length=12)
    email = models.EmailField("Student Email")
    address = models.TextField(
        "Student Address",
        help_text="Street, apartment number if applicable, city, state, postal code.",
    )
    dob = models.DateField("Student Birthday", help_text="MM/DD/YYYY")
    degree = models.CharField(
        "Degree Seeking",
        max_length=128,
        choices=DEGREE_CHOICES,
    )
    enrollment = models.CharField(max_length=128, choices=ENROLLMENT_CHOICES)
    academic_year = models.CharField(
        "Application Year",
        max_length=128,
        choices=ACADEMIC_YEARS,
    )
    assistance = models.ManyToManyField(
        GenericChoice,
        verbose_name='Student is applying as',
        related_name='assistance',
        help_text="Check all that apply",
    )
    classification = models.CharField(
        "Student is",
        max_length=128,
        choices=CLASSIFICATION_CHOICES,
    )
    schools = models.TextField(
        "List the schools to which the student has applied for admission.",
        help_text="""
            Note: Carthage will not submit application for ELCA or
            Tuition Exchange scholarships until a student has applied to that
            institution for admission.
        """,
    )
    comments = models.TextField(null=True, blank=True)

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
            reverse('admin:tuition_remission_change', args=(self.id,)),
        )
