# -*- coding: utf-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
To run just this test:

  $ cd lino_faggio/projects/docs
  $ python manage.py test

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from lino.runtime import cal
from lino.runtime import courses
from lino.runtime import users
from django.conf import settings

from lino.utils.djangotest import RemoteAuthTestCase
from lino.utils import i2d
from lino.modlib.users.choicelists import UserProfiles


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
                   profile=UserProfiles.admin,
                   language="en").save()
        ses = settings.SITE.login('robin')

        """Run do_update_events a first time

        """

        res = ses.run(obj.do_update_events)
        self.assertEqual(res['success'], True)
        expected = """\
Update Events for First Line (1/10/14 First Room)...
Generating events between 2014-01-13 and 2019-05-22.
Update Guests for Course #1 Appointment 1...
0 row(s) have been updated.
Update Guests for Course #1 Appointment 2...
0 row(s) have been updated.
Update Guests for Course #1 Appointment 3...
0 row(s) have been updated.
Update Guests for Course #1 Appointment 4...
0 row(s) have been updated.
Update Guests for Course #1 Appointment 5...
0 row(s) have been updated.
5 row(s) have been updated."""
        self.assertEqual(res['info_message'], expected)
        ar = ses.spawn(cal.EventsByController, master_instance=obj)
        s = ar.to_rst(column_names="when_text state")
        # print s
        self.assertEqual(s, """\
============= ===========
 When          State
------------- -----------
 Mon 1/13/14   Suggested
 Mon 1/20/14   Suggested
 Mon 1/27/14   Suggested
 Mon 2/3/14    Suggested
 Mon 2/10/14   Suggested
============= ===========
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
============= ===========
 When          State
------------- -----------
 Mon 1/13/14   Suggested
 Mon 1/27/14   Draft
 Mon 1/27/14   Suggested
 Mon 2/3/14    Suggested
 Mon 2/10/14   Suggested
============= ===========
""")


        """Run do_update_events a second time

        """

        res = ses.run(obj.do_update_events)
        self.assertEqual(res['success'], True)
        expected = """\
Update Events for First Line (1/10/14 First Room)...
Generating events between 2014-01-13 and 2019-05-22.
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
============= ===========
 When          State
------------- -----------
 Mon 1/13/14   Suggested
 Mon 1/27/14   Draft
 Mon 2/3/14    Suggested
 Mon 2/10/14   Suggested
 Mon 2/17/14   Suggested
============= ===========
""")



