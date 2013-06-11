## Copyright 2013 Luc Saffre
## This file is part of the Lino-Faggio project.
## Lino-Faggio is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-Faggio is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.db.models import loading
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from django.contrib.contenttypes.models import ContentType


from lino import dd
from lino import mixins
#~ from lino.models import SiteConfig

#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.cal import models as cal

contacts = dd.resolve_app('contacts')
ledger = dd.resolve_app('ledger')
sales = dd.resolve_app('sales')
#~ cal = dd.resolve_app('cal')
school = dd.resolve_app('school')

#~ print 20130607, loading.cache.postponed

    
class AutoFillAction(dd.RowAction):
    label = _("Fill")
    
    def run_from_ui(self,obj,ar,**kw):
        L = list(sales.Invoiceable.get_invoiceables_for(obj.partner,obj.date))
        if len(L) == 0:
            return ar.error(_("No invoiceables found for %s.") % obj.partner)
        def ok():
            for ii in L:
                i = InvoiceItem(voucher=obj,invoiceable=ii,product=ii.get_invoiceable_product())
                i.product_changed(ar)
                i.full_clean()
                i.save()
            kw.update(refresh=True)
            return kw
        msg = _("This will add %d invoice items.") % len(L)
        return ar.confirm(ok, msg, _("Are you sure?"))
    
    
class Invoice(sales.Invoice):
    
    auto_fill = AutoFillAction()
    
    class Meta(sales.Invoice.Meta):
        app_label = 'sales'
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
    
class InvoiceItem(sales.InvoiceItem):
    
    invoiceable_label = _("Invoiceable")
    
    class Meta(sales.InvoiceItem.Meta):
        app_label = 'sales'
        verbose_name = _("Voucher item")
        verbose_name_plural = _("Voucher items")
    
    
    invoiceable_type = dd.ForeignKey(ContentType,
        editable=False,blank=True,null=True,
        verbose_name=string_concat(invoiceable_label,' ',_('(type)')))
    invoiceable_id = dd.GenericForeignKeyIdField(
        invoiceable_type,
        editable=False,blank=True,null=True,
        verbose_name=string_concat(invoiceable_label,' ',_('(object)')))
    invoiceable = dd.GenericForeignKey(
        'invoiceable_type', 'invoiceable_id',
        verbose_name=invoiceable_label)
    
    #~ @dd.chooser()
    #~ def enrolment_choices(self,voucher):
        #~ Enrolment = dd.resolve_model('school.Enrolment')
        #~ # print 20130605, voucher.partner.pk
        #~ return Enrolment.objects.filter(pupil__id=voucher.partner.pk).order_by('request_date')
        #~ 
    #~ def enrolment_changed(self,ar):
        #~ if self.enrolment is not None and self.enrolment.course is not None:
            #~ self.product = self.enrolment.course.tariff
        #~ self.product_changed(ar)
    
class ItemsByInvoice(sales.ItemsByInvoice):
    app_label = 'sales' # we want to "override" the original table

    column_names = "invoiceable product title description:20x1 discount unit_price qty total_incl total_base total_vat"
    
    #~ @classmethod
    #~ def get_choices_text(self,obj,request,field):
        #~ if field.name == 'enrolment':
            #~ return unicode(obj.course)
        #~ # raise Exception("20130607 field.name is %r" % field.name)
        #~ return super(ItemsByInvoice,self).get_choices_text(obj,field,request)
    
#~ class InvoicingsByEnrolment(sales.InvoiceItemsByProduct):
    #~ app_label = 'sales'
    #~ master_key = 'enrolment'
    #~ editable = False
    #~ 
class InvoicingsByInvoiceable(sales.InvoiceItemsByProduct):
    app_label = 'sales'
    master_key = 'invoiceable'
    editable = False
    
#~ sales.ItemsByInvoice.column_names = "enrolment product title description:20x1 discount unit_price qty total_incl total_base total_vat"
    

