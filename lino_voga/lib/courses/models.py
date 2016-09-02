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

.. xfile:: courses/Enrolment/item_description.html

     The template used to fill the items description.

"""

from __future__ import unicode_literals
from __future__ import print_function

from builtins import str

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.translation import string_concat

from lino.utils.mti import get_child
from lino.api import dd, rt

from lino.mixins import Referrable
from lino.modlib.printing.mixins import Printable
from lino_cosi.lib.invoicing.mixins import Invoiceable
from lino_cosi.lib.accounts.utils import DEBIT
from lino.utils import join_elems
from lino.modlib.printing.utils import PrintableObject

from lino_cosi.lib.courses.models import *

contacts = dd.resolve_app('contacts')

day_and_month = dd.plugins.courses.day_and_month

MAX_SHOWN = 3  # maximum number of invoiced events shown in
               # invoicing_info

# from lino.utils.media import TmpMediaFile

from lino.modlib.printing.utils import CustomBuildMethod
from lino.mixins.periods import Monthly
from lino.modlib.printing.mixins import DirectPrintAction


"""The default activity are **courses**.  a **hike** usually includes
a bus travel. One enrolment can mean several participants (seats).  A
**journey** also includes a room in a hotel.

"""
CourseAreas.clear()
add = CourseAreas.add_item
add('C', _("Courses"), 'default')    # one place per enrolment
add('H', _("Hikes"), 'hikes', 'courses.Hikes')
add('J', _("Journeys"), 'journeys', 'courses.Journeys')


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


class XlsColumn(object):

    def __init__(self, label, func, width=None, **styles):
        self.label = label
        self.func = func
        self.styles = styles
        self.width = width


class XlsTable(object):
    def __init__(self):
        self.columns = []

    def add_column(self, *args, **kwargs):
        self.columns.append(XlsColumn(*args, **kwargs))

    def write_to_sheet(self, sheet, rows):
        rowno = 1
        for i, col in enumerate(self.columns):
            # sheet.write(rowno, i, label)
            cell = sheet.cell(row=rowno, column=i+1)
            cell.value = col.label
            for k, v in col.styles.items():
                setattr(cell, k, v)
            if col.width is not None:
                sheet.column_dimensions[cell.column].width = col.width
            
        for row in rows:
            rowno += 1
            for i, col in enumerate(self.columns):
                value = col.func(row)
                # sheet.write(rowno, i, value)
                sheet.cell(row=rowno, column=i+1).value = value


class CourseToXls(CustomBuildMethod):
    """Interesting, but currently not used."""
    target_ext = '.xlsx'
    name = 'course2xls'
    label = _("Export")

    def custom_build(self, ar, obj, target):
        from openpyxl.workbook import Workbook
        from openpyxl.styles import Alignment
        events = obj.events_by_course.order_by('start_date')

        xt = XlsTable()
        
        # def func(enr):
        #     # s = ''.join([str(e) for e in enr.pupil_info])
        #     s = enr.pupil_info.text
        #     print(20160512, s, E.tostring(enr.pupil_info))
        #     return s
        # xt.add_column("Teilnehmer", func)
        xt.add_column(
            "Teilnehmer", lambda enr: enr.pupil_info.text,
            alignment=Alignment(
                horizontal="general", vertical="top",
                wrap_text=True))

        xt.add_column("Anzahl", lambda enr: enr.places)
        xt.add_column("Start", lambda enr: enr.start_date)
        xt.add_column("End", lambda enr: enr.end_date)
        xt.add_column("Invoicing", lambda enr: enr.invoicing_info.text)
        xt.add_column("Payment", lambda enr: enr.payment_info)

        for i, evt in enumerate(events):
            lbl = day_and_month(evt.start_date)

            def func(enr):
                qs = rt.modules.cal.Guest.objects.filter(
                    event=evt, partner=enr.pupil)
                n = qs.count()
                if n == 0:
                    return ''
                return n
                
            xt.add_column(
                lbl, func, alignment=Alignment(
                    vertical="center", text_rotation=90), width=4)
        xt.add_column("...", lambda enr: "")
        xt.add_column("...", lambda enr: "")
        xt.add_column("...", lambda enr: "")

        wb = Workbook()
        # sheet = wb.add_sheet(str(obj))
        ws = wb.active
        ws.title = str(obj)
        # ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
        # print(type(six.text_type('100')))
        ws.column_dimensions["A"].width = 40
        ws.row_dimensions[1].height = 30
        xt.write_to_sheet(ws, obj.enrolments)
        wb.save(target)


class TeacherType(Referrable, mixins.BabelNamed, Printable):

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'TeacherType')
        # verbose_name = _("Teacher type")
        # verbose_name_plural = _('Teacher types')
        verbose_name = _("Instructor Type")
        verbose_name_plural = _("Instructor Types")


@dd.python_2_unicode_compatible
class Teacher(contacts.Person):
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


class PupilType(Referrable, mixins.BabelNamed, Printable):

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'PupilType')
        # verbose_name = _("Pupil type")
        # verbose_name_plural = _('Pupil types')
        verbose_name = _("Participant Type")
        verbose_name_plural = _("Participant Types")


@dd.python_2_unicode_compatible
class Pupil(contacts.Person):
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

    # suggested_courses = dd.ShowSlaveTable('courses.SuggestedCoursesByPupil')

    def __str__(self):
        s = self.get_full_name(salutation=False)
        info = self.get_enrolment_info()
        if info:
            s += " ({0})".format(info)
        return s

    def get_enrolment_info(self):
        """Return a short string with some additional information about this
        pupil.

        """
        if self.pupil_type:
            return self.pupil_type.ref

    @classmethod
    def get_parameter_fields(cls, **fields):
        fields.update(
            partner_list=dd.ForeignKey(
                'lists.List', blank=True, null=True),
            course=dd.ForeignKey(
                'courses.Course', blank=True, null=True))

        return super(Pupil, cls).get_parameter_fields(**fields)

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Pupil, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.course:
            qs = qs.filter(
                Q(enrolments_by_pupil__start_date__isnull=True) |
                Q(enrolments_by_pupil__start_date__lte=dd.today()))
            qs = qs.filter(
                Q(enrolments_by_pupil__end_date__isnull=True) |
                Q(enrolments_by_pupil__end_date__gte=dd.today()))
            qs = qs.distinct()
            # qs = qs.filter(enrolments_by_pupil__course=pv.course)
            # qs = qs.filter(
            #     enrolments_by_pupil__state__in=EnrolmentStates.filter(
            #         invoiceable=True))
            qs = qs.filter(
                enrolments_by_pupil__course=pv.course,
                enrolments_by_pupil__state__in=EnrolmentStates.filter(
                    invoiceable=True))
            # qs = qs.filter(
            #     enrolments_by_pupil__state=EnrolmentStates.confirmed)
            

        if pv.partner_list:
            qs = qs.filter(list_memberships__list=pv.partner_list)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Pupil, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.course:
            yield str(pv.course)
        if pv.partner_list:
            yield str(pv.partner_list)


# class CreateInvoicesForCourse(CreateInvoice):
#     """
#     Create invoices for all participants of this course.
#     """
#     def get_partners(self, ar):
#         course = ar.selected_rows[0]
#         return [obj.pupil for obj in course.enrolment_set.filter(
#             state=EnrolmentStates.confirmed)]


