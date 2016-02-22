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


from lino.api import dd, rt, _

from lino_xl.lib.cal.fixtures.std import objects as lib_objects


def objects():

    yield lib_objects()

    GuestRole = rt.modules.cal.GuestRole
    yield GuestRole(**dd.str2kw('name', _("Participant")))
    yield GuestRole(**dd.str2kw('name', _("Guide")))
    yield GuestRole(**dd.str2kw('name', _("Teacher")))
