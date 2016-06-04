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

from django.db.models import Q
from django.utils.translation import string_concat

from lino.api import dd, rt, _

from lino.mixins import Referrable
from lino.mixins.periods import Monthly
from lino.utils import join_elems

from lino.modlib.printing.mixins import DirectPrintAction
from lino.modlib.plausibility.choicelists import Checker

from lino_voga.lib.courses.models import *

from lino.modlib.printing.utils import PrintableObject

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


class PrintPresenceSheet(DirectPrintAction):
    """Action to print a presence sheet.
    """
    combo_group = "creacert"
    label = _("Presence sheet")
    tplname = "presence_sheet"
    build_method = "weasy2pdf"
    icon_name = None
    # show_in_bbar = False
    parameters = Monthly(
        show_remarks=models.BooleanField(
            _("Show remarks"), default=False),
        show_states=models.BooleanField(
            _("Show states"), default=True))
    params_layout = """
    start_date
    end_date
    show_remarks
    show_states
    """
    keep_user_values = True


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
        s = ""
        if self.member_until is None:
            pass
        elif self.member_until >= dd.demo_date():
            s = "E"
        if self.is_ckk:
            s += "C"
        if self.is_lfv:
            s += "L"
        # if self.is_raviva:
        #     s += "R"
        if self.section:
            s += "S"
            # s += " {0}".format(self.section)
        if s:
            return "M{0}".format(s)
        return "N"

    @classmethod
    def get_parameter_fields(cls, **fields):
        fields.update(
            show_members=dd.YesNo.field(
                _("Members"), blank=True,
                help_text=_(
                    "Show those whose 'Member until' is after today.")),
            show_ckk=dd.YesNo.field(_("CKK"), blank=True),
            show_lfv=dd.YesNo.field(_("LFV"), blank=True),
            show_raviva=dd.YesNo.field(_("Raviva"), blank=True))

        return super(Pupil, cls).get_parameter_fields(**fields)

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Pupil, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.show_members == dd.YesNo.no:
            qs = qs.filter(
                Q(member_until__isnull=True) | Q(member_until__lt=dd.today()))
        elif pv.show_members == dd.YesNo.yes:
            qs = qs.filter(Q(member_until__gte=dd.today()))
        for k in ('ckk', 'raviva', 'lfv'):
            v = pv['show_' + k]
            if v:
                qs = qs.filter(**{'is_' + k: v == dd.YesNo.yes})
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Pupil, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.show_members:
            yield "{0}:{1}".format(_("Members"), pv.show_members)
        if pv.show_members:
            yield "{0}:{1}".format(_("Members"), pv.show_members)


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
Pupils.params_layout = "aged_from aged_to gender "\
                       "show_members show_lfv show_ckk show_raviva"
Pupils.column_names = (
    'name_column address_column '
    'pupil_type section is_lfv is_ckk is_raviva member_until *')


