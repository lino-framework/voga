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

"""
The :xfile:`models.py` for the :mod:`lino_faggio` app.
"""

from django.db import models
from django.db.models import loading
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat



from lino import dd
from lino import mixins
#~ from lino.models import SiteConfig

#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.cal import models as cal

contacts = dd.resolve_app('contacts')
ledger = dd.resolve_app('ledger')
#~ cal = dd.resolve_app('cal')
courses = dd.resolve_app('courses')
products = dd.resolve_app('products')
notes = dd.resolve_app('notes')

#~ print 20130607, loading.cache.postponed

    
#~ notes.Note._meta.verbose_name = _("Note")
#~ notes.Note._meta.verbose_name_plural = _("Notes")

        
        

#~ from lino.modlib.cal import models as cal

#~ dd.inject_field('cal.Room','price',dd.PriceField(verbose_name=_("Price"),
    #~ blank=True,null=True,
    #~ default=0))
    
     

#~ @dd.receiver(dd.pre_analyze,dispatch_uid='faggio_setup_workflows')
#~ def faggio_setup_workflows(sender,**kw):
    #~ 
    #~ site = sender
    #~ courses = dd.resolve_app('courses')
#~ 
    #~ courses.EnrolmentStates.confirmed.add_transition(_("Confirm"))
    #~ courses.EnrolmentStates.certified.add_transition(CertifyEnrolment) 
    
from lino.modlib.courses import workflows
    


@dd.when_prepared('partners.Person','partners.Organisation')
def hide_region(model):
    model.hide_elements('region')

@dd.when_prepared('partners.Person','partners.Organisation')
def add_merge_action(model):
    model.define_action(merge_row=dd.MergeAction(model))
    
    
   
def site_setup(site):
    site.modules.accounts.Accounts.set_detail_layout(
        """
        ref:10 name id:5
        seqno chart group type clearable
        ledger.MovementsByAccount #ledger.DuePaymentsByAccount
        """)
    
    site.modules.system.SiteConfigs.set_detail_layout(
        """
        site_company next_partner_id:10
        default_build_method 
        clients_account   sales_account     sales_vat_account
        suppliers_account purchases_account purchases_vat_account
        pupil_guestrole
        """)
    
    
        

"""
The following trick worked but was rather hackerish. 
Now we have :meth:`lino.modlib.vat.SiteMixin.get_item_vat`.
"""
if False:

    sales = dd.resolve_app('sales')

    @dd.receiver(dd.post_init, sender=sales.Invoice)
    def set_default_item_vat(sender, instance=None,**kwargs):
        instance.item_vat = True

