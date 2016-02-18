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
    # courses.EventsByCourse
    remark #OptionsByCourse
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
request_date start_date end_date user
course pupil
remark amount workflow_buttons printed
confirmation_details sales.InvoicingsByInvoiceable
"""


EnrolmentsByPupil.column_names = 'request_date course start_date end_date '\
                                 'amount workflow_buttons *'

EnrolmentsByCourse.column_names = 'request_date pupil_info start_date end_date '\
                                  'option remark amount workflow_buttons *'

