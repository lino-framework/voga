.. _voga.specs.sales:

Sales
=====

.. to test only this doc:

    $ python setup.py test -s tests.DocsTests.test_sales

    doctest init:

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *
    

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

>>> rt.show('sales.InvoicesToCreate')
No data to display


On the API level it defines the :class:`Invoiceable
<lino_cosi.lib.auto.sales.mixins.Invoiceable>` mixin.

It also defines two utility functions :func:`get_invoiceables_for
<lino_cosi.lib.auto.sales.models.get_invoiceables_for>` and
:func:`create_invoice_for
<lino_cosi.lib.auto.sales.models.create_invoice_for>`.

Lino Voga uses this functionality by extending :class:`Enrolment
<lino_cosi.lib.courses.models.Enrolment>` so that it inherits from
:class:`Invoiceable <lino_cosi.lib.auto.sales.mixins.Invoiceable>`. In
Lino Voga, enrolments are the things for which they write invoices.

An important new challenge appeared when I was in Belgium: they
recently started to have a new invoicing method which they name
"Abo-Kurse" ("Subscription courses"). :ticket:`766` is to implement a
first proof of concept. A subscription course does not end and start
at a given date, the course itself is continously being
given. Participants can start on any time of the year. They usually
pay for 12 sessions in advance (the first invoice for that enrolment),
and Lino must write a new invoice every 12 weeks.
