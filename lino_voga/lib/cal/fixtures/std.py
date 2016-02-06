# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)


from lino.api import dd, rt, _


def objects():
    GuestRole = rt.modules.cal.GuestRole
    yield GuestRole(**dd.str2kw('name', _("Participant")))
    yield GuestRole(**dd.str2kw('name', _("Guide")))
    yield GuestRole(**dd.str2kw('name', _("Teacher")))
