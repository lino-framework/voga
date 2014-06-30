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
26 apps: about, contenttypes, system, users, countries, contacts, lists, courses, extensible, cal, rooms, products, accounts, ledger, vat, sales, finan, iban, notes, uploads, outbox, excerpts, lino_faggio, appypod, export_excel, djangosite.
69 models:
========================== ========= =======
 Name                       #fields   #rows
-------------------------- --------- -------
 accounts.Account           13        12
 accounts.Chart             4         1
 accounts.Group             7         7
 cal.Calendar               6         7
 cal.Event                  23        320
 cal.EventType              16        7
 cal.Guest                  6         0
 cal.GuestRole              6         0
 cal.Priority               5         9
 cal.RecurrentEvent         21        9
 cal.RemoteCalendar         7         0
 cal.Room                   9         6
 cal.Subscription           4         0
 cal.Task                   17        0
 contacts.Company           28        19
 contacts.CompanyType       7         16
 contacts.Partner           24        88
 contacts.Person            31        69
 contacts.Role              4         0
 contacts.RoleType          4         5
 contenttypes.ContentType   4         70
 countries.Country          6         8
 countries.Place            8         76
 courses.Course             23        23
 courses.Enrolment          9         100
 courses.Line               13        9
 courses.Pupil              33        35
 courses.PupilType          5         4
 courses.Slot               5         0
 courses.Teacher            33        8
 courses.TeacherType        5         4
 courses.Topic              4         4
 excerpts.Excerpt           11        0
 excerpts.ExcerptType       14        1
 finan.BankStatement        11        3
 finan.BankStatementItem    11        9
 finan.JournalEntry         9         0
 finan.JournalEntryItem     11        0
 finan.PaymentOrder         11        3
 finan.PaymentOrderItem     10        15
 ledger.AccountInvoice      18        20
 ledger.InvoiceItem         9         32
 ledger.Journal             17        6
 ledger.Movement            9         98
 ledger.Voucher             7         45
 lists.List                 7         0
 lists.ListType             4         0
 lists.Member               7         0
 notes.EventType            8         0
 notes.Note                 16        100
 notes.NoteType             10        6
 outbox.Attachment          4         0
 outbox.Mail                8         0
 outbox.Recipient           6         0
 products.Product           12        8
 products.ProductCat        5         3
 rooms.Booking              24        3
 sales.Invoice              24        19
 sales.InvoiceItem          15        32
 sales.InvoicingMode        8         0
 sales.ShippingMode         5         0
 system.HelpText            4         2
 system.SiteConfig          15        1
 system.TextFieldTemplate   5         2
 uploads.Upload             9         0
 uploads.UploadType         7         0
 users.Authority            3         0
 users.User                 15        3
 vat.PaymentTerm            7         0
========================== ========= =======
<BLANKLINE>



Menus
-----

System administrator
--------------------

Rolf is the local system administrator, he has a complete menu:

>>> ses = settings.SITE.login('rolf') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen, Organisationen, Partner, Partnerlisten, Kursleiter, Teilnehmer
- Kurse : Kurse, Offene Einschreibungsanfragen, Auszustellende Teilnahmebescheinigungen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Buchungen
- Produkte : Produkte, Produktkategorien
- Verkauf : Verkaufsrechnungen (S), Zu fakturieren
- Einkauf : Einkaufsrechnungen (P), Zahlungsaufträge (PO)
- Financial : Bestbank (B), Kasse (C), Diverse Buchungen (M)
- Büro : Meine Notizen, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge
- Berichte :
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
- Konfigurierung :
  - Büro : Meine Einfügetexte, Notizarten, Ereignisarten, Upload-Arten, Auszugsarten
  - System : Site-Parameter, Benutzer, Inhaltstypen, Hilfetexte
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen, Listenarten
  - Kurse : Kursleiterarten, Teilnehmerarten, Themen, Kursserien, Timetable Slots
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Termine, Gastrollen, Ereignisarten, Externe Kalender
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten, Journale
  - MWSt. : Zahlungsbedingungen
  - Verkauf : Lieferarten
 - Explorer :
  - Büro : Einfügetexte, Notizen, Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Auszüge
  - System : Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile
  - Kontakte : Kontaktpersonen, Listenmitglieder
  - Kurse : Einschreibungen, Einschreibungs-Zustände
  - Kalender : Aufgaben, Gäste, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - Buchhaltung : Rechnungen, Belege, VoucherTypes, Bewegungen, Geschäftsjahre
  - MWSt. : VatRegimes, TradeTypes, VatClasses
  - Financial : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge
- Site : Info

