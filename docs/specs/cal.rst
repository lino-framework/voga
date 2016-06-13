.. _voga.tested.cal:

========
Calendar
========

.. to test only this document:

  $ python setup.py test -s tests.DocsTests.test_cal

.. doctest initialization:

   >>> from lino import startup
   >>> startup('lino_voga.projects.docs.settings.demo')
   >>> from lino.api.doctest import *

This document describes how :ref:`voga` extends the default calendar
functions.


See also :ref:`book.specs.cal`.

Workflow
========

The following workflows are defined in
:mod:`lino_voga.lib.cal.workflows`.

>>> rt.show(cal.EventStates)
======= ============ ============ ======== =================== ======== ============= =========
 value   name         text         Symbol   Edit participants   Stable   Transparent   No auto
------- ------------ ------------ -------- ------------------- -------- ------------- ---------
 10      suggested    Suggested    ?        Yes                 No       No            No
 20      draft        Draft        ☐        Yes                 No       No            No
 50      took_place   Took place   ☑        Yes                 Yes      No            No
 70      cancelled    Cancelled    ☉        No                  Yes      Yes           Yes
 75      omitted      Omitted      ☒        No                  Yes      Yes           No
======= ============ ============ ======== =================== ======== ============= =========
<BLANKLINE>

>>> rt.show(cal.GuestStates)
======= ========= ============ ========= ========
 value   name      Afterwards   text      Symbol
------- --------- ------------ --------- --------
 10      invited   No           Invited   ☐
 40      present   Yes          Present   ☑
 50      absent    Yes          Absent    ☉
 60      excused   No           Excused   ⚕
======= ========= ============ ========= ========
<BLANKLINE>


Rooms
=====

The following rooms are defined in the
:mod:`lino_voga.lib.voga.fixtures.buche` demo fixture.


>>> ses = rt.login('robin')
>>> ses.show(cal.Rooms)  #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS +REPORT_NDIFF
================== ================== =================== ============================= ============
 Designation        Calendar           Tariff              Company                       City
------------------ ------------------ ------------------- ----------------------------- ------------
 Mirrored room      Mirrored room      Spiegelraum Eupen   Lern- und Begegnungszentrum   Eupen
 Computer room      Computer room      Rent per meeting    Lern- und Begegnungszentrum   Eupen
 Conferences room   Conferences room                       Lern- und Begegnungszentrum   Butgenbach
 Computer room      Computer room                          Lern- und Begegnungszentrum   Butgenbach
 Computer room      Computer room                          Zur Klüüs                     Kelmis
 Computer room      Computer room                          Sport- und Freizeitzentrum    Sankt Vith
 Outside            Outside
================== ================== =================== ============================= ============
<BLANKLINE>

(The last room, because it has no company, caused a bug which was fixed on
:blogref:`20140920`)
