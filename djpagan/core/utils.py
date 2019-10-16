from django.conf import settings
from django.contrib.auth.models import Group, User

from djimix.core.database import get_connection, xsql


def get_objects(sql, sid=None):

    connection = get_connection()
    # automatically closes the connection after leaving 'with' block
    with connection:
        objects = xsql(sql, connection, settings.INFORMIX_DEBUG)
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
