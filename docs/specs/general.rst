.. _voga.tested.general:

=======
General
=======

.. To run only this test::

    $ python setup.py test -s tests.DocsTests.test_general

    doctest init:

    >>> import lino
    >>> lino.startup('lino_voga.projects.docs.settings.doctests')
    >>> from lino.api.doctest import *

The demo database has 35 pupils and 8 teachers:

>>> rt.modules.courses.Pupil.objects.count()
35
>>> rt.modules.courses.Teacher.objects.count()
8


.. Note that there are no excerpts

   >>> rt.show(rt.modules.excerpts.Excerpts)
   No data to display



The demo database
-----------------

>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_db_overview())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
37 apps: lino_startup, staticfiles, about, extjs, jinja, bootstrap3, printing, system, contenttypes, gfks, users, office, countries, contacts, lists, beid, cal, products, rooms, cosi, accounts, ledger, vat, sales, invoicing, courses, finan, sepa, notes, uploads, outbox, excerpts, voga, export_excel, extensible, wkhtmltopdf, appypod.
72 models:
========================== ============================== ========= =======
 Name                       Default table                  #fields   #rows
-------------------------- ------------------------------ --------- -------
 accounts.Account           accounts.Accounts              12        12
 accounts.Group             accounts.Groups                4         7
 cal.Calendar               cal.Calendars                  4         8
 cal.Event                  cal.OneEvent                   23        346
 cal.EventType              cal.EventTypes                 12        8
 cal.Guest                  cal.Guests                     6         0
 cal.GuestRole              cal.GuestRoles                 2         3
 cal.Priority               cal.Priorities                 3         4
 cal.RecurrentEvent         cal.RecurrentEvents            19        16
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
 contenttypes.ContentType   gfks.ContentTypes              3         73
 countries.Country          countries.Countries            4         8
 countries.Place            countries.Places               6         78
 courses.Course             courses.Courses                28        25
 courses.CourseType         courses.CourseTypes            3         0
 courses.Enrolment          courses.Enrolments             16        100
 courses.Line               courses.Lines                  16        10
 courses.Pupil              courses.Pupils                 39        35
 courses.PupilType          courses.PupilTypes             3         3
 courses.Slot               courses.Slots                  5         0
 courses.Teacher            courses.Teachers               39        8
 courses.TeacherType        courses.TeacherTypes           3         4
 courses.Topic              courses.Topics                 2         5
 excerpts.Excerpt           excerpts.Excerpts              11        0
 excerpts.ExcerptType       excerpts.ExcerptTypes          15        8
 finan.BankStatement        finan.BankStatements           15        0
 finan.BankStatementItem    finan.BankStatementItemTable   10        0
 finan.JournalEntry         finan.FinancialVouchers        13        0
 finan.JournalEntryItem     finan.JournalEntryItemTable    10        0
 finan.PaymentOrder         finan.PaymentOrders            15        0
 finan.PaymentOrderItem     finan.PaymentOrderItemTable    10        0
 gfks.HelpText              gfks.HelpTexts                 4         2
 invoicing.Item             invoicing.Items                9         30
 invoicing.Plan             invoicing.Plans                6         1
 ledger.AccountingPeriod    ledger.AccountingPeriods       7         6
 ledger.Journal             ledger.Journals                15        6
 ledger.MatchRule           ledger.MatchRules              3         10
 ledger.Movement            ledger.Movements               9         0
 ledger.PaymentTerm         ledger.PaymentTerms            6         7
 ledger.Voucher             ledger.Vouchers                9         68
 lists.List                 lists.Lists                    5         8
 lists.ListType             lists.ListTypes                2         3
 lists.Member               lists.Members                  5         0
 notes.EventType            notes.EventTypes               4         0
 notes.Note                 notes.Notes                    16        100
 notes.NoteType             notes.NoteTypes                9         3
 outbox.Attachment          outbox.Attachments             4         0
 outbox.Mail                outbox.Mails                   8         0
 outbox.Recipient           outbox.Recipients              6         0
 products.Product           products.Products              10        9
 products.ProductCat        products.ProductCats           3         5
 rooms.Booking              rooms.Bookings                 23        3
 sales.InvoiceItem          sales.InvoiceItems             15        66
 sales.VatProductInvoice    sales.Invoices                 23        38
 sepa.Account               sepa.Accounts                  6         17
 system.SiteConfig          system.SiteConfigs             18        1
 uploads.Upload             uploads.Uploads                9         0
 uploads.UploadType         uploads.UploadTypes            6         0
 users.Authority            users.Authorities              3         0
 users.User                 users.Users                    15        1
 vat.InvoiceItem            vat.InvoiceItemTable           9         48
 vat.VatAccountInvoice      vat.Invoices                   19        30
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
- Calendar : My appointments, My tasks, My guests, My presences, Bookings, Calendar
- Accounting :
  - Sales : Sales invoices (SLS)
  - Purchases : Purchase invoices (PRC)
  - Financial : Payment Orders (PMO), Cash (CSH), Bestbank (BNK), Miscellaneous Journal Entries (MSC)
  - Create invoices
- Courses : Participants, Instructors, -, Topics, Course series, -, Draft courses, Inactive courses, Active courses, Closed courses, -, Pending requested enrolments, Pending confirmed enrolments
- Office : My Notes, My Uploads, My Outbox, My Excerpts
- Reports :
  - System : Broken GFKs
  - Accounting : Situation, Activity Report, Debtors, Creditors
  - Courses : Status Report
- Configure :
  - System : Site Parameters, Help Texts, Users
  - Places : Countries, Places
  - Contacts : Organization types, Functions, List Types
  - Calendar : Calendars, Rooms, Priorities, Recurrent event rules, Guest Roles, Calendar Event Types, Remote Calendars
  - Tariffs : Tariffs, Tariff Categories
  - Accounting : Account Groups, Accounts, Journals, Accounting periods, Payment Terms
  - VAT : VAT rules
  - Courses : Course types, Instructor Types, Participant Types, Timetable Slots
  - Office : Note Types, Event Types, Upload Types, Excerpt Types
- Explorer :
  - System : content types, Authorities, User Profiles
  - Contacts : Contact Persons, List memberships
  - Calendar : Tasks, Participants, Subscriptions, Event states, Guest states, Task states
  - Accounting : Match rules, Vouchers, Voucher types, Movements, Fiscal Years, Trade types, Journal groups
  - VAT : VAT regimes, VAT Classes, Product invoices, Product invoice items, Invoicing plans
  - Courses : Courses, Enrolments, Enrolment states
  - Financial : Bank Statements, Journal Entries, Payment Orders
  - SEPA : Bank accounts
  - Office : Notes, Uploads, Upload Areas, Outgoing Mails, Attachments, Excerpts
- Site : About



