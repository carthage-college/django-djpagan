from django.conf import settings
from django.test import TestCase
from django_webtest import WebTest
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from djpagan.core.sql import MOST_RECENT_TERM
from djpagan.core.utils import get_objects

from djtools.utils.logging import seperator


class CoreSQLTestCase(TestCase):

    def setUp(self):
        pass

    def test_most_recent_term_sql(self):

        sid = settings.TEST_STUDENT_ID

        sql = MOST_RECENT_TERM(
            student_number = sid
        )
        student = get_objects(sql)

        self.assertEqual(
            student[0].id, sid
        )
