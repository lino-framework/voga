# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)


from lino.api import dd, rt, _

from lino.modlib.cal.fixtures.std import objects as lib_objects


def objects():

    yield lib_objects()

    GuestRole = rt.modules.cal.GuestRole
    yield GuestRole(**dd.str2kw('name', _("Participant")))
    yield GuestRole(**dd.str2kw('name', _("Guide")))
    yield GuestRole(**dd.str2kw('name', _("Teacher")))
