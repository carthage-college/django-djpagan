from django.conf import settings
from django.test import TestCase
from django_webtest import WebTest
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from djpagan.fee.sql import LATEST_TERM_TEMP
from djpagan.fee.sql import ORDERED_TERMS_TEMP
from djpagan.fee.sql import STUDENT_BALANCE_LATE_FEE

from djzbar.utils.informix import get_session


class FeeSQLTestCase(TestCase):

    def setUp(self):
        self.sid = settings.TEST_STUDENT_ID
        self.lastname = settings.TEST_STUDENT_LASTNAME
        self.earl = settings.INFORMIX_EARL

    def test_student_balance_late_fee_sql(self):

        session = get_session(self.earl)

        # ordered terms temp table
        sql = ORDERED_TERMS_TEMP(
            start_date = settings.ORDERED_TERMS_START_DATE
        )
        session.execute(sql)

        # latest terms temp table
        sql = LATEST_TERM_TEMP
        session.execute(sql)

        # student balance late fee
        sql = STUDENT_BALANCE_LATE_FEE(
            student_number = self.sid
        )
        student = session.execute(sql).first()

        self.assertEqual(
            student.id, self.sid
        )

        session.close()

        print student
