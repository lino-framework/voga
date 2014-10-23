.. _faggio.tested.general:

=======
General
=======

.. include:: /include/tested.rst

..
  To run only this test::

  $ python setup.py test -s tests.DocsTests.test_general

The following statements import a set of often-used global names::

>>> from __future__ import print_function
>>> from django.utils import translation
>>> from django.test.client import Client
>>> from lino import dd
>>> from lino.runtime import *

We can now refer to every installed app via it's `app_label`.
For example here is how we can verify here that the demo database 
has 23 pupils and 7 teachers:

>>> courses.Pupil.objects.count()
35
>>> courses.Teacher.objects.count()
8


The demo database
-----------------

Test whether :meth:`get_db_overview_rst 
<lino_site.Site.get_db_overview_rst>` returns the expected result:

>>> print(settings.SITE.get_db_overview_rst()) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
29 apps: about, bootstrap3, lino, contenttypes, system, users, countries, contacts, lists, beid, courses, extensible, cal, rooms, products, accounts, ledger, vat, sales, finan, iban, notes, uploads, outbox, excerpts, lino_faggio, appypod, export_excel, djangosite.
69 models:
========================== ========= =======
 Name                       #fields   #rows
-------------------------- --------- -------
 accounts.Account           12        12
 accounts.Chart             2         1
 accounts.Group             5         7
 cal.Calendar               4         8
 cal.Event                  23        296
 cal.EventType              12        7
 cal.Guest                  6         0
 cal.GuestRole              2         0
 cal.Priority               3         4
 cal.RecurrentEvent         19        9
 cal.RemoteCalendar         7         0
 cal.Room                   7         7
 cal.Subscription           4         7
 cal.Task                   17        0
 contacts.Company           28        19
 contacts.CompanyType       3         16
 contacts.Partner           24        88
 contacts.Person            39        69
 contacts.Role              4         0
 contacts.RoleType          2         5
 contenttypes.ContentType   4         70
 countries.Country          4         8
 countries.Place            6         78
 courses.Course             27        25
 courses.Enrolment          13        100
 courses.Line               13        10
 courses.Pupil              41        35
 courses.PupilType          3         4
 courses.Slot               5         0
 courses.Teacher            41        8
 courses.TeacherType        3         4
 courses.Topic              2         5
 excerpts.Excerpt           10        1
 excerpts.ExcerptType       15        3
 finan.BankStatement        11        3
 finan.BankStatementItem    11        9
 finan.JournalEntry         9         0
 finan.JournalEntryItem     11        0
 finan.PaymentOrder         11        3
 finan.PaymentOrderItem     10        15
 ledger.AccountInvoice      18        20
 ledger.InvoiceItem         9         32
 ledger.Journal             13        6
 ledger.Movement            9         98
 ledger.Voucher             7         45
 lists.List                 5         8
 lists.ListType             2         3
 lists.Member               5         0
 notes.EventType            4         0
 notes.Note                 16        100
 notes.NoteType             8         6
 outbox.Attachment          4         0
 outbox.Mail                8         0
 outbox.Recipient           6         0
 products.Product           8         11
 products.ProductCat        3         5
 rooms.Booking              24        3
 sales.Invoice              24        19
 sales.InvoiceItem          15        26
 sales.InvoicingMode        6         0
 sales.ShippingMode         3         0
 system.HelpText            4         2
 system.SiteConfig          17        1
 system.TextFieldTemplate   5         2
 uploads.Upload             9         0
 uploads.UploadType         5         0
 users.Authority            3         0
 users.User                 15        1
 vat.PaymentTerm            5         0
========================== ========= =======
<BLANKLINE>



Menus
-----

System administrator
--------------------

Rolf is the local system administrator, he has a complete menu:

>>> ses = rt.login('robin') 
>>> ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Persons, Organizations, Partners, Partner Lists
- Courses : Participants, Instructors, -, Courses, Course Lines, -, Pending requested enrolments, Pending confirmed enrolments
- Calendar : Calendar, My events, My tasks, My guests, My presences, Bookings
- Products : Products, Product Categories
- Sales : Sales invoices (S), Invoices to create
- Purchases : Purchase invoices (P), Payment Orders (PO)
- Financial : Bestbank (B), Cash (C), Miscellaneous Journal Entries (M)
- Office : My Notes, My Uploads, My Outbox, My Excerpts
- Reports :
  - Accounting : Situation, Activity Report, Debtors, Creditors
- Configure :
  - Office : My Text Field Templates, Note Types, Event Types, Upload Types, Excerpt Types
  - System : Site Parameters, Users, content types, Help Texts
  - Places : Countries, Places
  - Contacts : Organization types, Functions, List Types
  - Courses : Instructor Types, Participant Types, Topics, Course Lines, Timetable Slots
  - Calendar : Calendars, Rooms, Priorities, Recurrent Events, Guest Roles, Event Types, Remote Calendars
  - Accounting : Account Charts, Account Groups, Accounts, Journals
  - VAT : Payment Terms
  - Sales : Shipping Modes
- Explorer :
  - Office : Text Field Templates, Notes, Uploads, Upload Areas, Outgoing Mails, Attachments, Excerpts
  - System : Authorities, User Groups, User Levels, User Profiles
  - Contacts : Contact Persons, List memberships
  - Courses : Enrolments, Enrolment states
  - Calendar : Tasks, Presences, Subscriptions, Event states, Guest states, Task states
  - Accounting : Invoices, Vouchers, VoucherTypes, Movements, Fiscal Years
  - VAT : VatRegimes, TradeTypes, VatClasses
  - Financial : Bank Statements, Journal Entries, Payment Orders
- Site : About
