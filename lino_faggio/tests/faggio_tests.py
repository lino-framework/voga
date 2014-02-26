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

from lino.runtime import courses
from lino.runtime import users
from django.conf import settings

from lino import dd
from lino.utils import i2d
from djangosite.utils.djangotest import RemoteAuthTestCase


class QuickTest(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        # from lino.runtime import courses, users, settings
        line = courses.Line(name="First Line")
        line.save()

        obj = courses.Course(
            line=line,
            start_date=i2d(20140110))
        self.assertEqual(unicode(obj), "First Line (1/10/14)")

        self.assertEqual(settings.SITE.kernel.__class__.__name__, 'Kernel')
        self.assertEqual(settings.SITE.kernel.site, settings.SITE)
        self.assertEqual(settings.SITE.plugins.extjs, dd.apps.extjs)

        settings.SITE.verbose_client_info_message = True
        users.User(username="robin",
                   profile=dd.UserProfiles.admin,
                   language="en").save()
        ses = settings.SITE.login('robin')
        ses.show(courses.EventsByCourse, obj,
                 column_names="when_text state")


class DemoTest(RemoteAuthTestCase):
    maxDiff = None
    fixtures = settings.SITE.demo_fixtures

    def test001(self):
        """
        test whether the demo fixtures load correctly.
        """


__all__ = ['QuickTest', 'DemoTest']
