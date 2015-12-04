# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for the :mod:`lino_voga.cal` app.

This module extends :mod:`lino.modlib.cal.models`
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.modlib.cal.models import *

from lino.modlib.users.choicelists import UserProfiles

from lino.modlib.contacts.mixins import ContactRelated
from lino_cosi.lib.courses.choicelists import EnrolmentStates

courses = dd.resolve_app('courses')

# must import this to activate these workflow definitions:

from lino.modlib.cal.workflows import voga  
from lino.modlib.office.roles import OfficeUser


dd.inject_field('system.SiteConfig', 'pupil_guestrole',
                dd.ForeignKey('cal.GuestRole',
                              verbose_name=_("Guest role for pupils"),
                              related_name='pupil_guestroles',
                              blank=True, null=True))


class Room(Room, ContactRelated):

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
        s = mixins.BabelNamed.__unicode__(self)
        if self.company and self.company.city:
            s = '%s (%s)' % (self.company.city, s)
        return s

    def save(self, *args, **kwargs):
        super(Room, self). save(*args, **kwargs)

        if not self.calendar:
            return

        if not settings.SITE.loading_from_dump:

            profiles = set()
            for p in UserProfiles.items():
                if isinstance(p.role, OfficeUser):
                    profiles.add(p)
            User = settings.SITE.user_model
            for u in User.objects.filter(profile__in=profiles):
                check_subscription(u, self.calendar)


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

    def __unicode__(self):
        if self.owner is None:
            return super(Event, self).__unicode__()
        owner = self.owner._meta.verbose_name + " #" + str(self.owner.pk)
        return "%s %s" % (owner, self.summary)

    def suggest_guests(self):
        #~ print "20130722 suggest_guests"
        for g in super(Event, self).suggest_guests():
            yield g
        if self.project is None:
            return
        if not settings.SITE.site_config.pupil_guestrole:
            return
        Guest = settings.SITE.modules.cal.Guest
        for obj in self.project.enrolment_set.exclude(
                state=EnrolmentStates.cancelled):
            if obj.pupil:
                yield Guest(event=self,
                            partner=obj.pupil,
                            role=settings.SITE.site_config.pupil_guestrole)

    def get_calendar(self):
        if self.room is not None and self.room.calendar is not None:
            return self.room.calendar
        return settings.SITE.site_config.site_calendar


class MyEvents(MyEvents):
    column_names = 'when_text summary room owner workflow_buttons *'


@dd.receiver(dd.post_analyze)
def customize_cal(sender, **kw):
    site = sender

    dd.update_field(site.modules.cal.Event, 'description',
                    format="plain")

    site.modules.cal.Events.set_detail_layout('general more')
    site.modules.cal.Events.add_detail_panel('general', """
    event_type summary user
    start end
    room priority access_class transparent #rset
    owner:30 workflow_buttons:30
    description
    """, _("General"))

    site.modules.cal.Events.add_detail_panel('more', """
    id created:20 modified:20  state
    #outbox.MailsByController cal.GuestsByEvent notes.NotesByOwner
    """, _("More"))

    site.modules.cal.Events.set_insert_layout(
        """
        start end
        room
        """,
        start="start_date start_time",
        end="end_date end_time",
        window_size=(60, 'auto'))
