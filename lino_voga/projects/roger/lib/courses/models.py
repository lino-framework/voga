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

import datetime

from lino.api import dd, rt, _

from lino.mixins.periods import DatePeriod
from lino.mixins import Referrable

from lino_voga.lib.courses.models import *


class Sections(dd.ChoiceList):
    verbose_name = _("Section")
    verbose_name_plural = _("Sections")
    
add = Sections.add_item

names = """Eupen Nidrum Walhorn Herresbach Eynatten Kelmis Hergenrath
Hauset Elsenborn Weywertz"""

for i, name in enumerate(names.split()):
    add(name.lower(), name, name.lower())
# add("01", "Eupen", "eupen")
# add("02", "Nidrum", "nidrum")
# add("03", "Walhorn", "walhorn")
add("etc", "Sonstige", "etc")


class Pupil(Pupil):
    """The Roger variant of Lino Voga adds a few very specific fields
    which are being used for filtering, and they may influence the
    price of an enrolment.

    .. attribute:: legacy_id
    .. attribute:: section
    .. attribute:: is_lfv
    .. attribute:: is_ckk
    .. attribute:: is_raviva
    .. attribute:: member_until

    """
    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Pupil')
        verbose_name = _("Participant")
        verbose_name_plural = _('Participants')

    legacy_id = models.CharField(
        _("Legacy ID"), max_length=12, blank=True)

    section = Sections.field(blank=True)

    is_lfv = models.BooleanField(_("LFV"), default=False)
    is_ckk = models.BooleanField(_("CKK"), default=False)
    is_raviva = models.BooleanField(_("Raviva"), default=False)
    is_member = models.BooleanField(_("Member"), default=False)
    member_until = models.DateField(_("Mitglied bis"), blank=True, null=True)

    def get_enrolment_info(self):
        """Return a short text to be displayed between parentheses
        in `lino_cosi.lib.courses.ui.EnrolmentsByCourse.pupil_info`.
        """
        if self.member_until is None:
            s = ""
        elif self.member_until >= datetime.date.today():
            s = "E"
        else:
            s = "e"
        if self.is_lfv:
            s += "L"
        if self.is_ckk:
            s += "C"
        if self.is_raviva:
            s += "R"
        if self.section:
            s += " " + self.section
        return s

    # TODO:
    # @classmethod
    # def get_parameter_fields(cls, **fields):
    #     fields.update(is_member=models.BooleanField(_("is member")))
    #     return super(Pupil, cls).get_parameter_fields(**fields)

    # @classmethod
    # def get_request_queryset(cls, ar):
    #     qs = super(Pupil, cls).get_request_queryset(ar)
        
    #     return qs

    # @classmethod
    # def get_title_tags(self, ar):
    #     return []


class PupilDetail(PupilDetail):
    # main = "general courses.EnrolmentsByPupil"
    # main = contacts.PersonDetail.main + ' courses_tab'

    # general = dd.Panel(contacts.PersonDetail.main, label=_("General"))
    # box5 = "remarks"

    courses = dd.Panel("""
    legacy_id member_until section is_lfv is_ckk is_raviva
    courses.SuggestedCoursesByPupil
    courses.EnrolmentsByPupil
    """, label=dd.plugins.courses.verbose_name)


Pupils.detail_layout = PupilDetail()


class Line(Line):
    # this is here just because is_abstract_model does not yet work as
    # expected: if you subclass a plugin which extends a given model
    # then you must also extend all models in your plugin.

    class Meta(Line.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Line')


class Course(Referrable, Course):
    """Adds a :attr:`ref` field.
    """
    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Course')
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def update_cal_summary(self, i):
        label = dd.babelattr(self.line.event_type, 'event_label')
        if self.ref:
            label = self.ref + ' ' + label
        return "%s %d" % (label, i)

    def __unicode__(self):
        if self.ref and self.line:
            return "{0} {1}".format(self.ref, self.line)
        return super(Course, self).__unicode__()

Course.set_widget_options('ref', preferred_with=6)


class CourseDetail(CourseDetail):
    general = dd.Panel("""
    ref line teacher workflow_buttons
    room start_date end_date start_time end_time
    name
    remark #OptionsByCourse
    # courses.EventsByCourse
    """, label=_("General"))


Courses.detail_layout = CourseDetail()
Courses.order_by = ['ref', '-start_date', '-start_time']
Courses.column_names = "ref start_date enrolments_until line room teacher " \
                       "workflow_buttons *"


class Enrolment(Enrolment, DatePeriod):
    """
    
    """
    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Enrolment')
        verbose_name = _("Enrolment")
        verbose_name_plural = _("Enrolments")

    # def suggest_guest_for(self, event):
    #     return self.state in GUEST_ENROLMENT_STATES

Enrolments.detail_layout = """
id course pupil request_date user
start_date end_date places fee option amount
remark workflow_buttons printed
confirmation_details invoicing.InvoicingsByInvoiceable
"""


EnrolmentsByPupil.column_names = 'request_date course start_date end_date '\
                                 'places remark amount workflow_buttons *'

EnrolmentsByCourse.column_names = 'request_date pupil_info start_date end_date '\
                                  'places remark fee option amount ' \
                                  'workflow_buttons *'

