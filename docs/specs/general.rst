.. _voga.tested.general:

=======
General
=======

.. To run only this test::

    $ python setup.py test -s tests.DocsTests.test_general

    doctest init:

    >>> import lino
    >>> lino.startup('lino_voga.projects.roger.settings.doctests')
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
41 apps: lino_startup, staticfiles, about, jinja, bootstrap3, extjs, users, office, countries, printing, system, contacts, lists, beid, contenttypes, gfks, plausibility, xl, cal, products, rooms, cosi, accounts, weasyprint, ledger, vat, sales, invoicing, courses, finan, sepa, notify, notes, uploads, outbox, excerpts, voga, export_excel, extensible, wkhtmltopdf, appypod.
75 models:
========================== ============================== ========= =======
 Name                       Default table                  #fields   #rows
-------------------------- ------------------------------ --------- -------
 accounts.Account           accounts.Accounts              15        13
 accounts.Group             accounts.Groups                6         7
 cal.Calendar               cal.Calendars                  6         8
 cal.Event                  cal.OneEvent                   23        1154
 cal.EventType              cal.EventTypes                 16        8
 cal.Guest                  cal.Guests                     6         0
 cal.GuestRole              cal.GuestRoles                 4         3
 cal.Priority               cal.Priorities                 5         4
 cal.RecurrentEvent         cal.RecurrentEvents            21        16
 cal.RemoteCalendar         cal.RemoteCalendars            7         0
 cal.Room                   cal.Rooms                      9         7
 cal.Subscription           cal.Subscriptions              4         35
 cal.Task                   cal.Tasks                      17        0
 contacts.Company           contacts.Companies             27        29
 contacts.CompanyType       contacts.CompanyTypes          7         16
 contacts.Partner           contacts.Partners              23        100
 contacts.Person            contacts.Persons               38        71
 contacts.Role              contacts.Roles                 4         0
 contacts.RoleType          contacts.RoleTypes             4         5
 contenttypes.ContentType   gfks.ContentTypes              3         76
 countries.Country          countries.Countries            6         8
 countries.Place            countries.Places               8         78
 courses.Course             courses.Activities             31        25
 courses.CourseType         courses.CourseTypes            5         0
 courses.Enrolment          courses.Enrolments             17        82
 courses.Line               courses.Lines                  22        10
 courses.Pupil              courses.Pupils                 47        35
 courses.PupilType          courses.PupilTypes             5         3
 courses.Slot               courses.Slots                  5         0
 courses.Teacher            courses.Teachers               40        8
 courses.TeacherType        courses.TeacherTypes           5         4
 courses.Topic              courses.Topics                 4         5
 excerpts.Excerpt           excerpts.Excerpts              11        0
 excerpts.ExcerptType       excerpts.ExcerptTypes          17        11
 finan.BankStatement        finan.BankStatements           16        21
 finan.BankStatementItem    finan.BankStatementItemTable   10        175
 finan.JournalEntry         finan.FinancialVouchers        14        0
 finan.JournalEntryItem     finan.JournalEntryItemTable    10        0
 finan.PaymentOrder         finan.PaymentOrders            15        16
 finan.PaymentOrderItem     finan.PaymentOrderItemTable    10        80
 gfks.HelpText              gfks.HelpTexts                 4         2
 invoicing.Item             invoicing.Items                10        6
 invoicing.Plan             invoicing.Plans                7         1
 ledger.AccountingPeriod    ledger.AccountingPeriods       7         17
 ledger.Journal             ledger.Journals                19        7
 ledger.MatchRule           ledger.MatchRules              3         11
 ledger.Movement            ledger.Movements               10        675
 ledger.PaymentTerm         ledger.PaymentTerms            9         8
 ledger.Voucher             ledger.Vouchers                9         205
 lists.List                 lists.Lists                    7         8
 lists.ListType             lists.ListTypes                4         3
 lists.Member               lists.Members                  5         0
 notes.EventType            notes.EventTypes               8         1
 notes.Note                 notes.Notes                    16        100
 notes.NoteType             notes.NoteTypes                11        3
 notify.Notification        notify.Notifications           9         3
 outbox.Attachment          outbox.Attachments             4         0
 outbox.Mail                outbox.Mails                   8         0
 outbox.Recipient           outbox.Recipients              6         0
 plausibility.Problem       plausibility.Problems          6         14
 products.Product           products.Products              15        11
 products.ProductCat        products.ProductCats           5         5
 rooms.Booking              rooms.Bookings                 23        3
 sales.InvoiceItem          sales.InvoiceItems             15        101
 sales.PaperType            sales.PaperTypes               5         2
 sales.VatProductInvoice    sales.Invoices                 24        83
 sepa.Account               sepa.Accounts                  6         17
 system.SiteConfig          system.SiteConfigs             18        1
 uploads.Upload             uploads.Uploads                9         0
 uploads.UploadType         uploads.UploadTypes            8         0
 users.Authority            users.Authorities              3         0
 users.User                 users.Users                    15        5
 vat.InvoiceItem            vat.InvoiceItemTable           9         136
 vat.VatAccountInvoice      vat.Invoices                   19        85
 vat.VatRule                vat.VatRules                   9         11
========================== ============================== ========= =======
<BLANKLINE>


