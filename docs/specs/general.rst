.. _voga.tested.general:

=======
General
=======

.. To run only this test::

    $ python setup.py test -s tests.DocsTests.test_general

    doctest init:

    >>> from __future__ import print_function
    >>> import lino
    >>> lino.startup('lino_voga.projects.roger.settings.doctest')
    >>> from lino.api.doctest import *

We can now refer to every installed app via it's `app_label`.
For example here is how we can verify here that the demo database 
has 23 pupils and 7 teachers:

>>> courses.Pupil.objects.count()
35
>>> courses.Teacher.objects.count()
8


.. Note that there are no excerpts

   >>> rt.show(excerpts.Excerpts)
   No data to display



The demo database
-----------------

>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_db_overview())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
35 apps: lino_startup, staticfiles, about, extjs, jinja, bootstrap3, appypod, printing, system, contenttypes, gfks, users, office, countries, contacts, lists, beid, cal, extensible, rooms, products, cosi, accounts, ledger, vat, sales, finan, sepa, courses, notes, uploads, outbox, excerpts, voga, export_excel.
69 models:
========================== ============================== ========= =======
 Name                       Default table                  #fields   #rows
-------------------------- ------------------------------ --------- -------
 accounts.Account           accounts.Accounts              12        12
 accounts.Group             accounts.Groups                4         7
 cal.Calendar               cal.Calendars                  4         8
 cal.Event                  cal.OneEvent                   23        346
 cal.EventType              cal.EventTypes                 12        8
 cal.Guest                  cal.Guests                     6         0
 cal.GuestRole              cal.GuestRoles                 2         0
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
 contenttypes.ContentType   gfks.ContentTypes              3         70
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
 excerpts.Excerpt           excerpts.Excerpts              11        0
 excerpts.ExcerptType       excerpts.ExcerptTypes          15        5
 finan.BankStatement        finan.BankStatements           12        0
 finan.BankStatementItem    finan.BankStatementItemTable   10        0
 finan.JournalEntry         finan.FinancialVouchers        10        0
 finan.JournalEntryItem     finan.JournalEntryItemTable    10        0
 finan.PaymentOrder         finan.PaymentOrders            12        0
 finan.PaymentOrderItem     finan.PaymentOrderItemTable    10        0
 gfks.HelpText              gfks.HelpTexts                 4         2
 ledger.Journal             ledger.Journals                14        6
 ledger.MatchRule           ledger.MatchRules              3         10
 ledger.Movement            ledger.Movements               9         0
 ledger.PaymentTerm         ledger.PaymentTerms            6         7
 ledger.Voucher             ledger.Vouchers                9         70
 lists.List                 lists.Lists                    5         8
 lists.ListType             lists.ListTypes                2         3
 lists.Member               lists.Members                  5         0
 notes.EventType            notes.EventTypes               4         0
 notes.Note                 notes.Notes                    16        100
 notes.NoteType             notes.NoteTypes                9         3
 outbox.Attachment          outbox.Attachments             4         0
 outbox.Mail                outbox.Mails                   8         0
 outbox.Recipient           outbox.Recipients              6         0
 products.Product           products.Products              9         9
 products.ProductCat        products.ProductCats           3         5
 rooms.Booking              rooms.Bookings                 24        3
 sales.InvoiceItem          sales.InvoiceItems             15        68
 sales.InvoicingMode        sales.InvoicingModes           6         0
 sales.VatProductInvoice    sales.Invoices                 25        40
 sepa.Account               sepa.Accounts                  6         17
 system.SiteConfig          system.SiteConfigs             17        1
 uploads.Upload             uploads.Uploads                9         0
 uploads.UploadType         uploads.UploadTypes            6         0
 users.Authority            users.Authorities              3         0
 users.User                 users.Users                    15        1
 vat.InvoiceItem            vat.InvoiceItemTable           9         48
 vat.VatAccountInvoice      vat.Invoices                   21        30
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
- Courses : Participants, Instructors, -, Topics, Course series, Courses, -, Pending requested enrolments, Pending confirmed enrolments
- Office : My Notes, My Uploads, My Outbox, My Excerpts
- Reports :
  - System : Broken GFKs
  - Accounting : Situation, Activity Report, Debtors, Creditors
- Configure :
  - System : Site Parameters, Help Texts, Users
  - Places : Countries, Places
  - Contacts : Organization types, Functions, List Types
  - Calendar : Calendars, Rooms, Priorities, Recurrent event rules, Guest Roles, Calendar Event Types, Remote Calendars
  - Accounting : Account Groups, Accounts, Journals, Payment Terms
  - VAT : VAT rules
  - Courses : Instructor Types, Participant Types, Timetable Slots
  - Office : Note Types, Event Types, Upload Types, Excerpt Types
- Explorer :
  - System : content types, Authorities, User Profiles
  - Contacts : Contact Persons, List memberships
  - Calendar : Tasks, Participants, Subscriptions, Event states, Guest states, Task states
  - Accounting : Match rules, Vouchers, Voucher types, Movements, Fiscal Years, Trade types
  - VAT : VAT regimes, VAT Classes
  - Sales : Voucher items
  - Financial : Bank Statements, Journal Entries, Payment Orders
  - SEPA : Bank accounts
  - Courses : Courses, Enrolments, Enrolment states
  - Office : Notes, Uploads, Upload Areas, Outgoing Mails, Attachments, Excerpts
- Site : About



