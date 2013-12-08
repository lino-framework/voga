.. _faggio.tested.general:

General
=======

.. include:: /include/tested.rst

The following statements import a set of often-used global names::

>>> from __future__ import print_function
>>> import json
>>> from pprint import pprint
>>> from django.conf import settings
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


The test database
-----------------

Test whether :meth:`get_db_overview_rst 
<lino_site.Site.get_db_overview_rst>` returns the expected result:

>>> print(settings.SITE.get_db_overview_rst()) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
21 applications: about, contenttypes, system, users, countries, contacts, courses, extensible, cal, rooms, products, accounts, ledger, vat, sales, finan, notes, uploads, outbox, lino_faggio, djangosite.
67 models:
========================== ========= =======
 Name                       #fields   #rows
-------------------------- --------- -------
 accounts.Account           13        12
 accounts.Chart             4         1
 accounts.Group             7         6
 cal.Calendar               6         7
 cal.Event                  23        318
 cal.EventType              17        7
 cal.Guest                  7         0
 cal.GuestRole              8         0
 cal.Priority               5         9
 cal.RecurrentEvent         21        9
 cal.RemoteCalendar         7         0
 cal.Room                   9         6
 cal.Subscription           4         21
 cal.Task                   17        0
 contacts.Company           27        19
 contacts.CompanyType       7         16
 contacts.Partner           23        88
 contacts.Person            29        69
 contacts.Role              4         0
 contacts.RoleType          4         5
 contenttypes.ContentType   4         68
 countries.City             8         75
 countries.Country          6         8
 courses.Course             23        23
 courses.Enrolment          9         100
 courses.Line               12        9
 courses.Pupil              31        35
 courses.PupilType          5         4
 courses.Slot               5         0
 courses.Teacher            31        8
 courses.TeacherType        5         4
 courses.Topic              4         4
 finan.BankStatement        11        3
 finan.BankStatementItem    11        21
 finan.JournalEntry         9         0
 finan.JournalEntryItem     11        0
 finan.PaymentOrder         11        3
 finan.PaymentOrderItem     10        18
 ledger.AccountInvoice      17        20
 ledger.InvoiceItem         9         32
 ledger.Journal             17        6
 ledger.Movement            9         113
 ledger.Voucher             7         45
 notes.EventType            8         0
 notes.Note                 14        100
 notes.NoteType             11        6
 outbox.Attachment          4         0
 outbox.Mail                8         0
 outbox.Recipient           6         0
 products.Product           12        8
 products.ProductCat        5         3
 rooms.Booking              24        3
 sales.Invoice              25        19
 sales.InvoiceItem          15        31
 sales.InvoicingMode        8         0
 sales.PaymentTerm          7         0
 sales.SalesRule            4         0
 sales.ShippingMode         5         0
 system.HelpText            4         2
 system.SiteConfig          16        1
 system.TextFieldTemplate   6         2
 uploads.Upload             11        0
 uploads.UploadType         2         0
 users.Authority            3         0
 users.Membership           3         0
 users.Team                 4         0
 users.User                 15        3
========================== ========= =======
<BLANKLINE>



User profiles
-------------

Rolf is the local system administrator, he has a complete menu:

>>> ses = settings.SITE.login('rolf') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen, Organisationen, Partner, Kursleiter, Teilnehmer
- Kurse : Kurse, Offene Einschreibungsanfragen, Auszustellende Teilnahmebescheinigungen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Buchungen
- Produkte : Produkte, Produktkategorien
- Verkauf : Verkaufsrechnungen (S), Zu fakturieren
- Einkauf : Einkaufsrechnungen (P), Zahlungsaufträge (PO)
- Financial : Bestbank (B), Cash (C), Miscellaneous Journal Entries (M)
- Büro : Meine Notizen, Mein E-Mail-Ausgang
- Berichte :
  - Buchhaltung : Tätigkeitsbericht
- Konfigurierung :
  - Büro : Meine Einfügetexte, Notizarten, Ereignisarten, Upload-Arten
  - System : Site-Parameter, Benutzer, Teams, Inhaltstypen, Hilfetexte
  - Kontakte : Länder, Orte, Organisationsarten, Funktionen
  - Kurse : Instructor Types, Participant Types, Themen, Kurs-Serien, Timetable Slots
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Termine, Gastrollen, Ereignisarten, Externe Kalender
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten, Journale
  - Verkauf : Fakturationsmodi, Lieferarten, Zahlungsbedingungen
- Explorer :
  - Büro : Einfügetexte, Notizen, Uploads, E-Mail-Ausgänge, Anhänge
  - System : Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile
  - Kontakte : Kontaktpersonen
  - Kurse : Einschreibungen, Einschreibungs-Zustände
  - Kalender : Aufgaben, Gäste, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - Buchhaltung : Rechnungen, Belege, VoucherTypes, Bewegungen, Geschäftsjahre
  - MWSt. : VatRegimes, TradeTypes, VatClasses
  - Financial : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge
- Site : Info

