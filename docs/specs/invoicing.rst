.. _voga.specs.invoicing:

How Lino Voga generates invoices
================================

.. to test only this doc:

    $ python setup.py test -s tests.DocsTests.test_sales

    doctest init:

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.shell import *
    >>> #from lino.api.doctest import *
    

The general functionality for automatically generating invoices is
defined in :mod:`lino_cosi.lib.invoicing`.

On the user-visible level this plugin adds an action of type
:class:`StartInvoicingBase
<lino_cosi.lib.invoicing.actions.StartInvoicingBase>` (with a basket
as icon, referring to a shopping basket) to every *partner* and to
every *invoices journal*.

>>> rt.modules.contacts.Partner.start_invoicing
<StartInvoicingForPartner start_invoicing (u'Create invoices')>
>>> print(rt.modules.contacts.Partner.start_invoicing.icon_name)
basket

The demo database contains exactly one plan:

>>> obj = rt.modules.invoicing.Plan.objects.all()[0]

>>> rt.show('invoicing.ItemsByPlan', obj)  #doctest: +REPORT_UDIFF
========== ============================== ======== ============== =========
 Selected   Partner                        Number   Amount         Invoice
---------- ------------------------------ -------- -------------- ---------
 Yes        Östges Otto                    1        50,00          SLS#58
 Yes        Radermacher Hedi               1        20,00          SLS#59
 Yes        Radermacher Christian          1        50,00          SLS#60
 Yes        Meier Marie-Louise             1        50,00          SLS#61
 Yes        Kaivers Karl                   1        20,00          SLS#62
 Yes        Hilgers Hildegard              1        50,00          SLS#63
 Yes        Engels Edgar                   1        20,00          SLS#64
 Yes        Charlier Ulrike                1        80,00          SLS#65
 Yes        Arens Annette                  1        20,00          SLS#66
 Yes        Lahm Lisa                      1        80,00
 Yes        Dupont Jean                    1        50,00
 Yes        di Rupo Didier                 1        50,00
 Yes        Radermacher Guido              1        80,00
 Yes        Radermacher Alfons             1        50,00
 Yes        Leffin Josefine                1        20,00
 Yes        Jonas Josef                    1        80,00
 Yes        Groteclaes Gregory             1        50,00
 Yes        Emonts Daniel                  1        80,00
 Yes        Demeulenaere Dorothée          1        50,00
 Yes        Bastiaensen Laurent            1        50,00
 Yes        Jeanémart Jérôme               1        20,00
 Yes        Vandenmeulenbos Marie-Louise   1        50,00
 Yes        Ärgerlich Erna                 1        20,00
 Yes        Radermacher Edgard             1        50,00
 Yes        Emonts-Gast Erna               1        20,00
 Yes        Laschet Laura                  1        50,00
 Yes        Jacobs Jacqueline              1        50,00
 Yes        Faymonville Luc                1        20,00
 Yes        Evers Eberhart                 1        50,00
 Yes        Dericum Daniel                 1        20,00
 **30**                                    **30**   **1 350,00**
========== ============================== ======== ============== =========
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
[<class 'lino_voga.projects.roger.lib.courses.models.Enrolment'>, <class 'lino_voga.lib.rooms.models.Booking'>]

Invoicings
==========

The detail window of an enrolment shows all invoicings of that
enrolment:

>>> obj = courses.Enrolment.objects.get(pk=83)
>>> rt.show('invoicing.InvoicingsByInvoiceable', obj)  #doctest: +REPORT_UDIFF
+--------------------+----------+-----------------------------+-------------------------+------------+-----------------+
| Invoice            | Quantity | Heading                     | Description             | Unit price | Total incl. VAT |
+====================+==========+=============================+=========================+============+=================+
| SLS#63             | 1        | WWW (1/11/14 Computer room) | Ihre Einschreibung 50€. |            | 50,00           |
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


