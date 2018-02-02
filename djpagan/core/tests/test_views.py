from django.conf import settings
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

from djtools.utils.logging import seperator


class CoreViewsTestCase(TestCase):

    def setUp(self):

        self.username = settings.TEST_USERNAME
        self.email = settings.TEST_EMAIL
        self.password = settings.TEST_PASSWORD
        self.user = User.objects.create_user(
            self.username, self.email, self.password
        )

        # add to student accounts group
        sa = Group.objects.create(name=settings.MANAGER_GROUP)
        sa.user_set.add(self.user)
        # cred dict
        self.credentials = {
            'username': self.username,
            'password': self.password
        }

    def test_home(self):
        print "\n"
        print "Home Page"
        seperator()
        earl = reverse('home')
        print earl
        # get home page
        response = self.client.get(earl)
        self.assertEqual(response.status_code, 302)
        # redirect to sign in page
        print "redirect to sign in at {}".format(response['location'])

        # attempt to sign in with client login method
        login = self.client.login(
            username=self.username, password=self.password
        )
        self.assertTrue(login)
        response = self.client.get(earl)
        self.assertEqual(response.status_code, 200)
        #print "{}".format(home.content)

    def test_most_recent_term(self):
        print "\n"
        print "Most Recent Term"
        seperator()
        earl = reverse('most_recent_term')
        print earl
        # get page
        response = self.client.get(earl, follow=True)
        print "redirect chain".format(response.redirect_chain)
        print "status code: {}".format(response.status_code)
        self.assertEqual(response.status_code, 200)

        # attempt to sign in with client login method
        login = self.client.login(
            username=self.username, password=self.password
        )
        self.assertTrue(login)
        response = self.client.get(earl)
        self.assertEqual(response.status_code, 200)

        sid = settings.TEST_STUDENT_ID
        student = self.client.post(
            earl, {'student_number': sid}
        )

        print "status code: {}".format(student.status_code)
        print "user ID: {}".format(student.context['user'].id)
        print "rendered form:\n"
        print student.context['form']
        print "student data:\n"
        print student.context['student']

        #session = self.client.session
        #print session

        self.assertEqual(student.context['student'][0].id, sid)
