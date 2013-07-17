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
19 applications: sessions, about, contenttypes, system, users, countries, contacts, products, accounts, ledger, vat, sales, finan, uploads, cal, outbox, courses, lino_faggio, djangosite.
64 models:
======================================= ========= =======
 Name                                    #fields   #rows
--------------------------------------- --------- -------
 accounts.Account                        11        9
 accounts.Chart                          3         1
 accounts.Group                          7         6
 cal.Calendar                            15        5
 cal.Event                               24        272
 cal.Guest                               7         0
 cal.GuestRole                           7         0
 cal.Priority                            4         0
 cal.Room                                7         6
 cal.Subscription                        4         0
 cal.Task                                20        0
 contacts.Company                        27        19
 contacts.CompanyType                    5         11
 contacts.Partner                        23        88
 contacts.Person                         29        69
 contacts.Role                           4         0
 contacts.RoleType                       3         5
 contenttypes.ConcreteModel              2         0
 contenttypes.ContentType                4         64
 contenttypes.FooWithBrokenAbsoluteUrl   3         0
 contenttypes.FooWithUrl                 3         0
 contenttypes.FooWithoutUrl              2         0
 contenttypes.ProxyModel                 2         0
 countries.City                          7         61
 countries.Country                       5         8
 countries.Language                      4         5
 courses.Course                          28        25
 courses.Enrolment                       7         100
 courses.Line                            6         10
 courses.Pupil                           31        35
 courses.PupilType                       3         4
 courses.Slot                            5         0
 courses.Teacher                         31        8
 courses.TeacherType                     3         5
 courses.Topic                           3         4
 finan.BankStatement                     11        10
 finan.DocItem                           10        43
 ledger.AccountInvoice                   17        10
 ledger.InvoiceItem                      9         19
 ledger.Journal                          12        3
 ledger.Movement                         7         30
 ledger.Voucher                          7         20
 outbox.Attachment                       4         0
 outbox.Mail                             9         0
 outbox.Recipient                        6         0
 products.Product                        10        5
 products.ProductCat                     4         3
 sales.Invoice                           25        0
 sales.InvoiceItem                       16        0
 sales.InvoicingMode                     7         0
 sales.PaymentTerm                       6         0
 sales.ProductDocItem                    12        0
 sales.SalesRule                         4         0
 sales.ShippingMode                      4         0
 sessions.Session                        3         4
 system.HelpText                         4         2
 system.SiteConfig                       4         1
 system.TextFieldTemplate                6         2
 uploads.Upload                          11        0
 uploads.UploadType                      2         0
 users.Authority                         3         0
 users.Membership                        3         0
 users.Team                              3         0
 users.User                              14        2
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