dd.inject_field('school.Course',
    'tariff',
    models.ForeignKey('products.Product',
        blank=True,null=True,
        verbose_name=_("Tariff"),
        related_name='courses_by_tariff'))
        
class ActiveCourses(school.ActiveCourses):
    app_label = 'school'
    column_names = 'info tariff max_places enrolments teacher company room'
    hide_sums = True

class CourseDetail(school.CourseDetail):     
    main = "general cal.EventsByController"
    general = dd.Panel("""
    line teacher start_date start_time room #slot state id:8
    max_places max_events end_date end_time every_unit every
    monday tuesday wednesday thursday friday saturday sunday
    company contact_person user calendar tariff
    school.EnrolmentsByCourse
    """,label=_("General"))
    

@dd.receiver(dd.post_analyze)
def customize_school(sender,**kw):
    site = sender
    site.modules.school.Courses.set_detail_layout(CourseDetail())
    #~ site.modules.school.ActiveCourses.column_names = 'info tariff max_places enrolments teacher company room'
     
#~ def site_setup(site):
@dd.receiver(dd.post_analyze)
def customize_cal(sender,**kw):
    site = sender
    
    #~ site.modules.cal.Events.set_detail_layout(EventDetail())
    site.modules.cal.Events.set_detail_layout('general more')
    site.modules.cal.Events.add_detail_panel('general',"""
    calendar summary user project 
    start end 
    room priority access_class transparent #rset 
    owner workflow_buttons
    description cal.GuestsByEvent 
    """,_("General"))
    
    site.modules.cal.Events.add_detail_panel('more',"""
    id created:20 modified:20  
    outbox.MailsByController #postings.PostingsByController
    """,_("More"))
    
    
    site.modules.cal.Events.set_insert_layout("""
    project 
    start end 
    """,
    start="start_date start_time",
    end="end_date end_time",
    window_size=(60,'auto'))
    

class PrintAndChangeStateAction(dd.ChangeStateAction):
    
    def run_from_ui(self,obj,ar,**kw):
        
        def ok():
            # to avoid UnboundLocalError local variable 'kw' referenced before assignment
            kw2 = obj.do_print.run_from_session(ar,**kw)
            kw2 = super(PrintAndChangeStateAction,self).run_from_ui(obj,ar,**kw2)
            kw2.update(refresh_all=True)
            return kw2
        msg = self.get_confirmation_message(obj,ar)
        return ar.confirm(ok, msg, _("Are you sure?"))
    
class ConfirmEnrolment(PrintAndChangeStateAction):
    required = dd.required(states='requested')
    label = _("Confirm")
    
    def get_confirmation_message(self,obj,ar):
        return _("Confirm enrolment of <b>%(pupil)s</b> to <b>%(course)s</b>.") % dict(
            pupil=obj.pupil,course=obj.course)        
    
class CertifyEnrolment(PrintAndChangeStateAction):
    required = dd.required(states='confirmed')
    label = _("Certify")
    #~ label = _("Award")
    #~ label = school.EnrolmentStates.award.text
    
    def get_confirmation_message(self,obj,ar):
        return _("Print certificate for <b>%(pupil)s</b>.") % dict(
            pupil=obj.pupil,course=obj.course)
    

@dd.receiver(dd.pre_analyze,dispatch_uid='faggio_setup_workflows')
def faggio_setup_workflows(sender,**kw):
    
    site = sender
    school = dd.resolve_app('school')

    #~ from lino.modlib.school import models as school
    school.EnrolmentStates.confirmed.add_transition(ConfirmEnrolment)
    school.EnrolmentStates.certified.add_transition(CertifyEnrolment) 
    #~ school.EnrolmentStates.abandoned.add_transition() 


@dd.when_prepared('partners.Person','partners.Organisation')
def hide_region(model):
    model.hide_elements('region')

@dd.when_prepared('partners.Person','partners.Organisation')
def add_merge_action(model):
    model.define_action(merge_row=dd.MergeAction(model))
        
