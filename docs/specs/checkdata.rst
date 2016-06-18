.. _voga.specs.checkdata:

=======================================
Checking for data problems in Lino Voga
=======================================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_checkdata

    >>> from lino import startup
    >>> startup('lino_voga.projects.edmund.settings.doctests')
    >>> from lino.api.doctest import *


Lino Voga offers some functionality for managing plausibility
problems.

See also :ref:`book.specs.checkdata`.

Data checkers available in Lino Voga
====================================

In the web interface you can select :menuselection:`Explorer -->
System --> Plausibility checkers` to see a table of all available
checkers.

.. 
    >>> show_menu_path(plausibility.Checkers)
    Explorer --> System --> Plausibility checkers
    

>>> rt.show(plausibility.Checkers)
================================= ===============================================
 value                             text
--------------------------------- -----------------------------------------------
 printing.CachedPrintableChecker   Check for missing target files
 countries.PlaceChecker            Check plausibility of geographical places.
 beid.BeIdCardHolderChecker        Check for invalid SSINs
 sepa.BankAccountChecker           Check for partner mismatches in bank accounts
 ledger.VoucherChecker             Check integrity of ledger movements
 cal.EventGuestChecker             Check for missing participants
 cal.ConflictingEventsChecker      Check for conflicting events
================================= ===============================================
<BLANKLINE>


Showing all problems
====================

In the web interface you can select :menuselection:`Explorer -->
System --> Plausibility problems` to see them.

..
    >>> show_menu_path(plausibility.AllProblems)
    Explorer --> System --> Plausibility problems


>>> rt.show(plausibility.AllProblems)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
No data to display
