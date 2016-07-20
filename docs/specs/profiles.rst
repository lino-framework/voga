.. _voga.specs.profiles:

=============
User profiles
=============

.. To run only this test::

    $ python setup.py test -s tests.SpecsTests.test_profiles

    doctest init:

    >>> import lino
    >>> lino.startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *


System administrator
====================

Robin is a system administrator, he has a complete menu:

>>> ses = rt.login('robin') 
>>> ses.user.profile
users.UserProfiles.admin:900
>>> ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Persons, Organizations, Partners, Partner Lists
- Office : Plausibility problems assigned to me, My Notifications, My Notes, My Uploads, My Outbox, My Excerpts
- Calendar : My appointments, Overdue appointments, My tasks, My guests, My presences, Bookings, Calendar
- Accounting :
  - Sales : Sales invoices (SLS), Sales credit notes (SLC)
  - Purchases : Purchase invoices (PRC)
  - Financial : Payment Orders (PMO), Cash (CSH), Bestbank (BNK), Miscellaneous Journal Entries (MSC)
  - Create invoices
- Activities : Participants, Instructors, -, Courses, Hikes, Journeys, -, Topics, Activity lines, -, Pending requested enrolments, Pending confirmed enrolments
- Reports :
  - System : Broken GFKs
  - Accounting : Situation, Activity Report, Debtors, Creditors
  - VAT : Due invoices
  - Activities : Status Report
- Configure :
  - System : Users, Site Parameters, Help Texts
  - Places : Countries, Places
  - Contacts : Organization types, Functions, List Types
  - Calendar : Calendars, Rooms, Priorities, Recurrent event rules, Guest Roles, Calendar Event Types, Remote Calendars
  - Tariffs : Tariffs, Tariff Categories
  - Accounting : Account Groups, Accounts, Journals, Accounting periods, Payment Terms
  - VAT : VAT rules, Paper types
  - Activities : Activity types, Instructor Types, Participant Types, Timetable Slots
  - Office : Note Types, Event Types, Upload Types, Excerpt Types
- Explorer :
  - System : Authorities, User Profiles, content types, Plausibility checkers, Plausibility problems, Notifications
  - Contacts : Contact Persons, List memberships
  - Calendar : Tasks, Presences, Subscriptions, Event states, Guest states, Task states
  - Accounting : Match rules, Vouchers, Voucher types, Movements, Fiscal Years, Trade types, Journal groups
  - VAT : VAT regimes, VAT Classes, Product invoices, Product invoice items, Invoicing plans
  - Activities : Activities, Enrolments, Enrolment states
  - Financial : Bank Statements, Journal Entries, Payment Orders
  - SEPA : Bank accounts
  - Office : Notes, Uploads, Upload Areas, Outgoing Mails, Attachments, Excerpts
- Site : About


>>> ses = rt.login('monique') 
>>> ses.user.profile
users.UserProfiles.secretary:200
>>> ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Persons, Organizations, Partners, Partner Lists
- Office : Plausibility problems assigned to me, My Notifications, My Notes, My Uploads, My Outbox, My Excerpts
- Calendar : My appointments, My tasks, My guests, My presences, Bookings, Calendar
- Accounting :
  - Sales : Sales invoices (SLS), Sales credit notes (SLC)
  - Purchases : Purchase invoices (PRC)
  - Financial : Payment Orders (PMO), Cash (CSH), Bestbank (BNK), Miscellaneous Journal Entries (MSC)
  - Create invoices
- Activities : Participants, Instructors, -, Courses, Hikes, Journeys, -, Activity lines, -, Pending requested enrolments, Pending confirmed enrolments
- Reports :
  - System : Broken GFKs
  - Accounting : Situation, Activity Report, Debtors, Creditors
  - VAT : Due invoices
  - Activities : Status Report
- Configure :
  - System : Site Parameters, Help Texts
  - Places : Countries
  - Calendar : Guest Roles
  - Tariffs : Tariffs, Tariff Categories
  - VAT : VAT rules, Paper types
  - Activities : Activity types, Instructor Types, Participant Types
- Explorer :
  - System : content types, Plausibility checkers, Plausibility problems, Notifications
  - Calendar : Presences, Event states, Guest states, Task states
  - VAT : VAT regimes, VAT Classes, Product invoices, Product invoice items
  - Activities : Activities, Enrolments
- Site : About


>>> ses = rt.login('marianne') 
>>> ses.user.profile
users.UserProfiles.user:100
>>> ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Persons, Organizations, Partners, Partner Lists
- Office : Plausibility problems assigned to me, My Notifications, My Notes, My Uploads, My Outbox, My Excerpts
- Calendar : My appointments, My tasks, My guests, My presences, Bookings, Calendar
- Accounting :
  - Sales : Sales invoices (SLS), Sales credit notes (SLC)
  - Purchases : Purchase invoices (PRC)
  - Financial : Payment Orders (PMO), Cash (CSH), Bestbank (BNK), Miscellaneous Journal Entries (MSC)
  - Create invoices
- Activities : Participants, Instructors, -, Courses, Hikes, Journeys, -, Activity lines, -
- Reports :
  - Accounting : Situation, Activity Report, Debtors, Creditors
  - VAT : Due invoices
  - Activities : Status Report
- Configure :
  - Places : Countries
  - Tariffs : Tariffs
  - VAT : VAT rules, Paper types
  - Activities : Activity types, Instructor Types, Participant Types
- Explorer :
  - VAT : VAT regimes, VAT Classes, Product invoices, Product invoice items
  - Activities : Activities
- Site : About
