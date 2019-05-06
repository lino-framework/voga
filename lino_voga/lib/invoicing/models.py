# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The :xfile:`models.py` module for :mod:`lino_voga.lib.invoicing`.

"""

from __future__ import unicode_literals

from lino_xl.lib.invoicing.models import *
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


Plans.detail_layout = """
user area today min_date max_date
partner course
invoicing.ItemsByPlan
"""


# from lino.modlib.users.mixins import StartPlan
from lino_xl.lib.invoicing.actions import StartInvoicing


class StartInvoicingForCourse(StartInvoicing):
    """Start an invoicing plan for this course.

    This is installed onto the :class:`courses.Course
    <lino_voga.lib.courses.models.Course>` model as `start_invoicing`.

    """
    show_in_bbar = True
    select_rows = True

    def get_options(self, ar):
        course = ar.selected_rows[0]
        assert isinstance(course, rt.models.courses.Course)
        return dict(course=course, partner=None)


@dd.receiver(dd.pre_analyze)
def install_start_action(sender=None, **kwargs):
    rt.models.courses.Course.start_invoicing = StartInvoicingForCourse()
    

