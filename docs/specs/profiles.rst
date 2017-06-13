.. _voga.specs.profiles:

=============
User types
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
>>> ses.user.user_type
auth.UserTypes.admin:900
>>> ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Persons, Organizations, Partner Lists
- Office : Plausibility problems assigned to me, My Notification messages, My Notes, My Uploads, My Outbox, My Excerpts
- Calendar : My appointments, Overdue appointments, Unconfirmed appointments, My tasks, My guests, My presences, My overdue appointments, Bookings, Calendar
- Accounting :
  - Sales : Sales invoices (SLS), Sales credit notes (SLC)
  - Purchases : Purchase invoices (PRC)
  - Financial : Payment Orders (PMO), Cash (CSH), Bestbank (BNK), Miscellaneous Journal Entries (MSC)
  - Create invoices
- Activities : Participants, Instructors, -, Courses, Hikes, Journeys, -, Topics, Activity lines, -, Pending requested enrolments, Pending confirmed enrolments
- Reports :
  - Accounting : Situation, Activity Report, Debtors, Creditors
  - VAT : Due invoices
  - Activities : Status Report
- Configure :
  - System : Site Parameters, Users, Help Texts
  - Places : Countries, Places
  - Contacts : Organization types, Functions, List Types
  - Calendar : Calendars, Rooms, Priorities, Recurring events, Guest Roles, Calendar entry types, Recurrency policies, Remote Calendars
  - Tariffs : Tariffs, Tariff Categories
  - Accounting : Account Groups, Accounts, Journals, Accounting periods, Payment Terms
  - VAT : VAT rules, Paper types
  - Activities : Activity types, Instructor Types, Participant Types, Timetable Slots
  - Office : Note Types, Event Types, Upload Types, Excerpt Types
- Explorer :
  - System : Authorities, User types, content types, Plausibility checkers, Plausibility problems, Notification messages, Changes
  - Contacts : Contact Persons, Partners, List memberships
  - Calendar : Calendar entries, Tasks, Presences, Subscriptions, Event states, Guest states, Task states
  - Accounting : Match rules, Vouchers, Voucher types, Movements, Fiscal Years, Trade types, Journal groups
  - VAT : VAT regimes, VAT Classes, Product invoices, Product invoice items, Invoicing plans
  - Activities : Activities, Enrolments, Enrolment states
  - Financial : Bank Statements, Journal Entries, Payment Orders
  - SEPA : Bank accounts
  - Office : Notes, Uploads, Upload Areas, Outgoing Mails, Attachments, Excerpts
- Site : About


Monique is a secretary.   

>>> print(rt.login('monique').user.user_type)
Secretary

>>> rt.login('monique').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Persons, Organizations, Partner Lists
- Office : Plausibility problems assigned to me, My Notification messages, My Notes, My Uploads, My Outbox, My Excerpts
- Calendar : My appointments, Unconfirmed appointments, My tasks, My guests, My presences, My overdue appointments, Calendar
- Accounting :
  - Sales : Sales invoices (SLS), Sales credit notes (SLC)
  - Purchases : Purchase invoices (PRC)
  - Financial : Payment Orders (PMO), Cash (CSH), Bestbank (BNK), Miscellaneous Journal Entries (MSC)
  - Create invoices
- Activities : Participants, Instructors, -, Courses, Hikes, Journeys, -, Activity lines, -, Pending requested enrolments, Pending confirmed enrolments
- Reports :
  - Accounting : Situation, Activity Report, Debtors, Creditors
  - VAT : Due invoices
  - Activities : Status Report
- Configure :
  - System : Site Parameters, Help Texts
  - Places : Countries, Places
  - Contacts : Organization types, Functions, List Types
  - Calendar : Guest Roles
  - Tariffs : Tariffs, Tariff Categories
  - Activities : Activity types, Instructor Types, Participant Types
- Explorer :
  - System : content types, Plausibility checkers, Plausibility problems, Changes
  - Contacts : Contact Persons, Partners, List memberships
  - Calendar : Calendar entries, Presences, Event states, Guest states, Task states
  - VAT : Product invoices
  - Activities : Activities, Enrolments
- Site : About


Marianne is a "simple user".

>>> print(rt.login('marianne').user.user_type)
User

>>> rt.login('marianne').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Persons, Organizations, Partner Lists
- Office : Plausibility problems assigned to me, My Notification messages, My Notes, My Uploads, My Outbox, My Excerpts
- Calendar : My appointments, Unconfirmed appointments, My tasks, My guests, My presences, My overdue appointments, Calendar
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
  - Activities : Activity types, Instructor Types, Participant Types
- Explorer :
  - Contacts : Partners
  - VAT : Product invoices
- Site : About

>>> rt.login('tom').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Activities : My courses given, -, Courses, Hikes, Journeys, -
- Site : About
