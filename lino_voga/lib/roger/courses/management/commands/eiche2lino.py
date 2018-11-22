# -*- coding: UTF-8 -*-
# Copyright 2016-2017 by Rumma & Ko Ltd.
"""

Defines the :manage:`eiche2lino` management command:

.. management_command:: eiche2lino

.. py2rst::

  from lino_voga.lib.roger.courses.management.commands.eiche2lino \
      import Command
  print(Command.help)

"""

from __future__ import unicode_literals, print_function

# from optparse import make_option

from builtins import range
from builtins import str
import datetime

from dateutil.parser import parse as parse_date
# from django.utils import translation
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from lino.api import rt

try:
    from xlrd import open_workbook, xldate_as_tuple
    from xlrd.xldate import XLDateError
except ImportError:
    pass  # ignore the problem so that autodoc can work without xlrd
          # installed.

from lino.utils import iif
from lino.utils import IncompleteDate
from lino_xl.lib.contacts.utils import street2kw

# from lino.api.shell import *
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
            dd.logger.info("Failed to read date %s : %s", v, e)
            return None
        assert len(t) == 6
        t = t[:3]
        return IncompleteDate(*t)

    def __init__(self, filename):
        self.filename = filename

    def objects(self):
        Country = rt.models.countries.Country

        self.country = Country.objects.get(isocode="BE")
        self.book = open_workbook(self.filename)
        s = self.book.sheet_by_index(0)
        # print 'Sheet:',s.name
        found = False
        ncols = len(self.column_headers)
        for rowx in range(s.nrows):
            row = s.row(rowx)
            values = [c.value for c in row]
            if len(values) != ncols:
                dd.logger.warning(
                    "Expected %d values in row %d but got %s",
                    ncols, rowx, values)
            # values = [s.cell(row, col).value for col in range(ncols)]
            if found:
                obj = self.row2instance(*values)

                try:
                    obj.full_clean()
                    yield obj
                except ValidationError as e:
                    dd.logger.warning("Failed to save %s : %s", obj, e)

                # obj.full_clean()
                # obj.save()
                # logger.info("%s (%s) has been saved", obj, obj.birth_date)
            elif values == self.column_headers:
                found = True
            elif row < 5:
                dd.logger.info("Ignored line %s (waiting for %s)",
                               values, self.column_headers)

    def row2instance(self, nr, title, last_name, first_name, street,
                     zip_code, city_name, phone, gsm, birth_date, bez, datum,
                     mg, mgnr, email):
        Place = rt.models.countries.Place
        Pupil = rt.models.courses.Pupil

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
                dd.logger.warning("Ignored invalid email address %r", email)

        kw.update(street2kw(street))

        if title == "Herr":
            kw.update(gender=dd.Genders.male)
        elif title == "Frau":
            kw.update(gender=dd.Genders.female)
        elif title:
            kw.update(title=title)
        city_name = city_name.strip()
        if city_name:
            #~ Place.objects.get(name)
            kw.update(city=Place.lookup_or_create(
                'name', city_name, country=self.country))
        #~ print birth_date
        kw.update(birth_date=self.date_converter(birth_date))
        return Pupil(**kw)


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

    def row2instance(self, legacy_id, title, last_name, first_name, street,
                     street_box,
                     zip_code, city_name, country_name,
                     phone, gsm, email, birth_date, erfasser,
                     remark,
                     eiche_mg, sektion, ckk, lfv, raviva,
                     nicht_mitglied, national_id, sex):
        Place = rt.models.countries.Place
        Pupil = rt.models.courses.Pupil
        Sections = rt.models.courses.Sections
        MEMBER_UNTIL = datetime.date(2016, 12, 31)

        update_fields = (
            'member_until', 'section', 'is_ckk', 'is_lfv', 'is_raviva')

        kw = dict(last_name=last_name, first_name=first_name)

        if legacy_id:
            kw.update(legacy_id=legacy_id)
        kw.update(is_raviva=raviva)
        kw.update(is_ckk=ckk)
        kw.update(is_lfv=lfv)
        kw.update(is_member=eiche_mg)
        kw.update(member_until=MEMBER_UNTIL if eiche_mg else None)
        kw.update(national_id=national_id)

        sektion = sektion.strip().lower()
        if sektion and sektion not in ("nein", "0", 'ja', '-1'):
            if sektion in ('wywertz', 'weywerz'):
                sektion = "weywertz"
            if sektion in ('heregenrath', ):
                sektion = "hergenrath"
            kw.update(section=Sections.get_by_name(sektion))

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
                dd.logger.warning("Ignored invalid email address %r", email)

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
            kw.update(city=Place.lookup_or_create(
                'name', city_name, country=self.country))
        #~ print birth_date
        kw.update(birth_date=self.date_converter(birth_date))

        try:
            obj = Pupil.objects.get(legacy_id=legacy_id)
            # for k, v in kw.items():
            changed = []
            for k in update_fields:
                if k in kw:
                    v = kw[k]
                    setattr(obj, k, v)
                    changed.append(v)
            uvalues = [eiche_mg, sektion, ckk, lfv, raviva]
            dd.logger.info("Updated %s (%s from %s)", obj, changed, uvalues)
        except Pupil.DoesNotExist:
            obj = Pupil(**kw)
            dd.logger.info("Created %s", obj)
        if eiche_mg and nicht_mitglied:
            dd.logger.warning("%s : Mitglied und Nicht-Mitglied zugleich", obj)
        return obj


class Command(BaseCommand):
    args = "Input_file1.xls [Input_file2.xls] ..."
    help = """

    First-time legacy data import.

    Customer-specific script to import data into :ref:`voga`
    from an .xls file. To be invoked using something like::

        python manage.py eiche2lino /path/to/Input_file.xls

    This is designed to be used several in February 2015 during the
    transitional phase.

    """

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError(self.help)

        Pupil = rt.models.courses.Pupil
        qs = Pupil.objects.all()
        if False:
            dd.logger.info("Delete %d pupils", qs.count())
            qs.delete()
            # for obj in Pupil.objects.all():
            #     obj.delete()

        for pth in args:
            book = MyBook2016(pth)
            for obj in book.objects():
                obj.save()


