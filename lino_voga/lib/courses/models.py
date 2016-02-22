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
Database models for `lino_voga.lib.courses`.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from lino.utils.mti import get_child
from lino.api import dd, rt
from lino.utils import mti

from lino_cosi.lib.courses.models import *
from lino_cosi.lib.auto.sales.mixins import Invoiceable
from lino_cosi.lib.auto.sales.models import CreateInvoice

from lino_voga.lib.contacts.models import Person
from lino_voga.lib.contacts.models import MyPersonDetail

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


class CreateInvoicesForCourse(CreateInvoice):
    """
    Create invoices for all participants of this course.
    """
    def get_partners(self, ar):
        course = ar.selected_rows[0]
        return [obj.pupil for obj in course.enrolment_set.filter(
            state=EnrolmentStates.confirmed)]


class Course(Course):
    """Extends the standard model by adding an action.

    .. attribute:: fee

        The default participation fee to apply for new enrolments.


    """
    class Meta(Course.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Course')

    fee = dd.ForeignKey('products.Product',
                        blank=True, null=True,
                        verbose_name=_("Default participation fee"),
                        related_name='courses_by_fee')

    create_invoices = CreateInvoicesForCourse()
    """See :class:`CreateInvoicesForCourse`."""

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(Course, cls).get_registrable_fields(site):
            yield f
        yield 'fee'

    @dd.chooser()
    def fee_choices(cls, line):
        Product = rt.modules.products.Product
        if not line or not line.fees_cat:
            return Product.objects.none()
        return Product.objects.filter(cat=line.fees_cat)


class CreateInvoiceForEnrolment(CreateInvoice):

    def get_partners(self, ar):
        return [o.pupil for o in ar.selected_rows]


class Enrolment(Enrolment, Invoiceable):
    """Adds

    .. attribute:: fee

        The participation fee to apply for this enrolment.


    .. attribute:: amount

        The total amount to pay for this enrolment. This is
        :attr:`places` * :attr:`fee`.

    """
    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Enrolment')
        verbose_name = _("Enrolment")
        verbose_name_plural = _("Enrolments")

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    fee = dd.ForeignKey('products.Product',
                        blank=True, null=True,
                        verbose_name=_("Participation fee"),
                        related_name='enrolments_by_fee')

    create_invoice = CreateInvoiceForEnrolment()

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

    @dd.chooser()
    def fee_choices(cls, course):
        Product = rt.modules.products.Product
        if not course or not course.line or not course.line.fees_cat:
            return Product.objects.none()
        return Product.objects.filter(cat=course.line.fees_cat)

    def full_clean(self, *args, **kwargs):
        if self.fee_id is None and self.course_id is not None:
            self.fee_id = self.course.fee_id
            if self.fee_id is None and self.course.line_id is not None:
                self.fee_id = self.course.line.fee_id
        if self.amount is None:
            self.compute_amount()
        super(Enrolment, self).full_clean(*args, **kwargs)

    def pupil_changed(self, ar):
        self.compute_amount()

    def places_changed(self, ar):
        self.compute_amount()

    def get_invoiceable_amount(self):
        return self.amount

    def compute_amount(self):
        #~ if self.course is None:
            #~ return
        if self.places is None:
            return
        # fee = self.course.fee or self.course.line.fee
        # fee = self.get_invoiceable_product()
        if self.fee is None:
            return
        # When `products` is not installed, then fee may be None
        # because it is a DummyField.
        price = getattr(self.fee, 'sales_price') or ZERO
        self.amount = price * self.places

    def get_invoiceable_product(self):
        if not self.state.invoiceable:
            return
        fee = self.fee
        # fee = self.course.fee or self.course.line.fee
        if not fee:
            return
        invoiced_qty = ZERO
        for obj in self.get_invoicings():
            invoiced_qty += obj.qty
        if not fee.number_of_events:
            if invoiced_qty:
                return
            return fee
        qs = self.course.events_by_course.filter(
            start_date__gte=self.start_date,
            state=rt.modules.cal.EventStates.took_place)
        if self.end_date:
            qs = qs.filter(end_date__lte=self.end_date)
        used_events = qs.count()
        paid_events = invoiced_qty * fee.number_of_events
        asset = paid_events - used_events
        if asset < fee.min_asset:
            return fee

    def get_invoiceable_title(self):
        return self.course

    def get_invoiceable_qty(self):
        return self.places

    def setup_invoice_item(self, item):
        item.description = dd.plugins.jinja.render_from_request(
            None, 'courses/Enrolment/item_description.html',
            obj=self, item=item)

Enrolments.detail_layout = """
    request_date user course
    pupil places fee option
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
    column_names = 'request_date pupil_info places ' \
                   'fee option remark amount:10 workflow_buttons *'


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
    max_places enrolments_until fee
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


# dd.inject_field(
#     'products.Product', 'number_of_events',
#     models.IntegerField(
#         _("Number of events"), null=True, blank=True,
#         help_text=_("Number of events paid per invoicing.")))

# dd.inject_field(
#     'products.Product', 'min_asset',
#     models.IntegerField(
#         _("Invoice threshold"), null=True, blank=True,
#         help_text=_("Minimum number of events to pay in advance.")))