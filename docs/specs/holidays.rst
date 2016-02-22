.. _voga.specs.holidays:

=================
Defining holidays
=================

.. How to test just this document

   $ python setup.py test -s tests.DocsTests.test_holidays

See also :ref:`xl.specs.holidays`.

..  Some initialization:

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.demo')
    >>> from lino.api.doctest import *
    >>> settings.SITE.verbose_client_info_message = True
    >>> from lino.api import rt, _
    >>> from atelier.utils import i2d
    >>> RecurrentEvent = cal.RecurrentEvent
    >>> Recurrencies = cal.Recurrencies


Recurrent event rules
=====================

Here are the default holidays defined as recurrent event rules
:class:`RecurrentEvent <lino.modlib.cal.models.RecurrentEvent>` by
:mod:`lino.modlib.cal.fixtures.std`:

>>> rt.show(cal.RecurrentEvents)
============ ========== ============================ ==================== =================================== ==================== =====================
 Start date   End Date   Designation                  Designation (de)     Designation (fr)                    Recurrency           Calendar Event Type
------------ ---------- ---------------------------- -------------------- ----------------------------------- -------------------- ---------------------
 1/1/13                  New Year's Day               Neujahr              Jour de l'an                        yearly               Holidays
 2/11/13                 Rosenmontag                  Rosenmontag          Rosenmontag                         Relative to Easter   Holidays
 2/13/13                 Ash Wednesday                Ash Wednesday        Ash Wednesday                       Relative to Easter   Holidays
 3/29/13                 Good Friday                  Good Friday          Good Friday                         Relative to Easter   Holidays
 3/31/13                 Easter sunday                Easter sunday        Easter sunday                       Relative to Easter   Holidays
 4/1/13                  Easter monday                Easter monday        Easter monday                       Relative to Easter   Holidays
 5/1/13                  International Workers' Day   Tag der Arbeit       Premier Mai                         yearly               Holidays
 5/9/13                  Ascension of Jesus           Ascension of Jesus   Ascension of Jesus                  Relative to Easter   Holidays
 5/20/13                 Pentecost                    Pentecost            Pentecost                           Relative to Easter   Holidays
 7/1/13       8/31/13    Summer holidays              Sommerferien         Vacances d'été                      yearly               Holidays
 7/21/13                 National Day                 Nationalfeiertag     Fête nationale                      yearly               Holidays
 8/15/13                 Assumption of Mary           Mariä Himmelfahrt    Assomption de Marie                 yearly               Holidays
 10/31/13                All Souls' Day               Allerseelen          Commémoration des fidèles défunts   yearly               Holidays
 11/1/13                 All Saints' Day              Allerheiligen        Toussaint                           yearly               Holidays
 11/11/13                Armistice with Germany       Waffenstillstand     Armistice                           yearly               Holidays
 12/25/13                Christmas                    Weihnachten          Noël                                yearly               Holidays
============ ========== ============================ ==================== =================================== ==================== =====================
<BLANKLINE>