class Line(Line):
    # this is here just because is_abstract_model does not yet work as
    # expected: if you subclass a plugin which extends a given model
    # then you must also extend all models in your plugin.

    class Meta(Line.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Line')


@dd.python_2_unicode_compatible
class Course(Referrable, Course, PrintableObject):
    """Adds a :attr:`ref` field and defines a custom :meth:`__str__`
    method.

    The custom :meth:`__str__` method defines how to textually
    represent a course e.g. in the dropdown list of a combobox or in
    reports. Rules:

    - If :attr:`ref` is given, it is shown, but see also the two
      following cases.

    - If :attr:`name` is given, it is shown (possibly behind the
      :attr:`ref`).

    - If a :attr:`line` (series) is given, it is shown (possibly
      behind the :attr:`ref`).

    - If neither :attr:`ref` nor :attr:`name` nor :attr:`line` are
      given, show a simple "Course #".


    .. attribute:: ref
    
        An identifying public course number to be used by both
        external and internal partners for easily referring to a given
        course.

    .. attribute:: name

        A short designation for this course. An extension of the
        :attr:`ref`.

    .. attribute:: line

        Pointer to the course series.



    """
    class Meta(Course.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Course')

    print_presence_sheet = PrintPresenceSheet()
    print_presence_sheet_html = PrintPresenceSheet(
        build_method='weasy2html',
        label=string_concat(_("Presence sheet"), _(" (HTML)")))

    @dd.displayfield(_("Print"))
    def print_actions(self, ar):
        if ar is None:
            return ''
        elems = []
        elems.append(ar.instance_action_button(
            self.print_presence_sheet))
        elems.append(ar.instance_action_button(
            self.print_presence_sheet_html))
        return E.p(*join_elems(elems, sep=", "))

    def __str__(self):
        if self.name:
            if self.ref:
                return "{0} {1}".format(self.ref, self.name)
            return self.name
        if self.ref:
            if self.line:
                return "{0} {1}".format(self.ref, self.line)
            return self.ref
        # Note that we cannot use super() with
        # python_2_unicode_compatible
        return "{0} #{1}".format(self._meta.verbose_name, self.pk)

    def update_cal_summary(self, i):
        label = dd.babelattr(self.line.event_type, 'event_label')
        if self.ref:
            label = self.ref + ' ' + label
        return "%s %d" % (label, i)

Course.set_widget_options('ref', preferred_with=6)


class CourseDetail(CourseDetail):
    general = dd.Panel("""
    ref line teacher workflow_buttons
    room start_date end_date start_time end_time
    name
    remark #OptionsByCourse
    # courses.EventsByCourse
    """, label=_("General"))
    # TODO: make an action renderable as a data element of a form
    enrolments = dd.Panel("""
    enrolments_until fee max_places:8 confirmed free_places print_actions
    EnrolmentsByCourse:40
    """, label=_("Enrolments"))


Courses.detail_layout = CourseDetail()
Courses.order_by = ['ref', '-start_date', '-start_time']
Courses.column_names = "ref start_date enrolments_until line room teacher " \
                       "workflow_buttons *"


# class Enrolment(Enrolment, DatePeriod):
#     """
    
#     """
#     class Meta:
#         app_label = 'courses'
#         abstract = dd.is_abstract_model(__name__, 'Enrolment')
#         verbose_name = _("Enrolment")
#         verbose_name_plural = _("Enrolments")

    # def suggest_guest_for(self, event):
    #     return self.state in GUEST_ENROLMENT_STATES

# Enrolments.detail_layout = """
# id course pupil request_date user
# start_date end_date places fee option amount
# remark workflow_buttons printed
# confirmation_details invoicing.InvoicingsByInvoiceable
# """


# EnrolmentsByPupil.column_names = 'request_date course start_date end_date '\
#                                  'places remark amount workflow_buttons *'

# EnrolmentsByCourse.column_names = 'request_date pupil_info start_date end_date '\
#                                   'places remark fee option amount ' \
#                                   'workflow_buttons *'


class MemberChecker(Checker):
    """Check membership payments.

    If :attr:`force_cleared_until
    <lino_cosi.lib.ledger.Plugin.force_cleared_until>` is set, then
    :attr:`member_until` dates before that date are tolerated.

    """
    verbose_name = _("Check membership payments")
    model = Pupil
    messages = dict(
        no_payment=_("Member until {0}, but no payment."),
        wrong_until=_("Member until {0} (expected {1})."),
    )

    def get_plausibility_problems(self, obj, fix=False):
        qs = rt.models.ledger.Movement.objects.filter(
            partner=obj,
            account__ref=dd.plugins.courses.membership_fee_account)
        qs = qs.order_by('-value_date')
        until = obj.member_until
        fcu = dd.plugins.ledger.force_cleared_until
        if qs.count() == 0:
            if until:
                if fcu and until > fcu:
                    return
                yield (False, self.messages['no_payment'].format(until))
            return
        
        def expected_until(mvt):
            pd = mvt.value_date
            if pd.month > 8:
                return pd.replace(year=pd.year+1, month=12, day=31)
            return pd.replace(month=12, day=31)

        eu = expected_until(qs[0])
        if until != eu:
            msg = self.messages['wrong_until'].format(until, eu)
            if until is None or until < eu:
                if fix:
                    obj.member_until = eu
                    obj.full_clean()
                    obj.save()
                else:
                    yield (True, msg)
            else:
                yield (False, msg)


MemberChecker.activate()
