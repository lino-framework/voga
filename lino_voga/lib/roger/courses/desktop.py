# -*- coding: UTF-8 -*-
# Copyright 2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
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

