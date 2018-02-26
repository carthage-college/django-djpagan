from django.conf import settings
from django.test import TestCase
from django_webtest import WebTest
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from djpagan.core.sql import ACCOUNT_NOTES
from djpagan.core.sql import PROGRAM_ENROLLMENT
from djpagan.core.sql import SESSION_DETAILS
from djpagan.core.sql import SEARCH_STUDENTS
from djpagan.core.sql import SUBSIDIARY_BALANCES
from djpagan.core.utils import get_objects

from djtools.utils.logging import seperator

from djzbar.utils.informix import get_session


class CoreSQLTestCase(TestCase):

    def setUp(self):
        self.sid = settings.TEST_STUDENT_ID
        self.lastname = settings.TEST_STUDENT_LASTNAME
        self.earl = settings.INFORMIX_EARL

    def test_search_students_lastname_sql(self):

        lastname = self.lastname
        try:
            sid = int(lastname)
        except:
            sql = SEARCH_STUDENTS(
                lastname = lastname
            )
            students = get_objects(sql)

        for s in students:
            self.assertEqual(
                s['lastname'], lastname
            )

    def test_session_detail_sql(self):

        session = get_session(self.earl)

        sql = SESSION_DETAILS(
            student_number = self.sid,
            start_date = settings.ORDERED_TERMS_START_DATE
        )

        details = session.execute(sql).first()

        self.assertEqual(
            details.id, self.sid
        )

    def test_program_enrollment_sql(self):

        sql = PROGRAM_ENROLLMENT(
            student_number = self.sid
        )
        enrollment = get_objects(sql, True)

        self.assertEqual(
            enrollment.id, self.sid
        )

    def test_account_notes_sql(self):

        sql = ACCOUNT_NOTES(
            student_number = self.sid
        )
        notes = get_objects(sql, True)

        if notes:
            self.assertEqual(
                notes.id, self.sid
            )

    def test_subsidiary_balances_sql(self):

        sql = SUBSIDIARY_BALANCES(
            student_number = self.sid
        )
        balances = get_objects(sql, True)

        self.assertEqual(
            balances.id, self.sid
        )

