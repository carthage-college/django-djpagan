from django.conf import settings
from django.contrib.auth.models import Group, User

from djzbar.utils.informix import do_sql

DEBUG = settings.INFORMIX_DEBUG


def get_objects(sql, sid=None):

    objects = do_sql(sql, key=DEBUG)
    if objects:
        objects = objects.fetchall()
        if sid:
            try:
                objects = objects[0]
            except:
                objects = None

    return objects


def create_test_user():

    user = User.objects.create_user(
        settings.TEST_USERNAME,
        settings.TEST_EMAIL,
        settings.TEST_PASSWORD
    )

    # add to student accounts group
    sa = Group.objects.create(name=settings.MANAGER_GROUP)
    sa.user_set.add(user)

    return user
