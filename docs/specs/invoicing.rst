.. _voga.specs.invoicing:

================================
How Lino Voga generates invoices
================================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_invoicing

    doctest init:

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *
    

The general functionality for automatically generating invoices is
defined in :mod:`lino_cosi.lib.invoicing`.

On the user-visible level this plugin adds

- a menu entry :menuselection:`Journals --> Create invoices`,

and a :class:`StartInvoicing
<lino_cosi.lib.invoicing.actions.StartInvoicing>` 
action (with a basket as icon, referring to a shopping basket) 
at four places: 

- as a menu command :menuselection:`Accounting --> Create invoices`
- on every *partner* (generate invoices for this partner)
- on every *course* (generate invoices for all enrolments of this
  course)
- on every *journal* which supports automatic invoice generation. 

>>> rt.models.contacts.Partner.start_invoicing
<StartInvoicingForPartner start_invoicing ('Create invoices')>

>>> rt.models.courses.Course.start_invoicing
<StartInvoicingForCourse start_invoicing ('Create invoices')>

The *invoices journal* which supports automatic generation is
indirectly defined by the :attr:`voucher_model
<lino_cosi.lib.invoicing.Plugin.voucher_model>` setting.

>>> vt = dd.plugins.invoicing.get_voucher_type()
>>> vt.table_class.start_invoicing
<StartInvoicingForJournal start_invoicing ('Create invoices')>

>>> rt.models.invoicing.Plan.start_invoicing
<StartInvoicing start_invoicing ('Create invoices')>

On the API level it defines the :class:`Invoiceable
<lino_cosi.lib.invoicing.mixins.Invoiceable>` mixin.

Lino Voga uses this functionality by extending :class:`Enrolment
<lino_cosi.lib.courses.models.Enrolment>` so that it inherits from
:class:`Invoiceable <lino_cosi.lib.invoicing.mixins.Invoiceable>`. In
Lino Voga, enrolments are the things for which they write invoices.

Another invoiceable thing in Lino Voga is when they rent a room to a
third-party organisation.  This is called a :class:`Booking
<lino_voga.lib.rooms.models.Booking>`.

IOW, in Lino Voga both :class:`Enrolment
<lino_cosi.lib.courses.models.Enrolment>` and :class:`Booking
<lino_voga.lib.rooms.models.Booking>` are :class:`Invoiceable
<lino_cosi.lib.invoicing.mixins.Invoiceable>`:

>>> rt.models_by_base(rt.modules.invoicing.Invoiceable)
[<class 'lino_voga.lib.courses.models.Enrolment'>, <class 'lino_voga.lib.rooms.models.Booking'>]

Enrolments as invoiceables
==========================

