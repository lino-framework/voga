.. _voga.specs.invoicing:

How Lino Voga generates invoices
================================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_invoicing

    doctest init:

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.shell import *
    >>> #from lino.api.doctest import *
    

The general functionality for automatically generating invoices is
defined in :mod:`lino_cosi.lib.invoicing`.

On the user-visible level this plugin adds 
a menu entry :menuselection:`Journals --> Create invoices`,
and an action of type
:class:`StartInvoicing
<lino_cosi.lib.invoicing.actions.StartInvoicing>` (with a basket as
icon, referring to a shopping basket) at three places: 

- on every *partner* (generate invoices for this partner)
- on every *course* (generate invoices for all enrolments of this
  course)
- on every *journal* which supports automatic invoice generation. 

>>> rt.models.contacts.Partner.start_invoicing
<StartInvoicingForPartner start_invoicing ('Create invoices')>
>>> print(rt.models.contacts.Partner.start_invoicing.icon_name)
basket

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
 Yes                   Radermacher Hedi                    3         150,00         SLS 25
 Yes                   Radermacher Edgard                  5         220,00         SLS 26
 Yes                   Radermacher Christian               5         250,00         SLS 27
 Yes                   Meier Marie-Louise                  2         130,00         SLS 28
 Yes                   Laschet Laura                       5         250,00         SLS 29
 Yes                   Kaivers Karl                        4         170,00         SLS 30
 Yes                   Jonas Josef                         4         200,00         SLS 31
 Yes                   Jacobs Jacqueline                   3         180,00         SLS 32
 Yes                   Hilgers Hildegard                   4         200,00         SLS 33
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
==================== ============================ ========== ============== ============ ==================
 Product invoice      Heading                      Quantity   Voucher date   State        Number of events
-------------------- ---------------------------- ---------- -------------- ------------ ------------------
 SLS 33               [1] Enrolment to Course #8   1          22/05/2014     Registered   12
 **Total (1 rows)**                                **1**                                  **12**
==================== ============================ ========== ============== ============ ==================
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

The items of automtically generated invoices have a
:attr:`description` field whose context is defined by the
:xfile:`courses/Enrolment/item_description.html` template and can be
complex and application specific.

