.. _voga.specs.invoicing:

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
at three places: 

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



The demo database contains exactly one plan:

>>> obj = rt.modules.invoicing.Plan.objects.all()[0]

>>> rt.show('invoicing.ItemsByPlan', obj)  #doctest: +REPORT_UDIFF
===================== =================================== ========= ============== =================
 Selected              Partner                             Number    Amount         Product invoice
--------------------- ----------------------------------- --------- -------------- -----------------
 Yes                   Radermacher Hedi                    3         150,00         SLS 1
 Yes                   Radermacher Edgard                  5         220,00         SLS 2
 Yes                   Radermacher Christian               5         250,00         SLS 3
 Yes                   Meier Marie-Louise                  2         130,00         SLS 4
 Yes                   Laschet Laura                       5         250,00         SLS 5
 Yes                   Kaivers Karl                        4         170,00         SLS 6
 Yes                   Jonas Josef                         4         200,00         SLS 7
 Yes                   Jacobs Jacqueline                   3         180,00         SLS 8
 Yes                   Hilgers Hildegard                   4         200,00         SLS 9
 Yes                   Groteclaes Gregory                  5         250,00
 Yes                   Engels Edgar                        3         90,00
 Yes                   Evers Eberhart                      4         200,00
 Yes                   Dobbelstein-Demeulenaere Dorothée   5         250,00
 Yes                   Demeulenaere Dorothée               4         170,00
 Yes                   Charlier Ulrike                     3         150,00
 Yes                   Lahm Lisa                           4         230,00
 Yes                   Vandenmeulenbos Marie-Louise        4         200,00
 Yes                   Dupont Jean                         2         70,00
 Yes                   di Rupo Didier                      4         200,00
 Yes                   Radermacher Jean                    2         100,00
 Yes                   Radermacher Guido                   2         130,00
 Yes                   Radermacher Alfons                  3         120,00
 Yes                   Leffin Josefine                     4         170,00
 Yes                   Emonts Daniel                       3         210,00
 Yes                   Bastiaensen Laurent                 4         230,00
 Yes                   Altenberg Hans                      4         200,00
 Yes                   Arens Annette                       3         120,00
 Yes                   Jeanémart Jérôme                    2         70,00
 Yes                   Brecht Bernd                        2         70,00
 Yes                   Ärgerlich Erna                      3         150,00
 Yes                   Östges Otto                         3         150,00
 Yes                   Emonts-Gast Erna                    3         150,00
 Yes                   Faymonville Luc                     3         120,00
 Yes                   Dericum Daniel                      3         90,00
 Yes                   Martelaer Mark                      2         100,00
 **Total (35 rows)**                                       **119**   **5 740,00**
===================== =================================== ========= ============== =================
<BLANKLINE>


On the API level it defines the :class:`Invoiceable
<lino_cosi.lib.invoicing.mixins.Invoiceable>` mixin.

Lino Voga uses this functionality by extending :class:`Enrolment
<lino_cosi.lib.courses.models.Enrolment>` so that it inherits from
:class:`Invoiceable <lino_cosi.lib.invoicing.mixins.Invoiceable>`. In
Lino Voga, enrolments are the things for which they write invoices.

Another invoiceable thing in Lino Voga is when they rent a room to a
third-party organisation. This is called a :class:`Booking
<lino_voga.lib.rooms.models.Booking>`.

IOW, in Lino Voga both :class:`Enrolment
<lino_cosi.lib.courses.models.Enrolment>` and :class:`Booking
<lino_voga.lib.rooms.models.Booking>` are :class:`Invoiceable
<lino_cosi.lib.invoicing.mixins.Invoiceable>`:

>>> rt.models_by_base(rt.modules.invoicing.Invoiceable)
[<class 'lino_voga.lib.courses.models.Enrolment'>, <class 'lino_voga.lib.rooms.models.Booking'>]


Invoicings
==========

The detail window of an enrolment shows all invoicings of that
enrolment:

>>> obj = courses.Enrolment.objects.get(pk=83)
>>> rt.show('invoicing.InvoicingsByInvoiceable', obj)  #doctest: +REPORT_UDIFF
==================== ============================== ========== ============== ============ ==================
 Product invoice      Heading                        Quantity   Voucher date   State        Number of events
-------------------- ------------------------------ ---------- -------------- ------------ ------------------
 SLS 9                [1] Enrolment to Activity #8   1          22/05/2014     Registered   12
 **Total (1 rows)**                                  **1**                                  **12**
==================== ============================== ========== ============== ============ ==================
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

There are 24 enrolments matching this condition:

