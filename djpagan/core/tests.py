from django.conf import settings
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

USERNAME = settings.TEST_USERNAME
PASSWORD = settings.TEST_PASSWORD


class CoreViewsTestCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': USERNAME,
            'password': PASSWORD
        }

    def test_signin(self):
        print "cred:"
        print self.credentials
        # attempt to sign in
        signin = self.client.post(
            reverse('auth_login'),
            self.credentials, follow=True
        )
        print reverse('auth_login')
        print "status code: {}".format(signin.status_code)
        print "post login status = {}".format(signin.context['user'].is_active)

        session = self.client.session
        print session

        login = self.client.login(username=USERNAME, password=PASSWORD)
        print "client login status = {}".format(login)

    def test_home(self):
        # get home page
        response = self.client.get(reverse('home'))
        # redirect to sign in page
        self.assertEqual(response.status_code, 302)
        print "status code: {}".format(response.status_code)
        print "redirect to sign in at {}".format(response['location'])

        # attempt to sign in with post
        signin = self.client.post(
            response['location'],
            self.credentials, follow=True
        )
        print "status code: {}".format(signin.status_code)
        #self.assertTrue(signin.context['user'].is_active)
        #self.assertEqual(str(signin.context['user']), USERNAME)
        print "user = {}".format(signin.context['user'])
        # attempt to sign in with client login method
        login = self.client.login(username=USERNAME, password=PASSWORD)
        print login
        #self.assertTrue(login)
        home = self.client.get(reverse('home'))
        print "home page content:"
        print home['location']
        print "{}".format(home.content)
