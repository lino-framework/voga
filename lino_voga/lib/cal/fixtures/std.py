# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# This file is part of Lino Voga.
#
# Lino Voga is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Voga is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Voga.  If not, see
# <http://www.gnu.org/licenses/>.

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
