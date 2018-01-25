from django.conf import settings

from djzbar.utils.informix import do_sql

from djpagan.billing.sql import JOURNAL_TYPES

DEBUG = settings.INFORMIX_DEBUG


def get_objects(sql):

    objects = do_sql(sql, key=DEBUG)
    if objects:
         objects = objects.fetchall()

    return objects
