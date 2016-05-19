.. _voga.specs.checkdata:

==========================
Checking for data problems
==========================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_checkdata

    >>> from lino import startup
    >>> startup('lino_voga.projects.docs.settings.doctests')
    >>> from lino.api.doctest import *
    

>>> from django.core.management import call_command
>>> call_command('checkdata', list=True)
================================= ===============================================
 value                             text
--------------------------------- -----------------------------------------------
 printing.CachedPrintableChecker   Check for missing target files
 countries.PlaceChecker            Check plausibility of geographical places.
 beid.BeIdCardHolderChecker        Check for invalid SSINs
 sepa.BankAccountChecker           Check for partner mismatches in bank accounts
 cal.EventGuestChecker             Check for missing participants
 cal.ConflictingEventsChecker      Check for conflicting events
================================= ===============================================
<BLANKLINE>


>>> call_command('checkdata')
Running 3 plausibility checkers on 340 Events...
No plausibility problems found in Events.
Running 1 plausibility checkers on 0 Excerpts...
No plausibility problems found in Excerpts.
Running 1 plausibility checkers on 100 Notes...
No plausibility problems found in Notes.
Running 1 plausibility checkers on 78 Places...
No plausibility problems found in Places.
Running 1 plausibility checkers on 69 Persons...
No plausibility problems found in Persons.
Running 1 plausibility checkers on 0 Payment Order items...
No plausibility problems found in Payment Order items.

>>> call_command('checkdata', 'cal.')
Running 2 plausibility checkers on 340 Events...
No plausibility problems found in Events.

>>> call_command('checkdata', 'foo')
Traceback (most recent call last):
...
CommandError: No checker matches ('foo',)
