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
from builtins import str
import datetime
import six

from django.utils.translation import ugettext_lazy as _
from lino.utils.mti import get_child
from lino.api import dd, rt

from lino.modlib.printing.mixins import Printable
from lino_cosi.lib.courses.models import *
from lino_cosi.lib.invoicing.mixins import Invoiceable
from lino_cosi.lib.accounts.utils import DEBIT, CREDIT


from lino_voga.lib.contacts.models import Person
from lino_voga.lib.contacts.models import MyPersonDetail

contacts = dd.resolve_app('contacts')
# sales = dd.resolve_app('sales')

day_and_month = dd.plugins.courses.day_and_month

MAX_SHOWN = 3  # maximum number of invoiced events shown in
               # invoicing_info


class TeacherType(mixins.Referrable, mixins.BabelNamed, Printable):

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


@dd.python_2_unicode_compatible
class Teacher(Person):
    """A **teacher** is a person with an additional field
    :attr:`teacher_type`.

    .. attribute:: teacher_type

        Pointer to :class:`TeacherType`.

    """
    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Teacher')
        verbose_name = _("Instructor")
        verbose_name_plural = _("Instructors")

        # verbose_name = _("Teacher")
        # verbose_name_plural = _("Teachers")

    teacher_type = dd.ForeignKey('courses.TeacherType', blank=True, null=True)

    def __str__(self):
        return self.get_full_name(salutation=False)


class PupilType(mixins.Referrable, mixins.BabelNamed, Printable):

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


@dd.python_2_unicode_compatible
class Pupil(Person):
    """A **pupil** is a person with an additional field
    :attr:`pupil_type`.

    .. attribute:: pupil_type

        Pointer to :class:`PupilType`.

    """

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Pupil')
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        # verbose_name = _("Pupil")
        # verbose_name_plural = _("Pupils")

    pupil_type = dd.ForeignKey('courses.PupilType', blank=True, null=True)

    suggested_courses = dd.ShowSlaveTable('courses.SuggestedCoursesByPupil')

    def __str__(self):
        s = self.get_full_name(salutation=False)
        if self.pupil_type:
            s += " (%s)" % self.pupil_type.ref
        return s

    def get_enrolment_info(self):
        if self.pupil_type:
            return self.pupil_type.ref


# class CreateInvoicesForCourse(CreateInvoice):
#     """
#     Create invoices for all participants of this course.
#     """
#     def get_partners(self, ar):
#         course = ar.selected_rows[0]
#         return [obj.pupil for obj in course.enrolment_set.filter(
#             state=EnrolmentStates.confirmed)]


class CourseType(mixins.Referrable, mixins.BabelNamed):

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'CourseType')
        verbose_name = _("Course type")
        verbose_name_plural = _('Course types')


class CourseTypes(dd.Table):
    model = 'courses.CourseType'
    detail_layout = """
    id name
    courses.LinesByType
    """