class CourseType(Referrable, mixins.BabelNamed):

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'CourseType')
        verbose_name = _("Activity type")
        verbose_name_plural = _('Activity types')


class Line(Line):

    class Meta(Line.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Line')

    course_type = dd.ForeignKey('courses.CourseType', blank=True, null=True)


@dd.python_2_unicode_compatible
class Course(Referrable, Course, PrintableObject):
    """Extends the standard model by adding a field :attr:`fee`.

    Also adds a :attr:`ref` field and defines a custom :meth:`__str__`
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


    .. attribute:: fee

        The default participation fee to apply for new enrolments.

    """
    class Meta(Course.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Course')
        # verbose_name = _("Activity")
        # verbose_name_plural = _('Activities')

    fee = dd.ForeignKey('products.Product',
                        blank=True, null=True,
                        verbose_name=_("Default participation fee"),
                        related_name='courses_by_fee')

    quick_search_fields = 'name line__name line__topic__name ref'

    # course2xls = CourseToXls.create_action()

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

# class CreateInvoiceForEnrolment(CreateInvoice):

#     def get_partners(self, ar):
#         return [o.pupil for o in ar.selected_rows]


class InvoicingInfo(object):
    """A volatile object which holds invoicing information about a given
    enrolment.

    .. attribute:: enrolment

        The enrolment it's all about.

    .. attribute:: max_date

        Don't consider dates after this.

    .. attribute:: invoiceable_fee

        Which fee to apply. If this is None, 

    .. attribute:: invoiced_qty

        

    """
    invoiceable_fee = None
    invoiced_qty = ZERO
    invoiced_events = 0
    used_events = []
    invoicings = None

    def __init__(self, enr, max_date=None):
        self.enrolment = enr
        self.max_date = max_date or dd.today()
        fee = enr.fee
        # fee = enr.course.fee or enr.course.line.fee
        if not fee:
            return
        if fee.min_asset is None:
            self.invoiceable_fee = fee
            return
            
        # history = []
        state_field = dd.plugins.invoicing.voucher_model._meta.get_field(
            'state')
        vstates = [s for s in state_field.choicelist.objects()
                   if not s.editable]
        # self.invoicings = enr.get_invoicings(voucher__state__in=vstates)
        self.invoicings = enr.invoicings.filter(voucher__state__in=vstates)
        if enr.free_events:
            self.invoiced_events += enr.free_events
        for obj in self.invoicings:
            if obj.product is not None:
                self.invoiced_qty += obj.qty
                if obj.product.number_of_events:
                    self.invoiced_events += int(
                        obj.qty * obj.product.number_of_events)
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
                start_date__lte=self.max_date,
                state=rt.models.cal.EventStates.took_place)
            if enr.end_date:
                qs = qs.filter(start_date__lte=enr.end_date)
            # Note that this query works only on the start_date of
            # events. If we want to filter on end_date, then don't
            # forget this field can be empty.
            self.used_events = qs.order_by('start_date')
            # print("20160414 c", self.used_events)
            # used_events = qs.count()
            # paid_events = invoiced_qty * fee.number_of_events
            asset = self.invoiced_events - self.used_events.count()
        else:
            asset = self.invoiced_qty
        # dd.logger.info("20160223 %s %s %s", enr, asset, fee.min_asset)
        if self.enrolment.end_date \
           and self.enrolment.end_date < self.max_date and asset >= 0:
            # ticket #1040 : a participant who declared to stop before
            # their asset got negative should not get any invoice for
            # a next asset
            return 
        if asset < fee.min_asset:
            self.invoiceable_fee = fee
            # self.invoiced_events = invoiced_events

    def as_html(self, ar):
        elems = []
        events = list(self.used_events)
        invoiced = events[self.invoiced_events:]
        coming = events[:self.invoiced_events]

        def fmt(ev):
            txt = day_and_month(ev.start_date)
            if ar is None:
                return txt
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
            if voucher and item.voucher.id == voucher.id:
                break
        return n


class Enrolment(Enrolment, Invoiceable):
    """Adds

    .. attribute:: fee

        The participation fee to apply for this enrolment.

    .. attribute:: free_events

        Number of events to add for first invoicing for this
        enrolment.

    .. attribute:: amount

        The total amount to pay for this enrolment. This is
        :attr:`places` * :attr:`fee`.

    .. attribute:: pupil_info

        Show the name and address of the participant.  Overrides
        :attr:`lino_cosi.lib.courses.models.Enrolment.pupil_info`
        in order to add (between parentheses after the name) some
        information needed to compute the price.

    .. attribute:: invoicing_info

        A virtual field showing a summary of recent invoicings.

    .. attribute:: payment_info

        A virtual field showing a summary of due accounting movements
        (debts and payments).

    """

    invoiceable_date_field = 'request_date'
    _invoicing_info = None

    class Meta:
        app_label = 'courses'
        abstract = False  # dd.is_abstract_model(__name__, 'Enrolment')
        verbose_name = _("Enrolment")
        verbose_name_plural = _("Enrolments")

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    fee = dd.ForeignKey('products.Product',
                        blank=True, null=True,
                        # verbose_name=_("Participation fee"),
                        related_name='enrolments_by_fee')

    free_events = models.IntegerField(
        pgettext("in an enrolment", "Free events"),
        null=True, blank=True,
        help_text=_("Number of events to add for first invoicing "
                    "for this enrolment."))

    # create_invoice = CreateInvoiceForEnrolment()

    def get_invoiceable_partner(self):
        return self.pupil.invoice_recipient or self.pupil

    # @classmethod
    # def get_invoiceable_partners(cls):
    #     return rt.models.courses.Pupil.objects.all()

    @classmethod
    def get_invoiceables_for_plan(cls, plan, partner=None):
        """Yield all enrolments for which the given plan and partner should
        generate an invoice.

        """
        qs = cls.objects.filter(**{
            cls.invoiceable_date_field + '__lte': plan.max_date or plan.today})
        if plan.course is not None:
            qs = qs.filter(course__id=plan.course.id)
        else:
            qs = qs.filter(course__state=CourseStates.active)
        if partner is None:
            partner = plan.partner
        if partner:
            pupil = get_child(partner, rt.models.courses.Pupil)
            # pupil = partner.get_mti_child('pupil')
            if pupil:  # isinstance(partner, rt.models.courses.Pupil):
                q1 = models.Q(
                    pupil__invoice_recipient__isnull=True, pupil=pupil)
                q2 = models.Q(pupil__invoice_recipient=partner)
                qs = cls.objects.filter(models.Q(q1 | q2))
            else:
                # if the partner is not a pupil, then it might still
                # be an invoice_recipient
                qs = cls.objects.filter(pupil__invoice_recipient=partner)
                
        # dd.logger.info("20160513 %s (%d rows)", qs.query, qs.count())
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
            self.fee = self.course.fee
            if self.fee_id is None and self.course.line_id is not None:
                self.fee = self.course.line.fee
        # if self.number_of_events is None:
        #     if self.fee_id and self.fee.number_of_events:
        #         self.number_of_events = self.fee.number_of_events
        #     self.number_of_events = self.course.max_events
        if self.amount is None:
            self.compute_amount()
        super(Enrolment, self).full_clean(*args, **kwargs)

    def pupil_changed(self, ar):
        self.compute_amount()

    def places_changed(self, ar):
        self.compute_amount()

    # def fee_changed(self, ar):
    #     if self.fee_id is not None:
    #         self.number_of_events = self.fee.number_of_events
    #     self.compute_amount()

    # def get_number_of_events(self):
    #     if self.number_of_events is not None:
    #         return self.number_of_events
    #     if self.fee_id and self.fee.number_of_events:
    #         return self.fee.number_of_events
    #     return self.course.max_events or 0

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

    def get_invoicing_info(self, max_date=None):
        if self._invoicing_info is None:
            self._invoicing_info = InvoicingInfo(self, max_date)
        # assert self._invoicing_info.max_date == max_date
        return self._invoicing_info

    def get_invoiceable_title(self, invoice=None):
        title = _("{enrolment} to {course}").format(
            enrolment=self.__class__._meta.verbose_name,
            course=self.course)
        if self.fee.number_of_events:
            info = self.get_invoicing_info()
            number = info.invoice_number(invoice)
            if number > 1:
                msg = _("[{number}] Renewal {title}")
            else:
                msg = _("[{number}] {title}")
            return msg.format(title=title, number=number)
        return title

    def get_invoiceable_qty(self):
        return self.places

    def setup_invoice_item(self, item):
        item.description = dd.plugins.jinja.render_from_request(
            None, 'courses/Enrolment/item_description.html',
            obj=self, item=item)

    def get_invoiceable_product(self, plan):
        """Return the product to use for the invoice.
        This also decides whether an invoice should be issued or not.
        """
        # dd.logger.info('20160223 %s', self.course)
        if not self.course.state.invoiceable:
            return
        if not self.state.invoiceable:
            return
        max_date = plan.max_date or plan.today

        # the following 2 lines were nonsense. it is perfectly okay to
        # write an invoice for an enrolment which starts in the
        # future.
        # if self.start_date and self.start_date > max_date:
        #     return

        # but at least for our demo fixtures we don't want invoices
        # for enrolments in the future:
        if self.request_date and self.request_date > max_date:
            return

        return self.get_invoicing_info(max_date).invoiceable_fee

    @dd.virtualfield(dd.HtmlBox(_("Participant")))
    def pupil_info(self, ar):
        if not self.pupil_id:
            return ''
        elems = []
        txt = self.pupil.get_full_name(nominative=True)
        if ar is None:
            elems = [txt]
        else:
            elems = [ar.obj2html(self.pupil, txt)]
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
        info = self.get_invoicing_info(dd.today())
        return info.as_html(ar)

    @dd.displayfield(_("Payment info"))
    def payment_info(self, ar):
        return rt.models.ledger.Movement.balance_info(
            DEBIT, partner=self.pupil, cleared=False)
        

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