>>> Enrolment = rt.models.courses.Enrolment
>>> EnrolmentStates = rt.models.courses.EnrolmentStates
>>> qs = Enrolment.objects.filter(start_date__isnull=False)
>>> qs = qs.filter(state=EnrolmentStates.confirmed)
>>> qs = qs.filter(fee__number_of_events__isnull=True)
>>> qs = qs.order_by('request_date')
>>> qs.count()
24

We want only those for which an invoice has been generated. Above
number shrinks to 8:

>>> from django.db.models import Count
>>> qs = qs.annotate(invoicings_count=Count('invoicings'))
>>> qs = qs.filter(invoicings_count__gt=0)
>>> qs.count()
8

Let's select the corresponding invoice items:

>>> InvoiceItem = dd.plugins.invoicing.item_model
>>> qs2 = InvoiceItem.objects.filter(
...     invoiceable_id__in=qs.values_list('id', flat=True))
>>> qs2.count()
8

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
--- Invoice #1 for enrolment #95 (Activity #20 / Hedi Radermacher (MLS)):
Title: Enrolment to Activity #20
Start date: 30/05/2014
Missed events: 12/05/2014, 19/05/2014, 26/05/2014
Description:
Time: Every Monday 18:00-19:30.
Tariff: 20€.
Scheduled dates:
02/06/2014, 16/06/2014, 23/06/2014, 30/06/2014, 07/07/2014, 14/07/2014, 28/07/2014, 
--- Invoice #2 for enrolment #128 (Activity #3 / Edgard Radermacher (MCS)):
Title: Enrolment to Activity #3
Start date: 12/05/2014
Missed events: 28/04/2014, 05/05/2014, 12/05/2014
Description:
Time: Every Monday 13:30-15:00.
Tariff: 20€.
Scheduled dates:
12/05/2014, 19/05/2014, 26/05/2014, 02/06/2014, 16/06/2014, 23/06/2014, 
--- Invoice #4 for enrolment #194 (Activity #19 / Marie-Louise Meier (MS)):
Title: Enrolment to Activity #19
Start date: 30/05/2014
Missed events: 07/03/2014, 14/03/2014, 21/03/2014, 28/03/2014, 04/04/2014, 11/04/2014
Description:
Time: Every Friday 19:00-20:00.
Tariff: 80€.
Scheduled dates:
--- Invoice #6 for enrolment #86 (Activity #11 / Karl Kaivers (MLS)):
Title: Enrolment to Activity #11
Start date: 30/05/2014
Missed events: 12/05/2014, 19/05/2014, 26/05/2014
Description:
Time: Every Monday 13:30-14:30.
Tariff: 20€.
Scheduled dates:
02/06/2014, 16/06/2014, 23/06/2014, 30/06/2014, 07/07/2014, 14/07/2014, 28/07/2014, 
--- Invoice #7 for enrolment #155 (Activity #5 / Josef Jonas (MEC)):
Title: Enrolment to Activity #5
Start date: 12/05/2014
Missed events: 25/04/2014, 02/05/2014, 09/05/2014
Description:
Time: Every Friday 13:30-15:00.
Tariff: 20€.
Scheduled dates:
16/05/2014, 23/05/2014, 30/05/2014, 06/06/2014, 13/06/2014, 
--- Invoice #8 for enrolment #119 (Activity #19 / Jacqueline Jacobs (MES)):
Title: Enrolment to Activity #19
Start date: 12/05/2014
Missed events: 07/03/2014, 14/03/2014, 21/03/2014, 28/03/2014, 04/04/2014, 11/04/2014
Description:
Time: Every Friday 19:00-20:00.
Tariff: 80€.
Scheduled dates:

Let's have a closer look at the first of above invoicings.

>>> course = rt.models.courses.Course.objects.get(pk=20)

These are the scheduled events for the course:

>>> qs = course.events_by_course.order_by('start_date')
>>> print(', '.join([dd.fds(e.start_date) for e in qs]))
12/05/2014, 19/05/2014, 26/05/2014, 02/06/2014, 16/06/2014, 23/06/2014, 30/06/2014, 07/07/2014, 14/07/2014, 28/07/2014

But our enrolment starts later:

>>> enr = rt.models.courses.Enrolment.objects.get(pk=95)
>>> print(dd.fds(enr.start_date))
30/05/2014
>>> enr.end_date

So it missed the first three events and covers only the following
events:

>>> qs = rt.models.system.PeriodEvents.started.add_filter(qs, enr)
>>> print(', '.join([dd.fds(e.start_date) for e in qs]))
02/06/2014, 16/06/2014, 23/06/2014, 30/06/2014, 07/07/2014, 14/07/2014, 28/07/2014

