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
Does some adaptions.
"""

from __future__ import unicode_literals
from __future__ import print_function

from lino.api import dd, rt, _

from lino.mixins.periods import DatePeriod

from lino_voga.lib.courses.models import *


class Pupil(Pupil):
    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Pupil')
        verbose_name = _("Participant")
        verbose_name_plural = _('Participants')

    legacy_id = models.CharField(
        _("Legacy ID"), max_length=12, blank=True)


class Enrolment(Enrolment, DatePeriod):
    """
    
    """
    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Enrolment')

    # def suggest_guest_for(self, event):
    #     return self.state in GUEST_ENROLMENT_STATES

Enrolments.detail_layout = """
request_date start_date end_date user
course pupil
remark amount workflow_buttons printed
confirmation_details sales.InvoicingsByInvoiceable
"""


EnrolmentsByPupil.column_names = 'request_date course start_date end_date '\
                                 'workflow_buttons *'

