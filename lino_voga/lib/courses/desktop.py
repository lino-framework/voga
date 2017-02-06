# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
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
Desktop design for this plugin.

"""

from __future__ import unicode_literals
from __future__ import print_function

from builtins import str

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino.utils import join_elems
from lino_voga.lib.contacts.models import PersonDetail

from lino_xl.lib.courses.desktop import *

contacts = dd.resolve_app('contacts')

day_and_month = dd.plugins.courses.day_and_month

from lino_xl.lib.cal.ui import EventsByController
from lino.utils.report import Report


class TeacherTypes(dd.Table):
    model = 'courses.TeacherType'
    detail_layout = """
    id name
    courses.TeachersByType
    """


class PupilTypes(dd.Table):
    model = 'courses.PupilType'
    detail_layout = """
    id name
    courses.PupilsByType
    """


class CourseTypes(dd.Table):
    model = 'courses.CourseType'
    detail_layout = """
    id name
    courses.LinesByType
    """


Lines.detail_layout = """
    id name ref
    course_area topic fees_cat fee options_cat body_template
    course_type event_type guest_role every_unit every
    description
    excerpt_title
    courses.CoursesByLine
    """


# Enrolments.detail_layout = """
#     request_date user course
#     pupil places fee option
#     remark amount workflow_buttons
#     confirmation_details invoicing.InvoicingsByInvoiceable
#     """

Enrolments.detail_layout = """
id course pupil request_date user
start_date end_date places:8 fee free_events:8 #option amount
remark workflow_buttons printed invoicing_info
confirmation_details invoicing.InvoicingsByInvoiceable
"""


from lino_cosi.lib.invoicing.models import InvoicingsByInvoiceable

InvoicingsByInvoiceable.column_names = (
    "voucher title qty voucher__voucher_date "
    "voucher__state product__number_of_events *")


class PendingRequestedEnrolments(PendingRequestedEnrolments):
    column_names = 'request_date course pupil remark user ' \
                   'amount workflow_buttons'


class EnrolmentsByPupil(EnrolmentsByPupil):
    column_names = 'request_date course start_date end_date '\
                   'places remark amount workflow_buttons *'

    # column_names = 'request_date course user:10 remark ' \
    #                'amount:10 workflow_buttons *'

    insert_layout = """
    course_area
    course
    places option
    remark
    request_date user
    """


class EnrolmentsByCourse(EnrolmentsByCourse):
    """The Voga version of :class:`EnrolmentsByCourse
    <lino_xl.lib.courses.ui.EnrolmentsByCourse>`.

    """
    # variable_row_height = True
    column_names = 'request_date pupil start_date end_date '\
                   'places:8 remark fee free_events:8 #option amount ' \
                   'workflow_buttons *'

    # column_names = 'request_date pupil_info places ' \
    #                'fee option remark amount:10 workflow_buttons *'


class EnrolmentsByFee(EnrolmentsByCourse):
    label = _("Enrolments using this fee")
    master_key = "fee"
    column_names = 'course request_date pupil_info start_date end_date '\
                   'places remark free_events #option amount *'


class PupilDetail(PersonDetail):

    # main = PersonDetail.main + " courses"
    main = 'general address courses ledger more'

    courses = dd.Panel("""
    # courses.SuggestedCoursesByPupil
    courses.EnrolmentsByPupil
    """, label=dd.plugins.courses.verbose_name)

    personal = 'pupil_type national_id card_number'

    bottom_box = """
    remarks:50 plausibility.ProblemsByOwner:30
    """


class TeacherDetail(PersonDetail):
    main = PersonDetail.main + " courses"

    courses = dd.Panel("""
    courses.EventsByTeacher
    courses.CoursesByTeacher
    """, label=dd.plugins.courses.verbose_name)

    personal = 'teacher_type national_id'


# class TeacherDetail(contacts.PersonDetail):
#     general = dd.Panel(contacts.PersonDetail.main, label=_("General"))
#     box5 = "remarks"
#     main = "general courses.CoursesByTeacher \
#     courses.EventsByTeacher cal.GuestsByPartner"