:attr:`Enrolment.invoicing_info` is a summary of what has been
invoiced (and what hasn't) for a given enrolment.

>>> from textwrap import wrap
>>> for obj in courses.Enrolment.objects.all():
...     ii = '\n'.join(wrap(E.to_rst(obj.invoicing_info), 80))
...     print(u"{} : {} {}\n{}".format(obj.id, obj.course, obj.pupil, ii))
...     #doctest: +REPORT_UDIFF +NORMALIZE_WHITESPACE
1 : 001 Griechenland 2014 Annette Arens (ME)
<BLANKLINE>
2 : 002 London 2014 Annette Arens (ME)
<BLANKLINE>
3 : 004 comp Annette Arens (ME)
<BLANKLINE>
4 : 007C WWW Annette Arens (ME)
Invoiced : 13.05., 20.05. Not invoiced : 29.10., 05.11., 12.11., 19.11., 26.11.,
03.12., 17.12., 24.12., 31.12., 07.01., 14.01., 21.01., 28.01., 11.02., 25.02.,
04.03., 11.03., 18.03., 25.03., 01.04., 15.04., 22.04., 29.04., 06.05.
5 : 009C BT Annette Arens (ME)
Invoiced : 13.05., 20.05. Not invoiced : 16.04., 23.04., 30.04., 07.05., 21.05.,
28.05., 04.06., 11.06., 18.06., 25.06., 02.07., 16.07., 23.07., 30.07., 06.08.,
13.08., 20.08., 27.08., 10.09., 17.09., 24.09., 01.10., 08.10., 15.10., 22.10.,
05.11., 12.11., 19.11., 26.11., 03.12., 10.12., 17.12., 31.12., 07.01., 14.01.,
21.01., 28.01., 04.02., 11.02., 04.03., 11.03., 18.03., 25.03., 01.04., 08.04.,
15.04., 29.04., 06.05.
6 : 010C FG Laurent Bastiaensen (MES)
Invoiced : 06.10., 13.10., 20.10.
7 : 010C FG Laurent Bastiaensen (MES)
Invoiced : (...) 04.05., 11.05., 18.05. Not invoiced : 24.11., 01.12., 08.12.,
15.12., 29.12., 05.01., 12.01., 19.01., 26.01., 02.02., 09.02., 02.03., 09.03.,
16.03., 23.03.
8 : 011C FG Laurent Bastiaensen (MES)
Invoiced : (...) 27.04., 11.05., 18.05. Not invoiced : 06.10., 13.10., 20.10.,
27.10., 10.11., 17.11., 24.11., 01.12., 08.12., 15.12., 22.12., 05.01., 12.01.,
19.01., 26.01., 02.02., 09.02., 23.02., 09.03., 16.03.
9 : 012 Rücken Ulrike Charlier (ME)
<BLANKLINE>
10 : 013 Rücken Ulrike Charlier (ME)
<BLANKLINE>
11 : 018 SV Ulrike Charlier (ME)
<BLANKLINE>
12 : 019 SV Ulrike Charlier (ME)
<BLANKLINE>
13 : 020C GLQ Dorothée Demeulenaere (ME)
Invoiced : 28.07.
14 : 020C GLQ Dorothée Demeulenaere (ME)
Invoiced : (...) 04.05., 11.05., 18.05. Not invoiced : 08.09., 15.09., 22.09.,
06.10., 13.10., 20.10., 27.10., 03.11., 10.11., 17.11., 01.12., 08.12., 15.12.,
22.12., 29.12., 05.01., 12.01., 26.01., 02.02., 09.02., 23.02., 02.03., 09.03.,
16.03.
15 : 021C GLQ Dorothée Dobbelstein-Demeulenaere (ME)
Invoiced : (...) 27.02., 24.04., 15.05.
16 : 005 comp Dorothée Dobbelstein-Demeulenaere (ME)
<BLANKLINE>
17 : 008C WWW Daniel Emonts (ME)
Invoiced : (...) 14.11., 21.11., 28.11.
18 : 016 Rücken Edgar Engels (MES)
<BLANKLINE>
19 : 017 Rücken Edgar Engels (MES)
<BLANKLINE>
20 : 003 comp Luc Faymonville (ME)
<BLANKLINE>
21 : 003 comp Luc Faymonville (ME)
<BLANKLINE>
22 : 006C WWW Luc Faymonville (ME)
Not invoiced : 27.10., 03.11., 17.11., 24.11., 01.12., 08.12., 15.12., 22.12.,
29.12., 12.01., 19.01., 26.01., 02.02., 09.02., 23.02., 02.03., 16.03., 23.03.,
30.03., 13.04., 20.04., 27.04., 04.05., 18.05.
23 : 022C MED Luc Faymonville (ME)
Invoiced : (...) 23.02., 02.03., 16.03.
24 : 023C MED Gregory Groteclaes (ME)
Invoiced : (...) 20.02., 27.02., 06.03.
25 : 024C Yoga Gregory Groteclaes (ME)
Invoiced : 11.05., 18.05. Not invoiced : 23.03., 13.04., 20.04., 27.04., 04.05.
26 : 025C Yoga Gregory Groteclaes (ME)
Invoiced : (...) 16.01., 23.01., 30.01.
27 : 014 Rücken Gregory Groteclaes (ME)
<BLANKLINE>
28 : 014 Rücken Gregory Groteclaes (ME)
<BLANKLINE>
29 : 015 Rücken Gregory Groteclaes (ME)
<BLANKLINE>
30 : 001 Griechenland 2014 Jacqueline Jacobs (MES)
<BLANKLINE>
31 : 002 London 2014 Jacqueline Jacobs (MES)
<BLANKLINE>
32 : 004 comp Jacqueline Jacobs (MES)
<BLANKLINE>
33 : 007C WWW Jacqueline Jacobs (MES)
Invoiced : (...) 06.05., 13.05., 20.05. Not invoiced : 12.11., 19.11., 26.11.,
03.12., 17.12., 24.12., 31.12., 07.01., 14.01., 21.01., 28.01., 11.02., 25.02.,
04.03., 11.03., 18.03.
34 : 009C BT Karl Kaivers (MLS)
Invoiced : 02.04., 09.04., 16.04.
35 : 009C BT Karl Kaivers (MLS)
Invoiced : (...) 06.05., 13.05., 20.05.
36 : 010C FG Karl Kaivers (MLS)
Invoiced : (...) 04.05., 11.05., 18.05. Not invoiced : 06.10., 13.10., 20.10.,
03.11., 10.11., 17.11., 24.11., 01.12., 08.12., 15.12., 29.12., 05.01., 12.01.,
19.01., 26.01., 02.02., 09.02., 02.03., 09.03., 16.03.
37 : 011C FG Laura Laschet (ME)
Invoiced : (...) 27.04., 11.05., 18.05. Not invoiced : 06.10., 13.10., 20.10.,
27.10., 10.11., 17.11., 24.11., 01.12., 08.12., 15.12., 22.12., 05.01., 12.01.,
19.01., 26.01., 02.02., 09.02., 23.02., 09.03., 16.03.
38 : 012 Rücken Laura Laschet (ME)
<BLANKLINE>
39 : 013 Rücken Laura Laschet (ME)
<BLANKLINE>
40 : 018 SV Laura Laschet (ME)
<BLANKLINE>
41 : 019 SV Marie-Louise Meier (MS)
<BLANKLINE>
42 : 019 SV Marie-Louise Meier (MS)
<BLANKLINE>
43 : 020C GLQ Marie-Louise Meier (MS)
Invoiced : (...) 04.05., 11.05., 18.05. Not invoiced : 28.07., 11.08., 18.08.,
25.08., 01.09., 08.09., 15.09., 22.09., 06.10., 13.10., 20.10., 27.10., 03.11.,
10.11., 17.11., 01.12., 08.12., 15.12., 22.12., 29.12., 05.01., 12.01., 26.01.,
02.02., 09.02., 23.02., 02.03., 09.03., 16.03., 30.03., 13.04., 20.04.
44 : 021C GLQ Marie-Louise Meier (MS)
Invoiced : (...) 27.02., 24.04., 15.05.
45 : 005 comp Marie-Louise Meier (MS)
<BLANKLINE>
46 : 008C WWW Erna Emonts-Gast (ME)
Invoiced : (...) 17.04., 24.04., 15.05.
47 : 016 Rücken Alfons Radermacher (MS)
<BLANKLINE>
48 : 017 Rücken Alfons Radermacher (MS)
<BLANKLINE>
49 : 017 Rücken Alfons Radermacher (MS)
<BLANKLINE>
50 : 003 comp Christian Radermacher (ME)
<BLANKLINE>
51 : 006C WWW Christian Radermacher (ME)
Not invoiced : 27.10., 03.11., 17.11., 24.11., 01.12., 08.12., 15.12., 22.12.,
29.12., 12.01., 19.01., 26.01., 02.02., 09.02., 23.02., 02.03., 16.03., 23.03.,
30.03., 13.04., 20.04., 27.04., 04.05., 18.05.
52 : 022C MED Christian Radermacher (ME)
Invoiced : 14.10., 21.10. Not invoiced : 23.09., 30.09., 07.10.
53 : 023C MED Christian Radermacher (ME)
Not invoiced : 06.02., 13.02., 20.02., 27.02., 06.03., 13.03., 27.03., 10.04.,
17.04., 24.04., 08.05., 15.05.
54 : 024C Yoga Guido Radermacher (ME)
Invoiced : 11.05., 18.05. Not invoiced : 23.03., 13.04., 20.04., 27.04., 04.05.
55 : 025C Yoga Guido Radermacher (ME)
Invoiced : 08.11., 22.11., 29.11.
56 : 025C Yoga Guido Radermacher (ME)
Invoiced : (...) 16.01., 23.01., 30.01.
57 : 014 Rücken Hedi Radermacher (MLS)
<BLANKLINE>
58 : 015 Rücken Hedi Radermacher (MLS)
<BLANKLINE>
59 : 001 Griechenland 2014 Hedi Radermacher (MLS)
<BLANKLINE>
60 : 002 London 2014 Hedi Radermacher (MLS)
<BLANKLINE>
61 : 004 comp Didier di Rupo (ME)
<BLANKLINE>
62 : 007C WWW Otto Östges (ME)
Invoiced : 12.11. Not invoiced : 29.10., 05.11.
63 : 007C WWW Otto Östges (ME)
Invoiced : (...) 06.05., 13.05., 20.05. Not invoiced : 17.12., 24.12., 31.12.,
07.01., 14.01., 21.01., 28.01., 11.02., 25.02., 04.03., 11.03., 18.03., 25.03.,
01.04., 15.04., 22.04.
64 : 009C BT Otto Östges (ME)
Invoiced : (...) 06.05., 13.05., 20.05. Not invoiced : 02.04., 09.04., 16.04.,
23.04., 30.04., 07.05., 21.05., 28.05., 04.06., 11.06., 18.06., 25.06., 02.07.,
16.07., 23.07., 30.07., 06.08., 13.08., 20.08., 27.08., 10.09., 17.09., 24.09.,
01.10., 08.10., 15.10., 22.10., 05.11., 12.11., 19.11., 26.11., 03.12., 10.12.,
17.12., 31.12., 07.01., 14.01., 21.01., 28.01., 04.02., 11.02., 04.03., 11.03.,
18.03., 25.03., 01.04., 08.04., 15.04.
65 : 010C FG Otto Östges (ME)
Invoiced : (...) 04.05., 11.05., 18.05. Not invoiced : 06.10., 13.10., 20.10.,
03.11., 10.11., 17.11., 24.11., 01.12., 08.12., 15.12., 29.12., 05.01., 12.01.,
19.01., 26.01., 02.02., 09.02., 02.03., 09.03., 16.03.
66 : 011C FG Otto Östges (ME)
Invoiced : (...) 13.10., 20.10., 27.10.
67 : 012 Rücken Otto Östges (ME)
<BLANKLINE>
68 : 013 Rücken Jean Dupont (ML)
<BLANKLINE>
69 : 018 SV Jean Dupont (ML)
<BLANKLINE>
70 : 018 SV Jean Dupont (ML)
<BLANKLINE>
71 : 019 SV Mark Martelaer (ME)
<BLANKLINE>
72 : 020C GLQ Mark Martelaer (ME)
Invoiced : (...) 04.05., 11.05., 18.05. Not invoiced : 28.07., 11.08., 18.08.,
25.08., 01.09., 08.09., 15.09., 22.09., 06.10., 13.10., 20.10., 27.10., 03.11.,
10.11., 17.11., 01.12., 08.12., 15.12., 22.12., 29.12., 05.01., 12.01., 26.01.,
02.02., 09.02., 23.02., 02.03., 09.03., 16.03., 30.03., 13.04., 20.04.
73 : 021C GLQ Mark Martelaer (ME)
Invoiced : 01.08., 08.08. Not invoiced : 25.07.
74 : 005 comp Marie-Louise Vandenmeulenbos (ME)
<BLANKLINE>
75 : 008C WWW Marie-Louise Vandenmeulenbos (ME)
Invoiced : (...) 17.04., 24.04., 15.05.
76 : 016 Rücken Marie-Louise Vandenmeulenbos (ME)
<BLANKLINE>
77 : 016 Rücken Marie-Louise Vandenmeulenbos (ME)
<BLANKLINE>
78 : 017 Rücken Marie-Louise Vandenmeulenbos (ME)
<BLANKLINE>
79 : 003 comp Marie-Louise Vandenmeulenbos (ME)
<BLANKLINE>
80 : 006C WWW Lisa Lahm (MEL)
Invoiced : (...) 03.11., 17.11., 24.11.
81 : 022C MED Bernd Brecht (MS)
Invoiced : (...) 23.02., 02.03., 16.03.
82 : 023C MED Bernd Brecht (MS)
Not invoiced : 20.02., 27.02., 06.03., 13.03., 27.03., 10.04., 17.04., 24.04.,
08.05., 15.05.


>>> rt.show(courses.Enrolments)
...     #doctest: +REPORT_UDIFF +ELLIPSIS
================= ======================= ======================================== =============== =================
 Date of request   Activity                Participant                              Workflow        Author
----------------- ----------------------- ---------------------------------------- --------------- -----------------
 14/09/2013        022C MED                Luc Faymonville (ME)                     **Requested**   Romain Raffault
 14/09/2013        022C MED                Christian Radermacher (ME)               **Confirmed**   Romain Raffault
 19/09/2013        022C MED                Bernd Brecht (MS)                        **Requested**   Romain Raffault
 08/11/2013        024C Yoga               Gregory Groteclaes (ME)                  **Confirmed**   Robin Rood
 08/11/2013        025C Yoga               Guido Radermacher (ME)                   **Confirmed**   Marianne Martin
 08/11/2013        025C Yoga               Guido Radermacher (ME)                   **Confirmed**   Marianne Martin
 23/11/2013        025C Yoga               Gregory Groteclaes (ME)                  **Confirmed**   Marianne Martin
 23/11/2013        024C Yoga               Guido Radermacher (ME)                   **Confirmed**   Robin Rood
 26/02/2014        003 comp                Christian Radermacher (ME)               **Confirmed**   Marianne Martin
 08/03/2014        009C BT                 Otto Östges (ME)                         **Confirmed**   Romain Raffault
 ...
 11/07/2015        017 Rücken              Alfons Radermacher (MS)                  **Confirmed**   Robin Rood
 11/07/2015        017 Rücken              Alfons Radermacher (MS)                  **Confirmed**   Robin Rood
 11/07/2015        012 Rücken              Otto Östges (ME)                         **Confirmed**   Marianne Martin
 11/07/2015        016 Rücken              Marie-Louise Vandenmeulenbos (ME)        **Confirmed**   Rolf Rompen
 11/07/2015        016 Rücken              Marie-Louise Vandenmeulenbos (ME)        **Confirmed**   Rolf Rompen
 26/07/2015        017 Rücken              Edgar Engels (MES)                       **Confirmed**   Robin Rood
 26/07/2015        016 Rücken              Alfons Radermacher (MS)                  **Confirmed**   Rolf Rompen
 26/07/2015        013 Rücken              Jean Dupont (ML)                         **Confirmed**   Monique Mommer
================= ======================= ======================================== =============== =================
<BLANKLINE>


Invoicings
==========

The detail window of an enrolment shows all invoicings of that
enrolment:

>>> obj = courses.Enrolment.objects.get(pk=64)
>>> rt.show('invoicing.InvoicingsByInvoiceable', obj)  #doctest: +REPORT_UDIFF
==================== ================================== ========== ============== ============ ==================
 Product invoice      Heading                            Quantity   Voucher date   State        Number of events
-------------------- ---------------------------------- ---------- -------------- ------------ ------------------
 SLS 9                [1] Enrolment to 009C BT           1          01/04/2014     Registered   12
 SLS 22               [2] Renewal Enrolment to 009C BT   1          01/07/2014     Registered   12
 SLS 31               [3] Renewal Enrolment to 009C BT   1          01/10/2014     Registered   12
 SLS 53               [4] Renewal Enrolment to 009C BT   1          01/01/2015     Registered   12
 **Total (4 rows)**                                      **4**                                  **48**
==================== ================================== ========== ============== ============ ==================
<BLANKLINE>


Subscription courses
====================

Subscription courses are courses for which the customer pays *a given
number of events*, not simply all events of that course. This means
that the presences for these courses must have been entered.

A subscription course does not end and start at a given date, the
course itself is continously being given. Participants can start on
any time of the year. They usually pay for 12 sessions in advance (the
first invoice for that enrolment), and Lino must write a new invoice
every 12 weeks.


Descriptions
============

The items of automatically generated invoices have a
:attr:`description` field whose context is defined by the
:xfile:`courses/Enrolment/item_description.html` template and can be
complex and application specific.

.. literalinclude:: /../lino_voga/lib/voga/config/courses/Enrolment/item_description.html


Scheduled dates
===============

For enrolments in non-continuous courses (i.e. with a fee whose
:attr:`number_of_events` is empty), the description on the invoice
includes a list of "Scheduled dates". This is basically an enumeration
of the planned events of that course.

It can happen that a participant joins a started course afterwards and
pays less, in function of the events he didn't attend. The amount to
be invoiced in such cases is subject to individual discussion, and the
user simply enters that amount in the enrolment.

The following code snippets tests whether above is true.

There are 11 enrolments matching this condition:

>>> Enrolment = rt.models.courses.Enrolment
>>> EnrolmentStates = rt.models.courses.EnrolmentStates
>>> qs = Enrolment.objects.filter(start_date__isnull=False)
>>> qs = qs.filter(state=EnrolmentStates.confirmed)
>>> qs = qs.filter(fee__number_of_events__isnull=True)
>>> qs = qs.order_by('request_date')
>>> qs.count()
11

We want only those for which an invoice has been generated. Above
number shrinks to 2:

>>> from django.db.models import Count
>>> qs = qs.annotate(invoicings_count=Count('invoicings'))
>>> qs = qs.filter(invoicings_count__gt=0)
>>> qs.count()
2

Let's select the corresponding invoice items:

>>> InvoiceItem = dd.plugins.invoicing.item_model
>>> qs2 = InvoiceItem.objects.filter(
...     invoiceable_id__in=qs.values_list('id', flat=True))
>>> qs2.count()
2

Now we define a utility function which prints out what we want to see
for each of these items:

>>> def fmt(obj):
...     enr = obj.invoiceable
...     missed_events = enr.course.events_by_course.filter(
...         start_date__lte=enr.start_date)
...     if missed_events.count() == 0: return
...     missed_events = ', '.join([dd.fds(o.start_date) for o in missed_events])
...     print(u"--- Invoice #{0} for enrolment #{1} ({2}):".format(
...         obj.voucher.number, enr.id, enr))
...     print("Title: {0}".format(obj.title))
...     print("Start date: " + dd.fds(obj.invoiceable.start_date))
...     print("Missed events: {0}".format(missed_events))
...     print("Description:")
...     print(noblanklines(obj.description))


And run it:

>>> for o in qs2: fmt(o)  #doctest: +REPORT_UDIFF
--- Invoice #16 for enrolment #61 (004 comp / Didier di Rupo (ME)):
Title: Enrolment to 004 comp
Start date: 02/04/2014
Missed events: 19/03/2014, 26/03/2014, 02/04/2014
Description:
Time: Every Wednesday 17:30-19:00.
Tariff: 20€.
Scheduled dates:
02/04/2014, 09/04/2014, 16/04/2014, 23/04/2014, 30/04/2014, 07/05/2014, 
--- Invoice #19 for enrolment #21 (003 comp / Luc Faymonville (ME)):
Title: Enrolment to 003 comp
Start date: 06/05/2014
Missed events: 24/03/2014, 31/03/2014, 07/04/2014, 14/04/2014, 28/04/2014, 05/05/2014
Description:
Time: Every Monday 13:30-15:00.
Tariff: 20€.
Scheduled dates:
12/05/2014, 19/05/2014, 

Let's have a closer look at the first of above invoicings.

>>> course = rt.models.courses.Course.objects.get(pk=4)

These are the scheduled events for the course:

>>> qs = course.events_by_course.order_by('start_date')
>>> print(', '.join([dd.fds(e.start_date) for e in qs]))
19/03/2014, 26/03/2014, 02/04/2014, 09/04/2014, 16/04/2014, 23/04/2014, 30/04/2014, 07/05/2014

But our enrolment starts later:

>>> enr = rt.models.courses.Enrolment.objects.get(pk=61)
>>> print(dd.fds(enr.start_date))
02/04/2014
>>> enr.end_date

So it missed the first three events and covers only the following
events:

>>> qs = rt.models.system.PeriodEvents.started.add_filter(qs, enr)
>>> print(', '.join([dd.fds(e.start_date) for e in qs]))
02/04/2014, 09/04/2014, 16/04/2014, 23/04/2014, 30/04/2014, 07/05/2014


Invoicing plan
==============


The demo database contains exactly one plan:

>>> obj = rt.modules.invoicing.Plan.objects.all()[0]

>>> rt.show('invoicing.ItemsByPlan', obj)  #doctest: +REPORT_UDIFF
==================== ======================= ============================================= ============ ========= ==========
 Selected             Partner                 Preview                                       Amount       Invoice   Workflow
-------------------- ----------------------- --------------------------------------------- ------------ --------- ----------
 Yes                  Bastiaensen Laurent     [3] Renewal Enrolment to 010C FG (50.00 €)    50,00        SLS 70
 Yes                  Faymonville Luc         [3] Renewal Enrolment to 006C WWW (48.00 €)   48,00        SLS 71
 Yes                  Radermacher Christian   [3] Renewal Enrolment to 006C WWW (48.00 €)   48,00        SLS 72
 Yes                  Arens Annette           [3] Renewal Enrolment to 007C WWW (48.00 €)   48,00        SLS 73
 Yes                  Brecht Bernd            [1] Enrolment to 023C MED (64.00 €)           64,00        SLS 74
 **Total (5 rows)**                                                                         **258,00**
==================== ======================= ============================================= ============ ========= ==========
<BLANKLINE>


