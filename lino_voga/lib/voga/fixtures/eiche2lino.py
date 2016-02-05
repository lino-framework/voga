# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Custom-specific script to import data into :ref:`voga`
from an .xls file. To be invoked using something like::

  python manage.py run /path/to/this/file.py Input_file.xls
  


"""

from __future__ import unicode_literals

import os

import logging
logger = logging.getLogger(__name__)

from dateutil.parser import parse as parse_date

from lino.utils import iif
from lino.utils import IncompleteDate
from xlrd import open_workbook, xldate_as_tuple
from xlrd.xldate import XLDateError

from lino.modlib.contacts.utils import street2kw

from lino.api.shell import *
from lino.api import dd
from lino.core.utils import is_valid_email


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
        try:
            t = xldate_as_tuple(v, self.book.datemode or 0)
        except XLDateError as e:
            logger.info("Failed to read date %s : %s", v, e)
            return None
        assert len(t) == 6
        t = t[:3]
        return IncompleteDate(*t)

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
                logger.info("%s (%s) has been saved", obj, obj.birth_date)
                yield obj
            elif values == self.column_headers:
                found = True
            elif row < 5:
                logger.info("Ignored line %s (waiting for %s)",
                            values, self.column_headers)

    def row2instance(self, nr, title, last_name, first_name, street,
                     zip_code, city_name, phone, gsm, birth_date, bez, datum,
                     mg, mgnr, email):
        kw = dict(last_name=last_name, first_name=first_name)
        if nr:
            kw.update(id=1000 + int(nr))
        kw.update(phone=phone)
        kw.update(gsm=gsm)
        try:
            kw.update(zip_code=str(int(zip_code)))
        except ValueError:
            kw.update(zip_code=zip_code)

        if email:
            if isinstance(email, basestring) and is_valid_email(email):
                kw.update(email=email)
            else:
                logger.warning("Ignored invalid email address %r", email)

        kw.update(street2kw(street))

        if title == "Herr":
            kw.update(gender=dd.Genders.male)
        elif title == "Frau":
            kw.update(gender=dd.Genders.female)
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


class MyBook2016(MyBook):

    column_headers = [
    "ID",
    "Titel",
    "Name",
    "Vorname",
    "Strasse",
    "Hausnummer",
    "PLZ",
    "Ort",
    "Land",
    "Privat",
    "Handy",
    "Email",
    "Geburtstag",
    "Erfasser",
    "Bemerkung",
    "Eiche-\nMitglied",
    "Sektions-\nmitglied",
    "CKK",
    "Landfrauen-\nverband",
    "Raviva",
    "Nicht-\nMitglied",
    "Nationalregister",
    "Geschlecht",
    ]

    def row2instance(self, nr, title, last_name, first_name, street,
                     street_box,
                     zip_code, city_name, country_name,
                     phone, gsm, email, birth_date, erfasser,
                     remark,
                     eiche_mg, sektions_mitglied, ckk, lfv, raviva,
                     nicht_mitglied, national_id, sex):
        kw = dict(last_name=last_name, first_name=first_name)
        if nr:
            kw.update(legacy_id=nr)
        kw.update(phone=phone)
        kw.update(gsm=gsm)
        try:
            kw.update(zip_code=str(int(zip_code)))
        except ValueError:
            kw.update(zip_code=zip_code)

        if email:
            if isinstance(email, basestring) and is_valid_email(email):
                kw.update(email=email)
            else:
                logger.warning("Ignored invalid email address %r", email)

        kw.update(street2kw(street))

        kw.update(street_box=street_box)
        kw.update(remarks=remark)

        if title == "Herr":
            kw.update(gender=dd.Genders.male)
        elif title == "Frau":
            kw.update(gender=dd.Genders.female)
        elif title:
            kw.update(title=title)

        if sex == "Weiblich":
            kw.update(gender=dd.Genders.female)
        elif sex == "Männlich":
            kw.update(gender=dd.Genders.male)
        city_name = city_name.strip()
        if city_name:
            #~ countries.Place.objects.get(name)
            kw.update(city=countries.Place.lookup_or_create(
                'name', city_name, country=self.country))
        #~ print birth_date
        kw.update(birth_date=self.date_converter(birth_date))
        return courses.Pupil(**kw)


def objects():

    p = settings.SITE.legacy_data_path or settings.SITE.project_dir
    # book = MyBook(os.path.join(p, "Eiche 2013.xls"))
    book = MyBook2016(os.path.join(p, "Eiche2016.xls"))
    yield book.objects()
