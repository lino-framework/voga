# -*- coding: UTF-8 -*-
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
This module extends :mod:`lino.modlib.cal.models`
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import dd

#~ dd.extends_app('lino.modlib.cal',globals())

#~ PARENT_APP = 'lino.modlib.cal'
from lino.modlib.cal.models import *

from lino.modlib.cal.workflows import faggio


#~ sales = dd.resolve_app('sales')

class Room(Room,contacts.ContactRelated):
    #~ class Meta(Room.Meta):
        #~ app_label = 'cal'
        
    tariff = dd.ForeignKey('products.Product',
        blank=True,null=True,
        verbose_name=_("Tariff"),
        related_name='rooms_by_tariff')
        
    def __unicode__(self):
        s = dd.BabelNamed.__unicode__(self)
        if self.company and self.company.city: 
            s = '%s (%s)' % (self.company.city,s)
        return s
        
class Rooms(Rooms):
    detail_layout = """
    id name 
    tariff company contact_person contact_role
    cal.EventsByRoom
    """

    

#~ class Event(Event,sales.Invoiceable):
class Event(Event):
    
    #~ class Meta(Event.Meta):
        #~ app_label = 'cal'
        
    #~ organizer = dd.ForeignKey('contacts.Partner',
        #~ verbose_name=_("Organizer"),
        #~ blank=True,null=True)
        
    invoiceable_date_field = 'start_date'
    #~ invoiceable_partner_field = 'organizer'
    invoiceable_partner_field = 'company'
    
    def get_invoiceable_product(self): 
        #~ if self.organizer and self.room: 
        if self.company and self.room: 
            #~ return products.Product.objects.get(pk=1) # todo : Tarife Raummiete
            return self.room.tariff
            
    def get_invoiceable_title(self): 
        #~ if self.organizer: 
        if self.company: 
            return unicode(self.room)

    def get_invoiceable_qty(self): 
        return 1
    
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
    id created:20 modified:20  state
    outbox.MailsByController #postings.PostingsByController
    """,_("More"))
    
    
    site.modules.cal.Events.set_insert_layout("""
    project 
    start end 
    """,
    start="start_date start_time",
    end="end_date end_time",
    window_size=(60,'auto'))
    

