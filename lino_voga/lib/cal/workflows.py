# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
#
# This file is part of Lino XL.
#
# Lino XL is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino XL is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino XL.  If not, see
# <http://www.gnu.org/licenses/>.
"""
Defines the default calendar workflows for :ref:`voga`.

"""

from __future__ import unicode_literals

from lino_xl.lib.cal.workflows import *
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

GuestStates.clear()
add = GuestStates.add_item
add('10', _("Invited"), 'invited', button_text="☐")
add('40', _("Present"), 'present', afterwards=True, button_text="☑")
add('50', _("Absent"), 'absent', afterwards=True, button_text="☉")
add('60', _("Excused"), 'excused', button_text="⚕")
# add('10', "☐", 'invited')
# add('40', "☑", 'present', afterwards=True)
# add('50', "☉", 'absent', afterwards=True)
# add('60', "⚕", 'excused')


@dd.receiver(dd.pre_analyze)
def my_event_workflows(sender=None, **kw):

    GuestStates.present.add_transition(
        # "\u2611",  # BALLOT BOX WITH CHECK
        required_states='invited')
        # help_text=_("Participant was present."))

    GuestStates.absent.add_transition(
        # "☉",  # 2609 SUN
        required_states='invited')
        # help_text=_("Participant was absent."))

    GuestStates.excused.add_transition(
        # "⚕",  # 2695
        required_states='invited')
        # help_text=_("Participant was excused."))

    GuestStates.invited.add_transition(
        # "☐",  # BALLOT BOX \u2610
        required_states='absent present excused')
        # help_text=_("Reset state to invited."))

    # sender.modules.cal.Event.find_next_date = FindNextDate()

    EventStates.suggested.add_transition(
        # "?",
        # _("Reset"),
        required_states='draft took_place cancelled')
        # help_text=_("Set to suggested state."))

    EventStates.draft.add_transition(
        # "\u2610",  # BALLOT BOX
        required_states='suggested took_place cancelled')
        # help_text=_("Set to draft state."))

    EventStates.took_place.add_transition(
        # "\u2611",  # BALLOT BOX WITH CHECK
        required_states='suggested draft cancelled')
        # help_text=_("Event took place."))
        #icon_name='emoticon_smile')
    #~ EventStates.absent.add_transition(states='published',icon_file='emoticon_unhappy.png')
    #~ EventStates.rescheduled.add_transition(_("Reschedule"),
        #~ states='published',icon_file='date_edit.png')
    EventStates.cancelled.add_transition(
        # "\u2609",  # SUN
        # pgettext("calendar event action", "Cancel"),
        #~ owner=True,
        # help_text=_("Event was cancelled."),
        required_states='suggested draft took_place')
        # icon_name='cross')
    # EventStates.omitted.add_transition(
    #     pgettext("calendar event action", "Omit"),
    #     states='suggested draft took_place',
    #     icon_name='date_delete')
    # EventStates.suggested.add_transition(
    #     _("Reset"),
    #     required_states='draft took_place cancelled',
    #     help_text=_("Reset to 'suggested' state."))