class Line(Line):

    class Meta(Line.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Line')

    course_type = dd.ForeignKey('courses.CourseType', blank=True, null=True)


Lines.detail_layout = """
    id name ref
    #course_area topic fees_cat fee options_cat body_template
    course_type event_type guest_role every_unit every
    description
    excerpt_title
    courses.CoursesByLine
    """


class Course(Course):
    """Extends the standard model by adding a field :attr:`fee`.

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


# class CreateInvoiceForEnrolment(CreateInvoice):

#     def get_partners(self, ar):
#         return [o.pupil for o in ar.selected_rows]


class InvoicingInfo(object):
    invoiceable_fee = None
    invoiced_events = 0
    used_events = []
    invoicings = None

    def __init__(self, enr):
        self.enrolment = enr
        fee = enr.fee
        # fee = enr.course.fee or enr.course.line.fee
        if not fee:
            return
        if fee.min_asset is None:
            self.invoiceable_fee = fee
            return
            
        self.invoiced_qty = ZERO
        invoiced_events = 0
        # history = []
        state_field = dd.plugins.invoicing.voucher_model._meta.get_field(
            'state')
        vstates = [s for s in state_field.choicelist.objects()
                   if not s.editable]
        self.invoicings = enr.get_invoicings(voucher__state__in=vstates)
        for obj in self.invoicings:
            self.invoiced_qty += obj.qty
            if obj.product.number_of_events:
                invoiced_events += int(obj.qty * obj.product.number_of_events)
            # history.append("".format())
        # print("20160414", self.invoicings, self.invoiced_qty)
        start_date = enr.start_date or enr.course.start_date
        # print("20160414 a", fee.number_of_events)
        if fee.number_of_events:
            # print("20160414 b", start_date)
            if not start_date:
                return
            qs = enr.course.events_by_course.filter(
                start_date__gte=start_date,
                state=rt.modules.cal.EventStates.took_place)
            if enr.end_date:
                qs = qs.filter(end_date__lte=enr.end_date)
            self.used_events = qs.order_by('start_date')
            # print("20160414 c", self.used_events)
            # used_events = qs.count()
            # paid_events = invoiced_qty * fee.number_of_events
            asset = invoiced_events - self.used_events.count()
        else:
            asset = self.invoiced_qty
        # dd.logger.info("20160223 %s %s %s", enr, asset, fee.min_asset)
        if asset < fee.min_asset:
            self.invoiceable_fee = fee
            self.invoiced_events = invoiced_events

    def as_html(self, ar):
        if ar is None:
            return ''
        elems = []
        events = list(self.used_events)
        invoiced = events[self.invoiced_events:]
        coming = events[:self.invoiced_events]

        def fmt(ev):
            txt = day_and_month(ev.start_date)
            return ar.obj2html(ev, txt)
        if len(invoiced) > 0:
            elems.append("{0} : ".format(_("Invoiced")))
            if len(invoiced) > MAX_SHOWN:
                elems.append("(...) ")
                invoiced = invoiced[-MAX_SHOWN:]
            elems += join_elems(map(fmt, invoiced), sep=', ')
            # s += ', '.join(map(fmt, invoiced))
            # elems.append(E.p(s))
        if len(coming) > 0:
            if len(elems) > 0:
                elems.append(E.br())
            elems.append("{0} : ".format(_("Not invoiced")))
            elems += join_elems(map(fmt, coming), sep=', ')
            # s += ', '.join(map(fmt, coming))
            # elems.append(E.p(s))
        return E.p(*elems)

        # for i, ev in enumerate(self.used_events):
        #     txt = day_and_month(ev.start_date)
        #     if i >= self.invoiced_events:
        #         txt = E.b(txt)
        #     elems.append(ar.obj2html(ev, txt))
        # return E.p(*join_elems(elems, sep=', '))

    def invoice_number(self, voucher):
        if self.invoicings is None:
            return 0
        n = 1
        for item in self.invoicings:
            n += 1
            if item.voucher.id == voucher.id:
                break
        return n


class Enrolment(Enrolment, Invoiceable):
    """Adds

    .. attribute:: fee

        The participation fee to apply for this enrolment.


    .. attribute:: amount

        The total amount to pay for this enrolment. This is
        :attr:`places` * :attr:`fee`.

    .. attribute:: pupil_info

        Show the name and address of the participant.  Overrides
        :attr:`lino_cosi.lib.courses.ui.EnrolmentsByCourse.pupil_info`
        in order to add (between parentheses after the name) some
        information needed to compute the price.

    .. attribute:: invoicing_info

        A virtual field showing a summary of recent invoicings.

    .. attribute:: payment_info

        A virtual field showing a summary of due accounting movements
        (debts and payments).

    """

    invoiceable_date_field = 'request_date'

    class Meta:
        app_label = 'courses'
        abstract = False  # dd.is_abstract_model(__name__, 'Enrolment')
        verbose_name = _("Enrolment")
        verbose_name_plural = _("Enrolments")

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    fee = dd.ForeignKey('products.Product',
                        blank=True, null=True,
                        verbose_name=_("Participation fee"),
                        related_name='enrolments_by_fee')

    # create_invoice = CreateInvoiceForEnrolment()

    def get_invoiceable_partner(self):
        return self.pupil

    # @classmethod
    # def get_invoiceable_partners(cls):
    #     return rt.modules.courses.Pupil.objects.all()

    @classmethod
    def get_invoiceables_for_plan(cls, plan, partner=None):

        qs = cls.objects.filter(**{
            cls.invoiceable_date_field + '__lte': plan.max_date})
        qs = qs.filter(course__state=EnrolmentStates.confirmed)
        if partner is None:
            partner = plan.partner
        if partner:
            pupil = get_child(partner, rt.modules.courses.Pupil)
            # pupil = partner.get_mti_child('pupil')
            if pupil:  # isinstance(partner, rt.modules.courses.Pupil):
                q1 = models.Q(
                    pupil__invoice_recipient__isnull=True, pupil=pupil)
                q2 = models.Q(pupil__invoice_recipient=partner)
                qs = cls.objects.filter(models.Q(q1 | q2))
            else:
                return
        for obj in qs.order_by(cls.invoiceable_date_field):
            # dd.logger.info('20160223 %s', obj)
            yield obj

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

    def fee_changed(self, ar):
        self.compute_amount()

    def get_invoiceable_amount(self):
        return self.amount

    def compute_amount(self):
        #~ if self.course is None:
            #~ return
        if self.places is None:
            return
        if self.fee is None:
            return
        # When `products` is not installed, then fee may be None
        # because it is a DummyField.
        price = getattr(self.fee, 'sales_price') or ZERO
        try:
            self.amount = price * self.places
        except TypeError as e:
            logger.warning("%s * %s -> %s", price, self.places, e)

    def get_invoicing_info(self):
        return InvoicingInfo(self)

    def get_invoiceable_title(self, invoice):
        if self.fee.number_of_events:
            info = self.get_invoicing_info()
            return "{0}, Rg. {1}".format(
                self.course, info.invoice_number(invoice))
        return self.course

    def get_invoiceable_qty(self):
        return self.places

    def setup_invoice_item(self, item):
        item.description = dd.plugins.jinja.render_from_request(
            None, 'courses/Enrolment/item_description.html',
            obj=self, item=item)

    def get_invoiceable_product(self):
        # dd.logger.info('20160223 %s', self.course)
        if not self.course.state.invoiceable:
            return
        if not self.state.invoiceable:
            return
        return self.get_invoicing_info().invoiceable_fee

    @dd.virtualfield(dd.HtmlBox(_("Participant")))
    def pupil_info(self, ar):
        if ar is None:
            return ''
        elems = [ar.obj2html(self.pupil,
                             self.pupil.get_full_name(nominative=True))]
        info = self.pupil.get_enrolment_info()
        if info:
            # elems += [" ({})".format(self.pupil.pupil_type.ref)]
            elems += [" ({})".format(info)]
        elems += [', ']
        elems += join_elems(
            self.pupil.address_location_lines(), sep=', ')
        if self.pupil.phone:
            elems += [', ', _("Phone: {0}").format(self.pupil.phone)]
        if self.pupil.gsm:
            elems += [', ', _("GSM: {0}").format(self.pupil.gsm)]
        return E.p(*elems)

    @dd.displayfield(_("Invoicing info"))
    def invoicing_info(self, ar):
        if ar is None:
            return ''
        info = self.get_invoicing_info()
        return info.as_html(ar)

    @dd.displayfield(_("Payment info"))
    def payment_info(self, ar):
        return rt.modules.ledger.Movement.balance_info(
            DEBIT, partner=self.pupil, cleared=False)
        

# Enrolments.detail_layout = """
#     request_date user course
#     pupil places fee option
#     remark amount workflow_buttons
#     confirmation_details invoicing.InvoicingsByInvoiceable
#     """

Enrolments.detail_layout = """
id course pupil request_date user
start_date end_date places fee option amount
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


class EnrolmentsByCourse(EnrolmentsByCourse):
    """The Voga version of :class:`EnrolmentsByCourse
    <lino_cosi.lib.courses.ui.EnrolmentsByCourse>`.

    """
    variable_row_height = True
    column_names = 'request_date pupil_info start_date end_date '\
                   'places remark fee option amount ' \
                   'workflow_buttons *'

    # column_names = 'request_date pupil_info places ' \
    #                'fee option remark amount:10 workflow_buttons *'


class EnrolmentsByFee(EnrolmentsByCourse):
    label = _("Enrolments using this fee")
    master_key = "fee"
    column_names = 'course request_date pupil_info start_date end_date '\
                   'places remark option amount *'


class PupilDetail(MyPersonDetail):

    main = 'general address courses sales ledger more'

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
    """The global list of all pupils."""
    model = 'courses.Pupil'
    detail_layout = PupilDetail()
    column_names = 'name_column address_column pupil_type *'
    auto_fit_column_widths = True
    # parameters = mixins.ObservedPeriod()

    params_layout = "aged_from aged_to gender"


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
    enrolments_until fee max_places:8 free_places
    EnrolmentsByCourse:40
    """, label=_("Enrolments"))

    more = dd.Panel("""
    # company contact_person
    state user id events_text
    invoicing.InvoicingsByInvoiceable
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
    """Shows the courses of a given topic.

    This is used both in the detail window of a topic and in
    :class:`StatusReport`.

    """
    order_by = ["ref"]
    column_names = "info name weekdays_text:10 times_text:10 "\
                   "enrolments max_places:8 free_places"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(CoursesByTopic, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.active)
        kw.update(can_enroll=dd.YesNo.yes)
        return kw


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
        kw.update(state=CourseStates.active)
        kw.update(can_enroll=dd.YesNo.yes)
        return kw


class LinesByType(Lines):
    master_key = 'course_type'


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


from lino.utils.report import Report
from lino.mixins import ObservedPeriod


# class StatusCoursesByTopic(CoursesByTopic):

class StatusReport(Report):
    """Gives an overview about what's up today .

    """

    label = _("Status Report")

    # parameters = ObservedPeriod(
    #     detailed=models.BooleanField(
    #         verbose_name=_("Detailed"), default=False),
    # )

    # params_layout = "start_date end_date detailed"

    # @classmethod
    # def param_defaults(self, ar, **kw):
    #     D = datetime.date
    #     kw.update(start_date=D(D.today().year, 1, 1))
    #     kw.update(end_date=D(D.today().year, 12, 31))
    #     return kw

    @classmethod
    def get_story(cls, self, ar):
        for topic in rt.modules.courses.Topic.objects.all():
            yield E.h3(str(topic))
            yield ar.spawn(CoursesByTopic, master_instance=topic)


class EnrolmentsAndPaymentsByCourse(Enrolments):
    """Show enrolments of a course together with
    :attr:`invoicing_info` and :attr:`payment_info`.

    This is used by `payment_list.body.html`.

    

    """
    master_key = 'course'
    column_names = "pupil_info start_date invoicing_info payment_info"