>>> def fmt(obj):
...     return u"{0} : **{1}** ---\n{2}".format(
...         obj.voucher.number, obj.title, obj.description)
>>> qs = rt.models.sales.InvoiceItem.objects.order_by('id')
>>> qs = qs.filter(description__isnull=False)
>>> # from lino.utils import rstgen
>>> # print(rstgen.ul([fmt(o) for o in qs]))
>>> print('\n'.join([fmt(o) for o in qs]))
25 : **Enrolment to Course #25** ---
Time: Every Friday 19:00-20:30.
Tariff: 80€.
<BLANKLINE>
Scheduled dates:
<BLANKLINE>
<BLANKLINE>
25/07/2014, 01/08/2014, 08/08/2014, 22/08/2014, 29/08/2014, 05/09/2014, 12/09/2014, 19/09/2014, 26/09/2014, 03/10/2014, 
<BLANKLINE>
25 : **[1] Enrolment to Course #15** ---
Time: Every Tuesday 13:30-14:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 21/05/2014.
<BLANKLINE>
25 : **Enrolment to Course #20** ---
Time: Every Monday 18:00-19:30.
Tariff: 20€.
<BLANKLINE>
Scheduled dates:
<BLANKLINE>
<BLANKLINE>
12/05/2014, 19/05/2014, 26/05/2014, 02/06/2014, 16/06/2014, 23/06/2014, 30/06/2014, 07/07/2014, 14/07/2014, 28/07/2014, 
<BLANKLINE>
26 : **[1] Enrolment to Course #23** ---
Time: Every Friday 19:00-20:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: .
<BLANKLINE>
26 : **[1] Enrolment to Course #13** ---
Time: Every Monday 13:30-14:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 02/05/2014.
<BLANKLINE>
26 : **Enrolment to Course #3** ---
Time: Every Monday 13:30-15:00.
Tariff: 20€.
<BLANKLINE>
Scheduled dates:
<BLANKLINE>
<BLANKLINE>
28/04/2014, 05/05/2014, 12/05/2014, 19/05/2014, 26/05/2014, 02/06/2014, 16/06/2014, 23/06/2014, 
<BLANKLINE>
26 : **[1] Enrolment to Course #8** ---
Time: Every Friday 13:30-15:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 29/05/2014.
<BLANKLINE>
26 : **[1] Enrolment to Course #23** ---
Time: Every Friday 19:00-20:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 30/05/2014.
<BLANKLINE>
27 : **[1] Enrolment to Course #22** ---
Time: Every Monday 18:00-19:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: .
<BLANKLINE>
27 : **[1] Enrolment to Course #12** ---
Time: Every Monday 11:00-12:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: .
<BLANKLINE>
27 : **[1] Enrolment to Course #17** ---
Time: Every Thursday 13:30-14:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 12/05/2014.
<BLANKLINE>
27 : **[1] Enrolment to Course #7** ---
Time: Every Wednesday 17:30-19:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 21/05/2014.
<BLANKLINE>
27 : **[1] Enrolment to Course #22** ---
Time: Every Monday 18:00-19:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 29/05/2014.
<BLANKLINE>
28 : **Enrolment to Course #19** ---
Time: Every Friday 19:00-20:00.
Tariff: 80€.
<BLANKLINE>
Scheduled dates:
<BLANKLINE>
<BLANKLINE>
07/03/2014, 14/03/2014, 21/03/2014, 28/03/2014, 04/04/2014, 11/04/2014, 
<BLANKLINE>
28 : **[1] Enrolment to Course #14** ---
Time: Every Tuesday 11:00-12:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: .
<BLANKLINE>
29 : **[1] Enrolment to Course #17** ---
Time: Every Thursday 13:30-14:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 21/05/2014.
<BLANKLINE>
29 : **[1] Enrolment to Course #7** ---
Time: Every Wednesday 17:30-19:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 29/05/2014.
<BLANKLINE>
29 : **[1] Enrolment to Course #22** ---
Time: Every Monday 18:00-19:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 30/05/2014.
<BLANKLINE>
29 : **[1] Enrolment to Course #12** ---
Time: Every Monday 11:00-12:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 09/06/2014.
<BLANKLINE>
29 : **[1] Enrolment to Course #17** ---
Time: Every Thursday 13:30-14:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: .
<BLANKLINE>
30 : **[1] Enrolment to Course #16** ---
Time: Every Thursday 11:00-12:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 12/05/2014.
<BLANKLINE>
30 : **[1] Enrolment to Course #6** ---
Time: Every Monday 13:30-15:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 21/05/2014.
<BLANKLINE>
30 : **Enrolment to Course #11** ---
Time: Every Monday 13:30-14:30.
Tariff: 20€.
<BLANKLINE>
Scheduled dates:
<BLANKLINE>
<BLANKLINE>
12/05/2014, 19/05/2014, 26/05/2014, 02/06/2014, 16/06/2014, 23/06/2014, 30/06/2014, 07/07/2014, 14/07/2014, 28/07/2014, 
<BLANKLINE>
30 : **[1] Enrolment to Course #16** ---
Time: Every Thursday 11:00-12:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 03/06/2014.
<BLANKLINE>
31 : **[1] Enrolment to Course #15** ---
Time: Every Tuesday 13:30-14:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 02/05/2014.
<BLANKLINE>
31 : **Enrolment to Course #5** ---
Time: Every Friday 13:30-15:00.
Tariff: 20€.
<BLANKLINE>
Scheduled dates:
<BLANKLINE>
<BLANKLINE>
25/04/2014, 02/05/2014, 09/05/2014, 16/05/2014, 23/05/2014, 30/05/2014, 06/06/2014, 13/06/2014, 
<BLANKLINE>
31 : **Enrolment to Course #25** ---
Time: Every Friday 19:00-20:30.
Tariff: 80€.
<BLANKLINE>
Scheduled dates:
<BLANKLINE>
<BLANKLINE>
25/07/2014, 01/08/2014, 08/08/2014, 22/08/2014, 29/08/2014, 05/09/2014, 12/09/2014, 19/09/2014, 26/09/2014, 03/10/2014, 
<BLANKLINE>
31 : **[1] Enrolment to Course #15** ---
Time: Every Tuesday 13:30-14:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 09/06/2014.
<BLANKLINE>
32 : **[1] Enrolment to Course #14** ---
Time: Every Tuesday 11:00-12:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: .
<BLANKLINE>
32 : **Enrolment to Course #19** ---
Time: Every Friday 19:00-20:00.
Tariff: 80€.
<BLANKLINE>
Scheduled dates:
<BLANKLINE>
<BLANKLINE>
07/03/2014, 14/03/2014, 21/03/2014, 28/03/2014, 04/04/2014, 11/04/2014, 
<BLANKLINE>
32 : **[1] Enrolment to Course #14** ---
Time: Every Tuesday 11:00-12:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 30/05/2014.
<BLANKLINE>
33 : **[1] Enrolment to Course #13** ---
Time: Every Monday 13:30-14:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: .
<BLANKLINE>
33 : **[1] Enrolment to Course #8** ---
Time: Every Friday 13:30-15:00.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 12/05/2014.
<BLANKLINE>
33 : **[1] Enrolment to Course #23** ---
Time: Every Friday 19:00-20:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 21/05/2014.
<BLANKLINE>
33 : **[1] Enrolment to Course #13** ---
Time: Every Monday 13:30-14:30.
Tariff: 50€/12 hours.
<BLANKLINE>
Your start date: 29/05/2014.
<BLANKLINE>
