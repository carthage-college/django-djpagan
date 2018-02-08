from django.conf import settings

from djzbar.utils.informix import do_sql

from djpagan.billing.sql import JOURNAL_TYPES

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