class Teachers(contacts.Persons):
    model = 'courses.Teacher'
    detail_layout = TeacherDetail()
    column_names = 'name_column address_column teacher_type *'
    auto_fit_column_widths = True


class TeachersByType(Teachers):
    master_key = 'teacher_type'


class Pupils(contacts.Persons):
    """The global list of all pupils.

    Fitler parameters:

    .. attribute:: course

        Show only pupils who participate in the given course.

    """
    model = 'courses.Pupil'
    detail_layout = PupilDetail()
    column_names = 'name_column address_column pupil_type *'
    auto_fit_column_widths = True
    # parameters = mixins.ObservedPeriod()

    params_layout = "aged_from aged_to gender"


class PupilsByType(Pupils):
    master_key = 'pupil_type'


class EventsByCourse(EventsByController):
    """Shows the events linked to this course.
    """
    column_names = "start_date auto_type workflow_buttons "\
                   "start_time end_time room summary *"

    slave_grid_format = "summary"

    @classmethod
    def get_slave_summary(self, obj, ar):
        """The summary view for this table.

        See :meth:`lino.core.actors.Actor.get_slave_summary`.

        """
        if ar is None:
            return ''
        sar = self.request_from(ar, master_instance=obj)

        elems = []
        for evt in sar:
            # if len(elems) > 0:
            #     elems.append(', ')
            elems.append(' ')
            if evt.auto_type:
                # elems.append("({}) ".format(evt.auto_type))
                elems.append("{}: ".format(evt.auto_type))
            lbl = day_and_month(evt.start_date)
            if evt.state.button_text:
                lbl = "{0}{1}".format(lbl, evt.state.button_text)
            elems.append(ar.obj2html(evt, lbl))
        # elems = join_elems(elems, sep=', ')
        sar = obj.do_update_events.request_from(sar)
        if sar.get_permission():
            btn = sar.ar2button(obj)
            elems.append(E.p(btn))

        # return E.div(class_="htmlText", *elems)
        return ar.html_text(E.div(*elems))


class CourseDetail(CourseDetail):
    """The detail layout of a :class:`Course` (:ref:`voga` variant).

    """
    main = "general events enrolments more"
    general = dd.Panel("""
    ref line teacher workflow_buttons
    room start_date end_date start_time end_time
    name
    remark
    """, label=_("General"))

    events = dd.Panel("""
    every_unit every max_date max_events
    monday tuesday wednesday thursday friday saturday sunday
    courses.EventsByCourse

    """, label=_("Events"))

    enrolments_top = 'enrolments_until fee:15 max_places:10 confirmed free_places:10 print_actions:15'

    enrolments = dd.Panel("""
    enrolments_top
    EnrolmentsByCourse
    """, label=_("Enrolments"))

    more = dd.Panel("""
    # company contact_person
    state user payment_term paper_type id
    invoicing.InvoicingsByInvoiceable
    """, label=_("More"))


Courses.detail_layout = CourseDetail()
# Courses._course_area = CourseAreas.default
Courses.order_by = ['ref', '-start_date', '-start_time']
Courses.column_names = "ref start_date enrolments_until line room teacher " \
                       "workflow_buttons *"


# class Courses(Courses):
#     # detail_layout = CourseDetail()
#     order_by = ['ref', '-start_date', '-start_time']
#     column_names = "ref start_date enrolments_until line room teacher " \
#                    "workflow_buttons *"


# @dd.receiver(dd.pre_analyze)
# def customize_courses(sender, **kw):
#     sender.modules.courses.Courses.set_detail_layout(CourseDetail())

