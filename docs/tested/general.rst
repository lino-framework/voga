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
>>> from lino.api.shell import *

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
28 apps: about, bootstrap3, lino, contenttypes, system, users, countries, contacts, lists, beid, courses, extensible, cal, rooms, products, accounts, ledger, vat, sales, finan, iban, notes, uploads, outbox, excerpts, lino_faggio, appypod, export_excel.
70 models:
========================== ============================== ========= =======
 Name                       Default table                  #fields   #rows
-------------------------- ------------------------------ --------- -------
 accounts.Account           accounts.Accounts              12        12
 accounts.Chart             accounts.Charts                2         1
 accounts.Group             accounts.Groups                5         7
 cal.Calendar               cal.Calendars                  4         8
 cal.Event                  cal.OneEvent                   23        296
 cal.EventType              cal.EventTypes                 12        7
 cal.Guest                  cal.Guests                     6         0
 cal.GuestRole              cal.GuestRoles                 2         0
 cal.Priority               cal.Priorities                 3         4
 cal.RecurrentEvent         cal.RecurrentEvents            19        9
 cal.RemoteCalendar         cal.RemoteCalendars            7         0
 cal.Room                   cal.Rooms                      7         7
 cal.Subscription           cal.Subscriptions              4         7
 cal.Task                   cal.Tasks                      17        0
 contacts.Company           contacts.Companies             28        19
 contacts.CompanyType       contacts.CompanyTypes          3         16
 contacts.Partner           contacts.Partners              24        88
 contacts.Person            contacts.Persons               39        69
 contacts.Role              contacts.Roles                 4         0
 contacts.RoleType          contacts.RoleTypes             2         5
 contenttypes.ContentType   contenttypes.ContentTypes      4         71
 contenttypes.HelpText      contenttypes.HelpTexts         4         2
 countries.Country          countries.Countries            4         8
 countries.Place            countries.Places               6         78
 courses.Course             courses.Courses                28        25
 courses.Enrolment          courses.Enrolments             13        100
 courses.Line               courses.Lines                  13        10
 courses.Pupil              courses.Pupils                 41        35
 courses.PupilType          courses.PupilTypes             3         4
 courses.Slot               courses.Slots                  5         0
 courses.Teacher            courses.Teachers               41        8
 courses.TeacherType        courses.TeacherTypes           3         4
 courses.Topic              courses.Topics                 2         5
 excerpts.Excerpt           excerpts.ExcerptsByX           11        1
 excerpts.ExcerptType       excerpts.ExcerptTypes          15        3
 finan.BankStatement        finan.BankStatements           11        0
 finan.BankStatementItem    finan.BankStatementItemTable   11        0
 finan.JournalEntry         finan.JournalEntries           9         0
 finan.JournalEntryItem     finan.JournalEntryItemTable    11        0
 finan.PaymentOrder         finan.PaymentOrders            11        0
 finan.PaymentOrderItem     finan.PaymentOrderItemTable    10        0
 ledger.AccountInvoice      ledger.Invoices                18        20
 ledger.InvoiceItem         ledger.InvoiceItemTable        9         32
 ledger.Journal             ledger.Journals                13        6
 ledger.Movement            ledger.Movements               9         28
 ledger.Voucher             ledger.Vouchers                7         39
 lists.List                 lists.Lists                    5         8
 lists.ListType             lists.ListTypes                2         3
 lists.Member               lists.Members                  5         0
 notes.EventType            notes.EventTypes               4         0
 notes.Note                 notes.Notes                    16        100
 notes.NoteType             notes.NoteTypes                8         6
 outbox.Attachment          outbox.Attachments             4         0
 outbox.Mail                outbox.Mails                   8         0
 outbox.Recipient           outbox.Recipients              6         0
 products.Product           products.Products              8         11
 products.ProductCat        products.ProductCats           3         5
 rooms.Booking              rooms.Bookings                 24        3
 sales.Invoice              sales.Invoices                 24        19
 sales.InvoiceItem          sales.InvoiceItemTable         15        26
 sales.InvoicingMode        sales.InvoicingModes           6         0
 sales.ShippingMode         sales.ShippingModes            3         0
 system.SiteConfig          system.SiteConfigs             17        1
 system.TextFieldTemplate   system.TextFieldTemplates      5         2
 uploads.Upload             uploads.Uploads                9         0
 uploads.UploadType         uploads.UploadTypes            6         0
 users.Authority            users.Authorities              3         0
 users.User                 users.Users                    15        1
 vat.PaymentTerm            vat.PaymentTerms               5         0
 vat.VatRule                vat.VatRules                   9         0
========================== ============================== ========= =======
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
- Calendar : Calendar, My appointments, My tasks, My guests, My presences, Bookings
- Products : Products, Product Categories
- Sales : Sales invoices (S), Invoices to create
- Purchases : Purchase invoices (P), Payment Orders (PO)
- Financial : Bestbank (B), Cash (C), Miscellaneous Journal Entries (M)
- Office : My Notes, My Uploads, My Outbox, My Excerpts
- Reports :
  - System : Stale Controllables
  - Accounting : Situation, Activity Report, Debtors, Creditors
- Configure :
  - System : Help Texts, Site Parameters, Users
  - Office : My Text Field Templates, Note Types, Event Types, Upload Types, Excerpt Types
  - Places : Countries, Places
  - Contacts : Organization types, Functions, List Types
  - Courses : Instructor Types, Participant Types, Topics, Course Lines, Timetable Slots
  - Calendar : Calendars, Rooms, Priorities, Recurrent Events, Guest Roles, Event Types, Remote Calendars
  - Accounting : Account Charts, Account Groups, Accounts, Journals
  - VAT : Payment Terms, VAT rules
  - Sales : Shipping Modes
- Explorer :
  - System : content types, Authorities, User Groups, User Levels, User Profiles
  - Office : Text Field Templates, Notes, Uploads, Upload Areas, Outgoing Mails, Attachments, Excerpts
  - Contacts : Contact Persons, List memberships
  - Courses : Enrolments, Enrolment states
  - Calendar : Tasks, Participants, Subscriptions, Event states, Guest states, Task states
  - Accounting : Invoices, Vouchers, VoucherTypes, Movements, Fiscal Years
  - VAT : VatRegimes, TradeTypes, VatClasses
  - Financial : Bank Statements, Journal Entries, Payment Orders
- Site : About
