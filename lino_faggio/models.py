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
Deserves a docstring.
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

#~ print 20130607, loading.cache.postponed

    

        
        

#~ from lino.modlib.cal import models as cal

#~ dd.inject_field('cal.Room','price',dd.PriceField(verbose_name=_("Price"),
    #~ blank=True,null=True,
    #~ default=0))
    
     
class PrintAndChangeStateAction(dd.ChangeStateAction):
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        
        def ok():
            # to avoid UnboundLocalError local variable 'kw' referenced before assignment
            kw2 = obj.do_print.run_from_ui(ar,**kw)
            kw2 = super(PrintAndChangeStateAction,self).run_from_ui(ar,**kw2)
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
    courses = dd.resolve_app('courses')

    #~ from lino.modlib.courses import models as courses
    #~ courses.EnrolmentStates.confirmed.add_transition(ConfirmEnrolment)
    courses.EnrolmentStates.confirmed.add_transition(_("Confirm"))
    courses.EnrolmentStates.certified.add_transition(CertifyEnrolment) 
    #~ courses.EnrolmentStates.abandoned.add_transition() 


@dd.when_prepared('partners.Person','partners.Organisation')
def hide_region(model):
    model.hide_elements('region')

@dd.when_prepared('partners.Person','partners.Organisation')
def add_merge_action(model):
    model.define_action(merge_row=dd.MergeAction(model))
        
