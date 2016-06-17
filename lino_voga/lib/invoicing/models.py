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

"""The :xfile:`models.py` module for :mod:`lino_voga.lib.invoicing`.

"""

from __future__ import unicode_literals

from lino_cosi.lib.invoicing.models import *
from lino.api import _


class Plan(Plan):
    """An extended invoicing plan.

    .. attribute:: course

        If this field is nonempty, select only enrolments of that
        given course.

    """

    class Meta(Plan.Meta):
        app_label = 'invoicing'
        abstract = dd.is_abstract_model(__name__, 'Plan')

    course = dd.ForeignKey('courses.Course', blank=True, null=True)


Plans.detail_layout = """user journal today max_date
    partner course
    invoicing.ItemsByPlan
    """


from lino_cosi.lib.invoicing.actions import StartInvoicing


class StartInvoicingForCourse(StartInvoicing):
    """Start an invoicing plan for this course.

    This is installed onto the :class:`courses.Course
    <lino_voga.lib.courses.models.Course>` model as `start_invoicing`.

    """
    select_rows = True

    def get_options(self, ar):
        course = ar.selected_rows[0]
        assert isinstance(course, rt.modules.courses.Course)
        return dict(course=course, partner=None, journal=None)


@dd.receiver(dd.pre_analyze)
def install_start_action(sender=None, **kwargs):
    rt.modules.courses.Course.start_invoicing = StartInvoicingForCourse()
    

