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
Adds some specific fields for managing the member fee.

"""

from __future__ import unicode_literals
from __future__ import print_function

from lino.api import dd

from lino_voga.lib.courses.desktop import *


class PupilDetail(PupilDetail):
    # main = "general courses.EnrolmentsByPupil"
    # main = contacts.PersonDetail.main + ' courses_tab'

    # general = dd.Panel(contacts.PersonDetail.main, label=_("General"))
    # box5 = "remarks"

    courses = dd.Panel("""
    legacy_id member_until section is_lfv is_ckk is_raviva
    courses.EnrolmentsByPupil
    """, label=dd.plugins.courses.verbose_name)


Pupils.detail_layout = PupilDetail()
Pupils.insert_layout = """
first_name last_name
gender language
pupil_type section member_until
is_lfv is_ckk is_raviva
"""
Pupils.params_layout = "course partner_list #aged_from #aged_to gender "\
                       "show_members show_lfv show_ckk show_raviva"
Pupils.column_names = (
    'name_column address_column '
    'pupil_type section is_lfv is_ckk is_raviva member_until *')

