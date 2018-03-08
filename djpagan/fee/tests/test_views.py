from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import Group

from djpagan.core.utils import create_test_user
from djpagan.fee.sql import LATEST_TERM_TEMP
from djpagan.fee.sql import ORDERED_TERMS_TEMP
from djpagan.fee.sql import STUDENT_BALANCE_LATE_FEE

from djzbar.utils.informix import get_session
from djtools.utils.logging import seperator


class FeeViewsTestCase(TestCase):

    def setUp(self):

        self.sid = settings.TEST_STUDENT_ID
        self.earl = settings.INFORMIX_EARL
        self.user = create_test_user()
        self.password = settings.TEST_PASSWORD


    def test_student_balance_late_fee(self):
        print("\n")
        print("Student balance late fee")
        sid = settings.TEST_STUDENT_ID
        seperator()
        earl = reverse_lazy('student_balance_late_fee')
        # get page
        response = self.client.get(earl, follow=True)
        self.assertEqual(response.status_code, 200)

        # attempt to sign in with client login method
        login = self.client.login(
            username=self.user.username, password=self.password
        )
        self.assertTrue(login)
        response = self.client.get(earl)
        self.assertEqual(response.status_code, 200)

        student = self.client.post(
            earl, {'student_number': sid}
        )

        # create database session connection
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
