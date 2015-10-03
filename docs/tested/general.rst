.. _faggio.tested.general:

=======
General
=======

.. To run only this test::

    $ python setup.py test -s tests.DocsTests.test_general

    doctest init:

    >>> from __future__ import print_function
    >>> from django.utils import translation
    >>> from django.test.client import Client
    >>> from lino.api import dd
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
32 apps: staticfiles, about, bootstrap3, lino_startup, appypod, printing, system, contenttypes, gfks, users, countries, contacts, lists, beid, cal, extensible, rooms, products, cosi, accounts, ledger, vat, sales, finan, sepa, courses, notes, uploads, outbox, excerpts, lino_faggio, export_excel.
74 models:
========================== ============================== ========= =======
 Name                       Default table                  #fields   #rows
-------------------------- ------------------------------ --------- -------
 accounts.Account           accounts.Accounts              12        12
 accounts.Group             accounts.Groups                5         7
 cal.Calendar               cal.Calendars                  4         8
 cal.Event                  cal.OneEvent                   23        296
 cal.EventType              cal.EventTypes                 12        8
 cal.Guest                  cal.Guests                     6         0
 cal.GuestRole              cal.GuestRoles                 2         0
 cal.Priority               cal.Priorities                 3         4
 cal.RecurrentEvent         cal.RecurrentEvents            19        9
 cal.RemoteCalendar         cal.RemoteCalendars            7         0
 cal.Room                   cal.Rooms                      7         7
 cal.Subscription           cal.Subscriptions              4         7
 cal.Task                   cal.Tasks                      17        0
 contacts.Company           contacts.Companies             26        29
 contacts.CompanyType       contacts.CompanyTypes          3         16
 contacts.Partner           contacts.Partners              22        98
 contacts.Person            contacts.Persons               37        69
 contacts.Role              contacts.Roles                 4         0
 contacts.RoleType          contacts.RoleTypes             2         5
 contenttypes.ContentType   gfks.ContentTypes              4         75
 countries.Country          countries.Countries            4         8
 countries.Place            countries.Places               6         78
 courses.Course             courses.Courses                28        25
 courses.Enrolment          courses.Enrolments             14        100
 courses.Line               courses.Lines                  15        10
 courses.Pupil              courses.Pupils                 39        35
 courses.PupilType          courses.PupilTypes             3         4
 courses.Slot               courses.Slots                  5         0
 courses.Teacher            courses.Teachers               39        8
 courses.TeacherType        courses.TeacherTypes           3         4
 courses.Topic              courses.Topics                 2         5
 excerpts.Excerpt           excerpts.Excerpts              11        1
 excerpts.ExcerptType       excerpts.ExcerptTypes          15        4
 finan.BankStatement        finan.BankStatements           11        15
 finan.BankStatementItem    finan.BankStatementItemTable   10        99
 finan.Grouper              finan.Groupers                 10        0
 finan.GrouperItem          finan.GrouperItemTable         9         0
 finan.JournalEntry         finan.FinancialVouchers        9         0
 finan.JournalEntryItem     finan.JournalEntryItemTable    10        0
 finan.PaymentOrder         finan.PaymentOrders            11        15
 finan.PaymentOrderItem     finan.PaymentOrderItemTable    10        0
 gfks.HelpText              gfks.HelpTexts                 4         2
 ledger.Journal             ledger.Journals                14        6
 ledger.MatchRule           ledger.MatchRules              3         10
 ledger.Movement            ledger.Movements               9         235
 ledger.PaymentTerm         ledger.PaymentTerms            5         0
 ledger.Voucher             ledger.Vouchers                8         147
 lists.List                 lists.Lists                    5         8
 lists.ListType             lists.ListTypes                2         3
 lists.Member               lists.Members                  5         0
 notes.EventType            notes.EventTypes               4         0
 notes.Note                 notes.Notes                    16        100
 notes.NoteType             notes.NoteTypes                9         6
 outbox.Attachment          outbox.Attachments             4         0
 outbox.Mail                outbox.Mails                   8         0
 outbox.Recipient           outbox.Recipients              6         0
 products.Product           products.Products              9         11
 products.ProductCat        products.ProductCats           3         5
 rooms.Booking              rooms.Bookings                 24        3
 sales.InvoiceItem          sales.InvoiceItemTable         15        62
 sales.InvoicingMode        sales.InvoicingModes           6         0
 sales.ShippingMode         sales.ShippingModes            3         0
 sales.VatProductInvoice    sales.Invoices                 26        37
 sepa.Account               sepa.Accounts                  6         17
 sepa.Movement              sepa.Movements                 9         0
 sepa.Statement             sepa.Statements                9         0
 system.SiteConfig          system.SiteConfigs             17        1
 uploads.Upload             uploads.Uploads                9         0
 uploads.UploadType         uploads.UploadTypes            6         0
 users.Authority            users.Authorities              3         0
 users.User                 users.Users                    15        1
 vat.InvoiceItem            vat.InvoiceItemTable           9         128
 vat.VatAccountInvoice      vat.Invoices                   20        80
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
- Calendar : My appointments, My tasks, My guests, My presences, Calendar, Bookings
- Products : Products, Product Categories
- Accounting :
  - Sales : Sales invoices (SLS)
  - Purchases : Purchase invoices (PRC)
  - Financial : Bestbank (BNK), Payment Orders (PMO), Cash (CSH), Miscellaneous Journal Entries (MSG)
- Sales : Invoices to create
- Courses : Participants, Instructors, -, Courses, Course series, -, Pending requested enrolments, Pending confirmed enrolments
- Office : My Notes, My Uploads, My Outbox, My Excerpts
- Reports :
  - System : Broken GFKs
  - Accounting : Situation, Activity Report, Debtors, Creditors
- Configure :
  - System : Site Parameters, Help Texts, Users
  - Places : Countries, Places
  - Contacts : Organization types, Functions, List Types
  - Calendar : Calendars, Rooms, Priorities, Recurrent Events, Guest Roles, Calendar Event Types, Remote Calendars
  - Accounting : Account Charts, Account Groups, Accounts, Journals, Payment Terms
  - VAT : VAT rules
  - Sales : Shipping Modes
  - Courses : Instructor Types, Participant Types, Topics, Course series, Timetable Slots
  - Office : Note Types, Event Types, Upload Types, Excerpt Types
- Explorer :
  - System : content types, Authorities, User Profiles
  - Contacts : Contact Persons, List memberships
  - Calendar : Tasks, Participants, Subscriptions, Event states, Guest states, Task states
  - Accounting : Match rules, Vouchers, Voucher types, Movements, Fiscal Years, Trade types
  - VAT : VAT regimes, VAT Classes
  - Financial : Bank Statements, Journal Entries, Payment Orders, Groupers
  - SEPA : Accounts
  - Courses : Enrolments, Enrolment states
  - Office : Notes, Uploads, Upload Areas, Outgoing Mails, Attachments, Excerpts
- Site : About
