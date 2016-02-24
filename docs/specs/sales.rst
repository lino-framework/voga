.. _voga.specs.sales:

Sales
=====

.. to test only this doc:

    $ python setup.py test -s tests.DocsTests.test_sales

    doctest init:

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.shell import *
    >>> #from lino.api.doctest import *
    

How Lino Voga generates invoices
================================

The general functionality for automatically generating invoices is in
:mod:`lino_cosi.lib.auto.sales` which extends
:mod:`lino_cosi.lib.sales`.

On the user-visible level it adds a :class:`CreateInvoice
<lino_cosi.lib.auto.sales.models.CreateInvoice>` action per partner, a
table :class:`InvoicesToCreate
<lino_cosi.lib.auto.sales.models.InvoicesToCreate>` to the main menu,
and a field :attr:`invoiceable` per invoice item.

>>> rt.modules.contacts.Partner.create_invoice
<CreateInvoiceForPartner create_invoice (u'Create invoice')>

>>> rt.show('sales.InvoicesToCreate')  #doctest: +REPORT_UDIFF
===================== =========== ============================== ============ ========================
 First date            Last date   Partner                        Amount       Actions
--------------------- ----------- ------------------------------ ------------ ------------------------
 9/26/13               9/26/13     Östges Otto                    50,00        **Invoices to create**
 9/29/13               9/29/13     Radermacher Hedi               20,00        **Invoices to create**
 10/2/13               10/2/13     Radermacher Christian          50,00        **Invoices to create**
 10/5/13               10/5/13     Meier Marie-Louise             50,00        **Invoices to create**
 10/8/13               10/8/13     Kaivers Karl                   20,00        **Invoices to create**
 10/26/13              10/26/13    Lahm Lisa                      80,00        **Invoices to create**
 10/29/13              10/29/13    Dupont Jean                    50,00        **Invoices to create**
 11/1/13               11/1/13     di Rupo Didier                 50,00        **Invoices to create**
 11/4/13               11/4/13     Radermacher Guido              80,00        **Invoices to create**
 11/7/13               11/7/13     Radermacher Alfons             50,00        **Invoices to create**
 11/10/13              11/10/13    Leffin Josefine                20,00        **Invoices to create**
 11/13/13              11/13/13    Jonas Josef                    80,00        **Invoices to create**
 11/28/13              11/28/13    Jeanémart Jérôme               20,00        **Invoices to create**
 12/1/13               12/1/13     Vandenmeulenbos Marie-Louise   50,00        **Invoices to create**
 12/4/13               12/4/13     Ärgerlich Erna                 20,00        **Invoices to create**
 12/10/13              12/10/13    Radermacher Edgard             50,00        **Invoices to create**
 12/13/13              12/13/13    Emonts-Gast Erna               20,00        **Invoices to create**
 12/16/13              12/16/13    Laschet Laura                  50,00        **Invoices to create**
 12/19/13              12/19/13    Jacobs Jacqueline              50,00        **Invoices to create**
 **Total (19 rows)**                                              **860,00**
===================== =========== ============================== ============ ========================
<BLANKLINE>


On the API level it defines the :class:`Invoiceable
<lino_cosi.lib.auto.sales.mixins.Invoiceable>` mixin.

It also defines two utility functions :func:`get_invoiceables_for
<lino_cosi.lib.auto.sales.models.get_invoiceables_for>` and
:func:`create_invoice_for
<lino_cosi.lib.auto.sales.models.create_invoice_for>`.

>>> alf = rt.modules.courses.Pupil.objects.get(pk=152)
>>> alf
Pupil #152 (u'Alfons Radermacher')

>>> for inv in rt.modules.sales.get_invoiceables_for(alf):
...     print(inv)
WWW (1/11/14 Computer room) / Alfons Radermacher


Lino Voga uses this functionality by extending :class:`Enrolment
<lino_cosi.lib.courses.models.Enrolment>` so that it inherits from
:class:`Invoiceable <lino_cosi.lib.auto.sales.mixins.Invoiceable>`. In
Lino Voga, enrolments are the things for which they write invoices.

Another invoiceable thing in Lino Voga is when they rent a room to a
third-party organisation. This is called a :class:`Booking
<lino_voga.lib.rooms.models.Booking>`.

>>> rt.models_by_base(rt.modules.sales.Invoiceable)
[<class 'lino_voga.projects.roger.lib.courses.models.Enrolment'>, <class 'lino_voga.lib.rooms.models.Booking'>]

Invoicings
==========

The detail window of an enrolment shows all invoicings of that
enrolment:

>>> obj = courses.Enrolment.objects.get(pk=83)
>>> rt.show('sales.InvoicingsByInvoiceable', obj)  #doctest: +REPORT_UDIFF
+--------------------+----------+-----------------------------+-------------------------+------------+-----------------+
| Invoice            | Quantity | Heading                     | Description             | Unit price | Total incl. VAT |
+====================+==========+=============================+=========================+============+=================+
| SLS#68             | 1        | WWW (1/11/14 Computer room) | Ihre Einschreibung 50€. |            | 50,00           |
|                    |          |                             | Angefragt 10/11/13.     |            |                 |
+--------------------+----------+-----------------------------+-------------------------+------------+-----------------+
| **Total (1 rows)** | **1**    |                             |                         |            | **50,00**       |
+--------------------+----------+-----------------------------+-------------------------+------------+-----------------+
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


