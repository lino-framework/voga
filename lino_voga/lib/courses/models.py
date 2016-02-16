# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino_voga.lib.courses`.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from lino.utils.mti import get_child
from lino.api import dd, rt
from lino.utils import mti

from lino_cosi.lib.courses.models import *
from lino_voga.lib.contacts.models import Person

contacts = dd.resolve_app('contacts')
sales = dd.resolve_app('sales')


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

from lino_cosi.lib.auto.sales.mixins import Invoiceable
from lino_cosi.lib.auto.sales.models import CreateInvoice


class CreateInvoiceForEnrolment(CreateInvoice):

    def get_partners(self, ar):
        return [o.pupil for o in ar.selected_rows]


class Enrolment(Enrolment, Invoiceable):
    """Adds"""
    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Enrolment')
        verbose_name = _("Enrolment")
        verbose_name_plural = _("Enrolments")

    amount = dd.PriceField(_("Participation fee"), blank=True, null=True)

    create_invoice = CreateInvoiceForEnrolment()

    def full_clean(self, *args, **kwargs):
        if self.amount is None:
            self.compute_amount()
        super(Enrolment, self).full_clean(*args, **kwargs)

    def pupil_changed(self, ar):
        self.compute_amount()

    def compute_amount(self):
        #~ if self.course is None:
            #~ return
        tariff = self.get_invoiceable_product()
        # When `products` is not installed, then tariff may be None
        # because it is a DummyField.
        self.amount = getattr(tariff, 'sales_price', ZERO)

    @classmethod
    def get_invoiceable_partners(cls):
        return rt.modules.courses.Pupil.objects.all()

    @classmethod
    def get_invoiceables_for_partner(cls, partner, max_date=None):
        pupil = get_child(partner, rt.modules.courses.Pupil)
        # pupil = partner.get_mti_child('pupil')
        # dd.logger.info('20160216 get_invoiceables_for_partner %s', partner.__class__)
        if pupil:  # isinstance(partner, rt.modules.courses.Pupil):
            q1 = models.Q(pupil__invoice_recipient__isnull=True, pupil=pupil)
            q2 = models.Q(pupil__invoice_recipient=partner)
            return cls.objects.filter(models.Q(q1 | q2))
            # ,invoice__isnull=True))

    @classmethod
    def unsued_get_partner_filter(cls, partner):
        q1 = models.Q(pupil__invoice_recipient__isnull=True, pupil=partner)
        q2 = models.Q(pupil__invoice_recipient=partner)
        return models.Q(q1 | q2)  # , invoice__isnull=True)

    def get_invoiceable_amount(self):
        return self.amount

    def get_invoiceable_product(self):
        if not self.state.invoiceable:
            return
        tariff = self.course.tariff or self.course.line.tariff
        if not tariff or not tariff.number_of_events:
            return tariff
        qs = self.course.events_by_course.filter(
            start_date__gte=self.start_date,
            state=rt.modules.cal.EventStates.took_place)
        if self.end_date:
            qs = qs.filter(end_date__lte=self.end_date)
        used_events = qs.count()
        paid_events = self.get_invoicings().count() * tariff.number_of_events
        asset = paid_events - used_events
        if asset < tariff.min_asset:
            return tariff

    def get_invoiceable_title(self):
        return self.course

    def get_invoiceable_qty(self):
        return self.places


Enrolments.detail_layout = """
    request_date user
    course pupil
    remark amount workflow_buttons
    confirmation_details sales.InvoicingsByInvoiceable
    """


class EnrolmentsByOption(Enrolments):
    master_key = 'option'
    column_names = 'course pupil remark amount request_date *'
    order_by = ['request_date']
    

class PendingRequestedEnrolments(PendingRequestedEnrolments):
    column_names = 'request_date course pupil remark user ' \
                   'amount workflow_buttons'


class EnrolmentsByPupil(EnrolmentsByPupil):
    column_names = 'request_date course user:10 remark ' \
                   'amount:10 workflow_buttons *'


class EnrolmentsByCourse(EnrolmentsByCourse):
    column_names = 'request_date pupil_info option remark ' \
                   'amount:10 workflow_buttons *'


from lino_voga.lib.contacts.models import MyPersonDetail


class PupilDetail(MyPersonDetail):

    main = 'general courses sales ledger more'

    personal = 'pupil_type'

    courses = dd.Panel("""
    courses.SuggestedCoursesByPupil
    courses.EnrolmentsByPupil
    """, label=dd.plugins.courses.verbose_name)


class TeacherDetail(MyPersonDetail):
    main = MyPersonDetail.main + " courses"
    personal = 'teacher_type'

    courses = dd.Panel("""
    courses.EventsByTeacher
    courses.CoursesByTeacher
    """, label=dd.plugins.courses.verbose_name)


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
    model = 'courses.Pupil'
    detail_layout = PupilDetail()
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


Courses.detail_layout = CourseDetail()

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


dd.inject_field(
    'products.Product', 'number_of_events',
    models.IntegerField(
        _("Number of events"), null=True, blank=True,
        help_text=_("Number of events paid per invoicing.")))

dd.inject_field(
    'products.Product', 'min_asset',
    models.IntegerField(
        _("Invoice threshold"), null=True, blank=True,
        help_text=_("Minimum number of events to pay in advance.")))
