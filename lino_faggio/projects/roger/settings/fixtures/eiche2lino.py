# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Custom-specific script to import data into :ref:`faggio`
from an .xls file. To be invoked using something like::

  python manage.py run /path/lino/blog/2013/1002.py Input_file.xls
  


"""

from __future__ import unicode_literals

import os

import logging
logger = logging.getLogger(__name__)


import sys

from dateutil.parser import parse as parse_date

from lino.utils import iif
from lino.utils import IncompleteDate
from xlrd import open_workbook, xldate_as_tuple

from lino.modlib.contacts.utils import street2kw

from lino.runtime import *
from lino import dd, rt
from djangosite.dbutils import is_valid_email


def string2date(s):
    return parse_date(s, fuzzy=True)


class MyBook():

    column_headers = """
    Nr.
    Titel
    Name
    Vorname
    Strasse
    PLZ
    Ort
    -
    Handy
    GEBURTSTAG
    BEZ.
    Datum
    -
    COK-MG
    E-Mail
    """.split()
    column_headers = [iif(x == '-', '', x) for x in column_headers]

    def date_converter(self, v):
        if not v:
            return None
        if isinstance(v, basestring):
            v = string2date(v)
            return IncompleteDate.from_date(v)
            #~ return v
        t = xldate_as_tuple(v, self.book.datemode)
        assert len(t) == 6
        t = t[:3]
        #~ print t
        return IncompleteDate(*t)

    def row2instance(self, nr, title, last_name, first_name, street, zip_code, city_name, phone, gsm, birth_date, bez, datum, mg, mgnr, email):
        kw = dict(last_name=last_name, first_name=first_name)
        if nr:
            kw.update(id=1000 + int(nr))
        kw.update(phone=phone)
        kw.update(gsm=gsm)
        try:
            kw.update(zip_code=str(int(zip_code)))
        except ValueError as e:
            kw.update(zip_code=zip_code)

        if email:
            if isinstance(email, basestring) and is_valid_email(email):
                kw.update(email=email)
            else:
                logger.warning("Ignored invalid email address %r", email)
        #~ kw.update(street=street)

        #~ kw.update(pupil_type=mg)

        kw.update(street2kw(street))

        if title == "Herr":
            kw.update(gender=mixins.Genders.male)
        elif title == "Frau":
            kw.update(gender=mixins.Genders.female)
        elif title:
            kw.update(title=title)
        city_name = city_name.strip()
        if city_name:
            #~ countries.Place.objects.get(name)
            kw.update(city=countries.Place.lookup_or_create(
                'name', city_name, country=self.country))
        #~ print birth_date
        kw.update(birth_date=self.date_converter(birth_date))
        return courses.Pupil(**kw)

    def __init__(self, filename):
        self.filename = filename

    def objects(self):
        self.country = countries.Country.objects.get(isocode="BE")
        self.book = open_workbook(self.filename)
        s = self.book.sheet_by_index(0)
        #~ print 'Sheet:',s.name
        found = False
        ncols = len(self.column_headers)
        for row in range(s.nrows):
            values = [s.cell(row, col).value for col in range(ncols)]
            if found:
                obj = self.row2instance(*values)
                obj.full_clean()
                obj.save()
                logger.info("%s has been saved", obj)
                yield obj
            elif values == self.column_headers:
                found = True
            elif row < 5:
                print "Ignored line %s" % values


def objects():

    # this wil create rooms and calendars :
    from lino_faggio.fixtures.faggio import Loader1
    yield Loader1().objects()

    # this will create subscriptions for each user and calendar
    # from lino.modlib.cal.fixtures.demo2 import subscribe_all
    # yield subscribe_all()

    if False:
        users.User.objects.all().delete()
        courses.Enrolment.objects.all().delete()
        cal.Event.objects.all().delete()
        courses.Course.objects.all().delete()
        courses.Teacher.objects.all().delete()
        courses.Pupil.objects.all().delete()
        courses.Course.objects.all().delete()
        sales.Invoice.objects.all().delete()
        ledger.AccountInvoice.objects.all().delete()
        ledger.Movement.objects.all().delete()
        finan.BankStatement.objects.all().delete()
        finan.PaymentOrder.objects.all().delete()

        keep_ids = set((settings.SITE.site_config.site_company.pk,))
        for r in cal.Room.objects.filter(company__isnull=False):
            keep_ids.add(r.company.pk)
        contacts.Company.objects.exclude(id__in=keep_ids).delete()
        contacts.Person.objects.exclude(id__in=keep_ids).delete()
        contacts.Partner.objects.exclude(id__in=keep_ids).delete()

        settings.SITE.site_config.next_partner_id = 1
        settings.SITE.site_config.save()
        eiche = contacts.Company(name="Die Eiche", language="de")
        eiche.save()
        settings.SITE.site_config.site_company = eiche
        settings.SITE.site_config.save()

    p = settings.SITE.legacy_data_path or settings.SITE.project_dir
    book = MyBook(os.path.join(p, "Eiche 2013.xls"))
    yield book.objects()
