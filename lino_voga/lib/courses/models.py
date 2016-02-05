# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino_voga.lib.courses`.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from lino.api import dd, rt
from lino.utils import mti

from lino_cosi.lib.courses.models import *
from lino_voga.lib.contacts.models import Person

contacts = dd.resolve_app('contacts')


class TeacherType(mixins.Referrable, mixins.BabelNamed, mixins.Printable):

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'TeacherType')
        # verbose_name = _("Teacher type")
        # verbose_name_plural = _('Teacher types')
        verbose_name = _("Instructor Type")
        verbose_name_plural = _("Instructor Types")


class TeacherTypes(dd.Table):
    model = 'courses.TeacherType'
    detail_layout = """
    id name
    courses.TeachersByType
    """


class Teacher(Person):

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Teacher')
        verbose_name = _("Instructor")
        verbose_name_plural = _("Instructors")

        # verbose_name = _("Teacher")
        # verbose_name_plural = _("Teachers")

    teacher_type = dd.ForeignKey('courses.TeacherType', blank=True, null=True)

    def __unicode__(self):
        return self.get_full_name(salutation=False)


class TeacherDetail(contacts.PersonDetail):
    general = dd.Panel(contacts.PersonDetail.main, label=_("General"))
    box5 = "remarks"
    main = "general courses.CoursesByTeacher \
    courses.EventsByTeacher cal.GuestsByPartner"


class Teachers(contacts.Persons):
    model = 'courses.Teacher'
    #~ detail_layout = TeacherDetail()
    column_names = 'name_column address_column teacher_type *'
    auto_fit_column_widths = True


class TeachersByType(Teachers):
    master_key = 'teacher_type'


class PupilType(mixins.Referrable, mixins.BabelNamed, mixins.Printable):

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'PupilType')
        # verbose_name = _("Pupil type")
        # verbose_name_plural = _('Pupil types')
        verbose_name = _("Participant Type")
        verbose_name_plural = _("Participant Types")


class PupilTypes(dd.Table):
    model = 'courses.PupilType'
    detail_layout = """
    id name
    courses.PupilsByType
    """


class Pupil(Person):

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Pupil')
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        # verbose_name = _("Pupil")
        # verbose_name_plural = _("Pupils")

    pupil_type = dd.ForeignKey('courses.PupilType', blank=True, null=True)

    suggested_courses = dd.ShowSlaveTable('courses.SuggestedCoursesByPupil')

    def __unicode__(self):
        s = self.get_full_name(salutation=False)
        if self.pupil_type:
            s += " (%s)" % self.pupil_type.ref
        return s


class PupilDetail(contacts.PersonDetail):
    main = "general courses.EnrolmentsByPupil"

    general = dd.Panel(contacts.PersonDetail.main, label=_("General"))
    box5 = "remarks"

    #~ pupil = dd.Panel("""
    #~ EnrolmentsByPupil
    #~ """,label = _("Pupil"))

    #~ def setup_handle(self,lh):

        #~ lh.general.label = _("General")
        #~ lh.courses.label = _("School")
        #~ lh.notes.label = _("Notes")


class Pupils(contacts.Persons):
    model = 'courses.Pupil'
    #~ detail_layout = PupilDetail()
    column_names = 'name_column address_column pupil_type *'
    auto_fit_column_widths = True


class PupilsByType(Pupils):
    master_key = 'pupil_type'


class CourseDetail(CourseDetail):
    main = "general events enrolments more"
    general = dd.Panel("""
    line teacher name workflow_buttons
    room start_date end_date start_time end_time
    # courses.EventsByCourse
    remark #OptionsByCourse
    """, label=_("General"))

    events = dd.Panel("""
    every_unit every max_date max_events
    monday tuesday wednesday thursday friday saturday sunday
    cal.EventsByController

    """, label=_("Events"))

    enrolments = dd.Panel("""
    max_places enrolments_until tariff
    EnrolmentsByCourse:40
    """, label=_("Enrolments"))

    more = dd.Panel("""
    # company contact_person
    user id events_text
    sales.InvoicingsByInvoiceable
    """, label=_("More"))


@dd.receiver(dd.post_analyze)
def customize_courses(sender, **kw):
    rt.modules.courses.Courses.set_detail_layout(CourseDetail())

if False:

    # Exception: Cannot reuse detail_layout of <class
    # 'lino_cosi.lib.courses.models.CoursesByTeacher'> for <class
    # 'lino_cosi.lib.courses.models.CoursesBySlot'>

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
    column_names = "start_date:8 line:20 \
    room__company__city:10 weekdays_text:10 times_text:10"


class CoursesByLine(CoursesByLine):
    """Like :class:`lino_cosi.lib.courses.CoursesByLine`, but with other
    default values in the filter parameters. In Voga we want to see
    only courses for which new enrolments can happen.
    
    TODO: when Lino gets class-based user roles, move this back to the
    library table and show all courses only for users with profile
    `courses.CourseManager`.

    """
    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(CoursesByLine, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.registered)
        kw.update(active=dd.YesNo.yes)
        return kw


# class ActiveCourses(ActiveCourses):
#     column_names = 'info max_places enrolments teacher line room *'
#     hide_sums = True