if False:

    # Exception: Cannot reuse detail_layout of <class
    # 'lino_xl.lib.courses.models.CoursesByTeacher'> for <class
    # 'lino_xl.lib.courses.models.CoursesBySlot'>

    class Courses(Courses):

        parameters = dict(Courses.parameters,
            city=models.ForeignKey('countries.Place', blank=True, null=True))

        params_layout = """topic line city teacher user state active:10"""

        @classmethod
        def get_request_queryset(self, ar):
            qs = super(Courses, self).get_request_queryset(ar)
            if ar.param_values.city:
                flt = Q(room__isnull=True)
                flt |= Q(room__company__city=ar.param_values.city)
                qs = qs.filter(flt)
            return qs

        @classmethod
        def get_title_tags(self, ar):
            for t in super(Courses, self).get_title_tags(ar):
                yield t
            if ar.param_values.city:
                yield _("in %s") % ar.param_values.city

        @dd.chooser()
        def city_choices(cls):
            Place = rt.modules.countries.Place
            Room = rt.modules.cal.Room
            places = set([
                obj.company.city.id
                for obj in Room.objects.filter(company__isnull=False)])
            # logger.info("20140822 city_choices %s", places)
            return Place.objects.filter(id__in=places)

    class SuggestedCoursesByPupil(SuggestedCoursesByPupil):
        button_text = _("Suggestions")
        params_layout = 'topic line city teacher active'

        @classmethod
        def param_defaults(self, ar, **kw):
            kw = super(SuggestedCoursesByPupil, self).param_defaults(ar, **kw)
            # kw.update(active=dd.YesNo.yes)
            pupil = ar.master_instance
            if pupil and pupil.city:
                kw.update(city=pupil.city)
            return kw


class CoursesByTopic(CoursesByTopic):
    """Shows the courses of a given topic.

    This is used both in the detail window of a topic and in
    :class:`StatusReport`.

    """
    order_by = ["ref"]
    column_names = "overview #name weekdays_text:10 times_text:10 "\
                   "max_places:8 confirmed "\
                   "free_places requested *"

    # detail_layout = Courses.detail_layout

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(CoursesByTopic, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.active)
        kw.update(can_enroll=dd.YesNo.yes)
        return kw


class CoursesByLine(CoursesByLine):
    """Like :class:`lino_xl.lib.courses.CoursesByLine`, but with other
    default values in the filter parameters. In Voga we want to see
    only courses for which new enrolments can happen.
    
    TODO: when Lino gets class-based user roles, move this back to the
    library table and show all courses only for users with profile
    `courses.CourseManager`.

    """
    # detail_layout = Courses.detail_layout

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(CoursesByLine, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.active)
        kw.update(can_enroll=dd.YesNo.yes)
        return kw


class LinesByType(Lines):
    master_key = 'course_type'


# class ActiveCourses(ActiveCourses):
#     column_names = 'info max_places enrolments teacher line room *'
#     hide_sums = True




class StatusReport(Report):
    """Gives an overview about what's up today .

    """

    label = _("Status Report")

    @classmethod
    def get_story(cls, self, ar):
        for topic in rt.models.courses.Topic.objects.all():
            yield E.h3(str(topic))
            yield ar.spawn(CoursesByTopic, master_instance=topic)


class EnrolmentsAndPaymentsByCourse(Enrolments):
    """Show enrolments of a course together with
    :attr:`invoicing_info` and :attr:`payment_info`.

    This is used by `payment_list.body.html`.

    

    """
    master_key = 'course'
    column_names = "pupil_info start_date invoicing_info payment_info"


class EnrolmentsByHike(EnrolmentsByCourse):
    column_names = 'request_date pupil '\
                   'places:8 remark fee option amount ' \
                   'workflow_buttons *'


class EnrolmentsByJourney(EnrolmentsByCourse):
    column_names = 'request_date pupil '\
                   'places:8 remark fee option amount ' \
                   'workflow_buttons *'


class HikeDetail(CourseDetail):
    enrolments = dd.Panel("""
    enrolments_top
    EnrolmentsByHike
    """, label=_("Enrolments"))


class JourneyDetail(CourseDetail):
    enrolments = dd.Panel("""
    enrolments_top
    EnrolmentsByJourney
    """, label=_("Enrolments"))


class Hikes(Courses):
    _course_area = CourseAreas.hikes
    detail_layout = HikeDetail()
    column_names = "ref name start_date enrolments_until line " \
                   "workflow_buttons *"


class Journeys(Courses):
    _course_area = CourseAreas.journeys
    detail_layout = JourneyDetail()
    column_names = "ref name start_date end_date enrolments_until line " \
                   "workflow_buttons *"


