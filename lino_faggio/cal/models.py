# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino-Faggio project.
# Lino-Faggio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino-Faggio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.

"""
The :xfile:`models.py` module for the :mod:`lino_faggio.cal` app.

This module extends :mod:`lino.modlib.cal.models`
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import dd

from lino.modlib.cal.models import *

contacts = dd.resolve_app('contacts')
courses = dd.resolve_app('courses')

# must import this to activate these workflow definitions:
from lino.modlib.cal.workflows import faggio  

dd.inject_field('system.SiteConfig', 'pupil_guestrole',
                dd.ForeignKey('cal.GuestRole',
                              verbose_name=_("Guest role for pupils"),
                              related_name='pupil_guestroles',
                              blank=True, null=True))


class Room(Room, contacts.ContactRelated):

    tariff = dd.ForeignKey('products.Product',
                           blank=True, null=True,
                           verbose_name=_("Tariff"),
                           related_name='rooms_by_tariff')

    calendar = dd.ForeignKey(
        'cal.Calendar',
        help_text=_("Calendar where events in this room are published."),
        related_name='room_calendars',
        blank=True, null=True)

    def __unicode__(self):
        s = dd.BabelNamed.__unicode__(self)
        if self.company and self.company.city:
            s = '%s (%s)' % (self.company.city, s)
        return s


class Rooms(Rooms):
    column_names = "name calendar tariff company company__city *"
    detail_layout = """
    id name calendar
    tariff company contact_person contact_role
    cal.EventsByRoom
    """


class Event(Event):

    invoiceable_date_field = 'start_date'
    invoiceable_partner_field = 'company'

    def get_invoiceable_product(self):
        if self.company and self.room:
            return self.room.tariff

    def get_invoiceable_title(self):
        if self.company:
            return unicode(self.room)

    def get_invoiceable_qty(self):
        return 1

    def get_event_summary(self, ar):
        """Overrides :meth:`lino.modlib.cal.models.Event.get_event_summary`
        """
        if self.owner is None:
            return self.summary
        else:
            return unicode(self.owner)

    def suggest_guests(self):
        #~ print "20130722 suggest_guests"
        for g in super(Event, self).suggest_guests():
            yield g
        if self.project is None:
            return
        if not settings.SITE.site_config.pupil_guestrole:
            return
        Guest = settings.SITE.modules.cal.Guest
        for obj in self.project.enrolment_set.exclude(state=courses.EnrolmentStates.cancelled):
            if obj.pupil:
                yield Guest(event=self,
                            partner=obj.pupil,
                            role=settings.SITE.site_config.pupil_guestrole)

    def get_calendar(self):
        """
        This is how :ref:`faggio` 
        """
        if self.room is not None and self.room.calendar is not None:
            return self.room.calendar
        return settings.SITE.site_config.site_calendar


#~ def site_setup(site):
@dd.receiver(dd.post_analyze)
def customize_cal(sender, **kw):
    site = sender

    dd.update_field(site.modules.cal.Event, 'description',
                    format="plain")

    #~ site.modules.cal.Events.set_detail_layout(EventDetail())
    site.modules.cal.Events.set_detail_layout('general more')
    site.modules.cal.Events.add_detail_panel('general', """
    event_type summary user course
    start end
    room priority access_class transparent #rset
    owner:30 workflow_buttons:30
    description
    """, _("General"))

    site.modules.cal.Events.add_detail_panel('more', """
    id created:20 modified:20  state
    #outbox.MailsByController cal.GuestsByEvent notes.NotesByOwner
    """, _("More"))

    site.modules.cal.Events.set_insert_layout("""
    start end
    course
    """,
                                              start="start_date start_time",
                                              end="end_date end_time",
                                              window_size=(60, 'auto'))
