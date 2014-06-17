# -*- coding: utf-8 -*-
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

"""This module contains "quick" tests that are run on a demo database
without any fixture. You can run only these tests by issuing::

  python manage.py test lino_faggio.tests.QuickTest
  python manage.py test lino_faggio.tests.DemoTest

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from lino.runtime import cal
from lino.runtime import courses
from lino.runtime import users
# from lino.runtime import rooms
from django.conf import settings

from lino import dd
from lino.utils import i2d
from djangosite.utils.djangotest import RemoteAuthTestCase


def create(model, **kwargs):
    obj = model(**kwargs)
    obj.full_clean()
    obj.save()
    return obj
    

class QuickTest(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        # from lino.runtime import courses, users, settings
        room = create(cal.Room, name="First Room")
        et = create(cal.EventType, name="Lesson")

        line = create(courses.Line, name="First Line", event_type=et)

        obj = create(
            courses.Course,
            line=line,
            room=room,
            max_events=5,
            monday=True,
            state=courses.CourseStates.registered,
            start_date=i2d(20140110))
        self.assertEqual(unicode(obj), "First Line (1/10/14 First Room)")

        # self.assertEqual(settings.SITE.kernel.__class__.__name__, 'Kernel')
        # self.assertEqual(settings.SITE.kernel.site, settings.SITE)
        # self.assertEqual(settings.SITE, dd.site)
        # self.assertEqual(settings.SITE.plugins, dd.apps)
        # self.assertEqual(settings.SITE.plugins.extjs, dd.apps.extjs)

        settings.SITE.verbose_client_info_message = True
        users.User(username="robin",
                   profile=dd.UserProfiles.admin,
                   language="en").save()
        ses = settings.SITE.login('robin')

        """Run do_update_events a first time

        """

        res = ses.run(obj.do_update_events)
        self.assertEqual(res['success'], True)
        expected = """\
Update Events for First Line (1/10/14 First Room)...
Generating events between 2014-01-13 and 2019-06-15.
5 row(s) have been updated."""
        self.assertEqual(res['info_message'], expected)
        ar = ses.spawn(cal.EventsByController, master_instance=obj)
        s = ar.to_rst(column_names="when_text state")
        # print s
        self.assertEqual(s, """\
======================= ===========
 When                    State
----------------------- -----------
 **2014 Jan 13 (Mon)**   Suggested
 **2014 Jan 20 (Mon)**   Suggested
 **2014 Jan 27 (Mon)**   Suggested
 **2014 Feb 03 (Mon)**   Suggested
 **2014 Feb 10 (Mon)**   Suggested
======================= ===========
""")

        """Now we want to skip the 2nd event.  We click on "Move next" on
        this event.

        """
        # e = cal.Event.objects.get(owner=obj, start_date=i2d(20140120))
        ar = cal.EventsByController.request(
            master_instance=obj,
            known_values=dict(
                start_date=i2d(20140120)))
        e = ar.data_iterator[0]
        self.assertEqual(e.state, cal.EventStates.suggested)
        #
        res = ses.run(e.move_next)

        self.assertEqual(res['success'], True)
        expected = """\
Move down for Course #1 Appointment 2...
1 row(s) have been updated."""
        self.assertEqual(res['info_message'], expected)

        self.assertEqual(e.state, cal.EventStates.draft)
        e.full_clean()
        e.save()
        
        ar = ses.spawn(cal.EventsByController, master_instance=obj)
        s = ar.to_rst(column_names="when_text state")
        # print s
        self.assertEqual(s, """\
======================= ===========
 When                    State
----------------------- -----------
 **2014 Jan 13 (Mon)**   Suggested
 **2014 Jan 27 (Mon)**   Draft
 **2014 Jan 27 (Mon)**   Suggested
 **2014 Feb 03 (Mon)**   Suggested
 **2014 Feb 10 (Mon)**   Suggested
======================= ===========
""")


        """Run do_update_events a second time

        """

        res = ses.run(obj.do_update_events)
        self.assertEqual(res['success'], True)
        expected = """\
Update Events for First Line (1/10/14 First Room)...
2 has been moved from 2014-01-20 to 2014-01-27: move subsequent dates (3, 4, 5) by 7 days, 0:00:00
3 : 2014-01-27 -> 2014-02-03
4 : 2014-02-03 -> 2014-02-10
5 : 2014-02-10 -> 2014-02-17
5 row(s) have been updated."""
        self.assertEqual(res['info_message'], expected)
        ar = ses.spawn(cal.EventsByController, master_instance=obj)
        s = ar.to_rst(column_names="when_text state")
        # print s
        self.assertEqual(s, """\
======================= ===========
 When                    State
----------------------- -----------
 **2014 Jan 13 (Mon)**   Suggested
 **2014 Jan 27 (Mon)**   Draft
 **2014 Feb 03 (Mon)**   Suggested
 **2014 Feb 10 (Mon)**   Suggested
 **2014 Feb 17 (Mon)**   Suggested
======================= ===========
""")




class DemoTest(RemoteAuthTestCase):
    maxDiff = None
    fixtures = settings.SITE.demo_fixtures

    def test001(self):
        """
        test whether the demo fixtures load correctly.
        """


__all__ = ['QuickTest', 'DemoTest']
