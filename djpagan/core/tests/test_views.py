from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from djpagan.core.sql import ACCOUNT_NOTES
from djpagan.core.sql import PROGRAM_ENROLLMENT
from djpagan.core.sql import SESSION_DETAILS
from djpagan.core.sql import SUBSIDIARY_BALANCES
from djpagan.core.utils import create_test_user, get_objects

from djtools.utils.logging import seperator

from djzbar.utils.informix import get_session


class CoreViewsTestCase(TestCase):

    def setUp(self):

        self.sid = settings.TEST_STUDENT_ID
        self.earl = settings.INFORMIX_EARL
        self.user = create_test_user()

    def test_home(self):
        print("\n")
        print("Home Page")
        seperator()
        earl = reverse('home')
        print(earl)
        # get home page
        response = self.client.get(earl)
        self.assertEqual(response.status_code, 302)
        # redirect to sign in page
        print("redirect to sign in at {}".format(response['location']))

        # attempt to sign in with client login method
        login = self.client.login(
            username=self.username, password=self.password
        )
        self.assertTrue(login)
        response = self.client.get(earl)
        self.assertEqual(response.status_code, 200)

    def test_student_detail(self):
        print("\n")
        print("Student Detail")
        sid = settings.TEST_STUDENT_ID
        seperator()
        earl = reverse('student_detail', args=[sid])
        # get page
        response = self.client.get(earl, follow=True)
        self.assertEqual(response.status_code, 200)

        # attempt to sign in with client login method
        login = self.client.login(
            username=self.username, password=self.password
        )
        self.assertTrue(login)
        response = self.client.get(earl)
        self.assertEqual(response.status_code, 200)

        student = self.client.post(
            earl, {'student_number': sid}
        )

        enrollment = get_objects(PROGRAM_ENROLLMENT(student_number=sid), True)
        balances = get_objects(SUBSIDIARY_BALANCES(student_number=sid), True)
        notes = get_objects(ACCOUNT_NOTES(student_number=sid), True)

        session = get_session(self.earl)

        sql = SESSION_DETAILS(
            student_number = self.sid,
            start_date = settings.ORDERED_TERMS_START_DATE
        )

        details = session.execute(sql).first()

        self.assertEqual(enrollment.id, sid)
        self.assertEqual(balances.id, sid)
        if notes:
            self.assertEqual(notes.id, sid)
        self.assertEqual(details.id, sid)

