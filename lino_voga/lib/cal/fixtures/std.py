# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime

from lino.api import dd, rt, _

from lino_xl.lib.cal.fixtures.std import objects as lib_objects


def objects():

    yield lib_objects()

    GuestRole = rt.models.cal.GuestRole

    yield GuestRole(**dd.str2kw('name', _("Participant")))
    yield GuestRole(**dd.str2kw('name', _("Guide")))
    yield GuestRole(**dd.str2kw('name', _("Teacher")))

    EventType = rt.models.cal.EventType
    RecurrentEvent = rt.models.cal.RecurrentEvent
    Recurrencies = rt.models.cal.Recurrencies
    DEMO_START_YEAR = rt.models.cal.DEMO_START_YEAR

    holidays = EventType.objects.get(
        **dd.str2kw('name', _("Holidays")))
    yield RecurrentEvent(
        event_type=holidays,
        every_unit=Recurrencies.yearly,
        monday=True, tuesday=True, wednesday=True, thursday=True,
        friday=True, saturday=True, sunday=True,
        every=1,
        start_date=datetime.date(
            year=DEMO_START_YEAR,
            month=7, day=1),
        end_date=datetime.date(
            year=DEMO_START_YEAR,
            month=8, day=31),
        **dd.str2kw('name', _("Summer holidays")))
