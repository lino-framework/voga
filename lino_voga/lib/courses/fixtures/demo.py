# -*- coding: UTF-8 -*-
# Copyright 2012-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
from __future__ import unicode_literals

from builtins import range
import datetime

from lino.api import dd, rt
from lino.utils import mti, Cycler
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

# courses = dd.resolve_app('courses')
# cal = dd.resolve_app('cal')
# users = dd.resolve_app('users')


def objects():
    Person = rt.models.contacts.Person
    PupilType = rt.models.courses.PupilType
    TeacherType = rt.models.courses.TeacherType
    Pupil = rt.models.courses.Pupil
    Teacher = rt.models.courses.Teacher
    SalesRule = rt.models.invoicing.SalesRule

    yield PupilType(ref="M", **dd.str2kw('name', _("Member")))
    yield PupilType(ref="H", **dd.str2kw('name', _("Helper")))
    yield PupilType(ref="N", **dd.str2kw('name', _("Non-member")))

    #~ yield courses.Room(name="A")
    #~ yield cal.Place(name="A")
    #~ yield cal.Place(name="B")
    #~ yield cal.Place(name="C")
    #~ yield cal.Place(name="D")
    #~ yield cal.Place(name="E")
    #~ yield cal.Place(name="F")
    PTYPES = Cycler(PupilType.objects.all())
    TTYPES = Cycler(TeacherType.objects.all())

    n = 0
    for p in Person.objects.all():
        if n % 2 == 0:
            yield mti.insert_child(p, Pupil, pupil_type=PTYPES.pop())
        if n % 9 == 0:
            yield mti.insert_child(p, Teacher, teacher_type=TTYPES.pop())
        n += 1

    invoice_recipient = None
    for n, p in enumerate(Pupil.objects.all()):
        if n % 10 == 0:
            yield SalesRule(
                partner=p, invoice_recipient=invoice_recipient)
            # p.invoice_recipient = invoice_recipient
            # yield p
        else:
            invoice_recipient = p
            
    if False:

        #~ PS = Cycler(courses.PresenceStatus.objects.all())
        CONTENTS = Cycler(rt.models.courses.Line.objects.all())
        USERS = Cycler(rt.models.users.User.objects.all())
        PLACES = Cycler(rt.models.cal.Room.objects.all())
        TEACHERS = Cycler(Teacher.objects.all())
        SLOTS = Cycler(rt.models.courses.Slot.objects.all())
        #~ SLOTS = Cycler(1,2,3,4)
        PUPILS = Cycler(Pupil.objects.all())
        #~ Event = settings.SITE.models.cal.Event

        #~ from lino_xl.lib.cal.utils import DurationUnit

        year = settings.SITE.demo_date().year
        if settings.SITE.demo_date().month < 7:
            year -= 1
        for i in range(10):
            c = courses.Course(
                user=USERS.pop(),
                teacher=TEACHERS.pop(),
                line=CONTENTS.pop(), room=PLACES.pop(),
                start_date=datetime.date(year, 9, 1 + i),
                end_date=datetime.date(year + 1, 6, 30),
                every=1,
                every_unit=cal.DurationUnits.weeks,
                slot=SLOTS.pop(),
            )
            yield c
            for j in range(5):
                yield courses.Enrolment(pupil=PUPILS.pop(), course=c)

            c.save()  # fill presences

            #~ for j in range(5):
                #~ yield courses.Event(start_date=settings.SITE.demo_date(j*7),course=c)
                #~ yield courses.Presence()
