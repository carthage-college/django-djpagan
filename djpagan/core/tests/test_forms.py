from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from djpagan.core.forms import MostRecentTermForm

from djtools.utils.logging import seperator


class CoreFormsTestCase(TestCase):

    def setUp(self):
        pass

    def test_most_recent_term_valid_data(self):
        form = MostRecentTermForm({
            'student_number': settings.TEST_STUDENT_ID,
        })
        self.assertTrue(form.is_valid())

    def test_most_recent_term_invalid_data(self):
        form = MostRecentTermForm({
            'student_number': '1234568-9',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'student_number': ['Enter a whole number.'],
        })

    def test_most_recent_term_blank_data(self):
        form = MostRecentTermForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'student_number': ['This field is required.'],
        })

