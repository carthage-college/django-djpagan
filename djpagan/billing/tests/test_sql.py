from django.conf import settings
from django.test import TestCase
from django_webtest import WebTest
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from djpagan.billing.sql import ALL_TRANSACTIONS
from djpagan.billing.sql import BRIDGED_CLASSES
from djpagan.billing.sql import BRIDGED_CLASSES_STUDENTS
from djpagan.billing.sql import CHEQUE_NUMBER
from djpagan.billing.sql import JOURNAL_TRANSACTIONS
from djpagan.billing.sql import JOURNAL_TYPES
from djpagan.core.utils import get_objects

from djtools.fields import TODAY

STATUS = settings.VOID_STATUS


class CoreSQLTestCase(TestCase):

    def test_journal_types_sql(self):

        objects = get_objects(JOURNAL_TYPES)
        self.assertGreaterEqual(len(objects), 1)

    def test_journal_transactions_sql(self):

        sql = JOURNAL_TRANSACTIONS(
            vch_ref = settings.TEST_JOURNAL_TYPE,
            journal_no = settings.TEST_JOURNAL_NUMBER,
            stat = STATUS
        )

        objects = get_objects(sql)
        self.assertGreaterEqual(len(objects), 1)

    def test_bridged_classes_sql(self):

        course_no = settings.TEST_BRIDGED_COURSE_NUMBER

        bridged = get_objects(
            BRIDGED_CLASSES(
                year = TODAY.year - 2,
                course_no = 'AND crs_rec.crs_no="{}"'.format(course_no)
            )
        )
        self.assertGreaterEqual(len(bridged), 1)

        sql = BRIDGED_CLASSES_STUDENTS(
            year = bridged[0].yr, course_no = course_no,
            a_sess = bridged[0].a_sess, b_sess = bridged[0].b_sess
        )

        objects = get_objects(sql)
        self.assertGreaterEqual(len(objects), 1)

    def test_all_student_transactions_sql(self):

        sql = ALL_TRANSACTIONS(
            student_id = settings.TEST_STUDENT_ID,
            stat = STATUS
        )

        objects = get_objects(sql)
        self.assertGreaterEqual(len(objects), 1)

    def test_cheque_number_sql(self):

        sql = CHEQUE_NUMBER(
            stat = STATUS,
            cheque_number = settings.TEST_CHEQUE_NUMBER
        )

        objects = get_objects(sql)
        self.assertGreaterEqual(len(objects), 1)

