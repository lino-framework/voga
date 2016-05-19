# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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

"""
Adds some demo data specific to Lino Voga à la Roger.

    legacy_id
    section

    is_lfv
    is_ckk
    is_raviva
    member_until


"""

from lino.api import dd, rt
from lino.utils.cycler import Cycler

from lino_voga.lib.courses.fixtures.demo import objects as lib_objects


def objects():

    yield lib_objects()

    SECTIONS = Cycler(rt.modules.courses.Sections.objects())

    for obj in rt.modules.courses.Pupil.objects.order_by('id'):
        if obj.id % 5 == 0:
            obj.is_lfv = True
        if obj.id % 6 == 0:
            obj.is_ckk = True
        if obj.id % 4 == 0:
            obj.section = SECTIONS.pop()
        elif obj.id % 10 != 0:
            obj.member_until = dd.demo_date().replace(month=12, day=31)
        yield obj
