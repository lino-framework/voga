# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Desktop design for this plugin.

"""

from __future__ import unicode_literals
from __future__ import print_function

from builtins import str

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino.utils import join_elems

from lino_xl.lib.courses.desktop import *
from lino_xl.lib.courses.roles import CoursesUser
from lino_voga.lib.contacts.models import PersonDetail

contacts = dd.resolve_app('contacts')

from lino_xl.lib.cal.ui import EntriesByController


class TeacherTypes(dd.Table):
    model = 'courses.TeacherType'
    required_roles = dd.login_required(CoursesUser)
    detail_layout = """
    id name
    courses.TeachersByType
    """


class PupilTypes(dd.Table):
    model = 'courses.PupilType'
    required_roles = dd.login_required(CoursesUser)
    detail_layout = """
    id name
    courses.PupilsByType
    """


class CourseTypes(dd.Table):
    model = 'courses.CourseType'
    required_roles = dd.login_required(CoursesUser)
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
#     confirmation_details invoicing.InvoicingsByGenerator
#     """

Enrolments.detail_layout = """
id course pupil request_date user
start_date end_date places:8 fee free_events:8 #option amount
remark workflow_buttons printed invoicing_info
confirmation_details invoicing.InvoicingsByGenerator
"""


from lino_xl.lib.invoicing.models import InvoicingsByGenerator

InvoicingsByGenerator.column_names = (
    "voucher title qty voucher__voucher_date "
    "voucher__state product__tariff__number_of_events *")


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
    remarks:50 checkdata.ProblemsByOwner:30
    """


class TeacherDetail(PersonDetail):
    main = PersonDetail.main + " courses"

    courses = dd.Panel("""
    courses.EntriesByTeacher
    courses.CoursesByTeacher
    """, label=dd.plugins.courses.verbose_name)

    personal = 'teacher_type national_id'


# class TeacherDetail(contacts.PersonDetail):
#     general = dd.Panel(contacts.PersonDetail.main, label=_("General"))
#     box5 = "remarks"
#     main = "general courses.CoursesByTeacher \
#     courses.EntriesByTeacher cal.GuestsByPartner"


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
    # parameters = mixins.ObservedDateRange()

    params_layout = "aged_from aged_to gender"


class PupilsByType(Pupils):
    master_key = 'pupil_type'


class EntriesByCourse(EntriesByController):
    """Shows the events linked to this course.
    """
    column_names = "start_date auto_type workflow_buttons "\
                   "start_time end_time room summary *"

    display_mode = "summary"


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
    courses.EntriesByCourse

    """, label=_("Events"))

    enrolments_top = 'enrolments_until fee:15 max_places:10 confirmed free_places:10 print_actions:15'

    more = dd.Panel("""
    # company contact_person
    state user payment_term paper_type id
    invoicing.InvoicingsByGenerator
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
            Place = rt.models.countries.Place
            Room = rt.models.cal.Room
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
    column_names = "detail_link weekdays_text:10 times_text:10 "\
                   "max_places:8 confirmed "\
                   "free_places requested trying *"

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
    library table and show all courses only for users with user_type
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
    insert_layout = """
    pupil
    places option
    remark
    request_date user
    """


class EnrolmentsByJourney(EnrolmentsByHike):
    pass


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


