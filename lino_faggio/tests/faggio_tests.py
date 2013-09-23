# -*- coding: utf-8 -*-
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
This module contains "quick" tests that are run on a demo database 
without any fixture. You can run only these tests by issuing::

  python manage.py test lino_faggio.QuickTest

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import decimal

#~ from django.utils import unittest
#~ from django.test.client import Client
from django.conf import settings


from django.utils import translation
from django.utils.encoding import force_unicode
from django.core.exceptions import ValidationError

from lino import dd
from lino.utils import i2d
from djangosite.utils.djangotest import RemoteAuthTestCase

DEMO_OVERVIEW = """\
20 applications: sessions, about, contenttypes, system, users, countries, contacts, products, accounts, ledger, vat, sales, finan, notes, uploads, cal, outbox, courses, lino_faggio, djangosite.
65 models:
======================================= ========= =======
 Name                                    #fields   #rows
--------------------------------------- --------- -------
 accounts.Account                        13        11
 accounts.Chart                          4         1
 accounts.Group                          8         6
 cal.Calendar                            21        5
 cal.Event                               24        272
 cal.Guest                               7         0
 cal.GuestRole                           8         0
 cal.Priority                            5         0
 cal.Room                                8         6
 cal.Subscription                        4         0
 cal.Task                                20        0
 contacts.Company                        27        19
 contacts.CompanyType                    7         16
 contacts.Partner                        23        88
 contacts.Person                         29        69
 contacts.Role                           4         0
 contacts.RoleType                       4         5
 contenttypes.ConcreteModel              2         0
 contenttypes.ContentType                4         65
 contenttypes.FooWithBrokenAbsoluteUrl   3         0
 contenttypes.FooWithUrl                 3         0
 contenttypes.FooWithoutUrl              2         0
 contenttypes.ProxyModel                 2         0
 countries.City                          8         62
 countries.Country                       6         8
 courses.Course                          28        25
 courses.Enrolment                       9         100
 courses.Line                            8         10
 courses.Pupil                           31        35
 courses.PupilType                       4         4
 courses.Slot                            5         0
 courses.Teacher                         31        8
 courses.TeacherType                     4         5
 courses.Topic                           4         4
 finan.BankStatement                     11        10
 finan.DocItem                           11        43
 ledger.AccountInvoice                   17        10
 ledger.InvoiceItem                      9         19
 ledger.Journal                          17        4
 ledger.Movement                         9         20
 ledger.Voucher                          7         31
 notes.EventType                         8         0
 notes.Note                              15        100
 notes.NoteType                          11        6
 outbox.Attachment                       4         0
 outbox.Mail                             9         0
 outbox.Recipient                        6         0
 products.Product                        11        5
 products.ProductCat                     5         3
 sales.Invoice                           25        11
 sales.InvoiceItem                       15        17
 sales.InvoicingMode                     8         0
 sales.PaymentTerm                       7         0
 sales.SalesRule                         4         0
 sales.ShippingMode                      5         0
 sessions.Session                        3         4
 system.HelpText                         4         2
 system.SiteConfig                       7         1
 system.TextFieldTemplate                6         2
 uploads.Upload                          11        0
 uploads.UploadType                      2         0
 users.Authority                         3         0
 users.Membership                        3         0
 users.Team                              4         0
 users.User                              15        3
======================================= ========= =======
"""


class DemoTest(RemoteAuthTestCase):
    maxDiff = None
    #~ fixtures = 'std demo'.split()
    fixtures = settings.SITE.demo_fixtures
    
    def test001(self):
        """
        test whether the demo fixtures load correctly.
        """

        s = settings.SITE.get_db_overview_rst()
        print s
        self.assertEqual(DEMO_OVERVIEW,s)
