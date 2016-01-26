.. _voga.specs.holidays:

=================
Defining holidays
=================

.. How to test just this document

   $ python setup.py test -s tests.DocsTests.test_holidays

Some initialization:

>>> from lino import startup
>>> startup('lino_voga.projects.roger.settings.demo')
>>> from lino.api.doctest import *
>>> settings.SITE.verbose_client_info_message = True
>>> from lino.api import rt, _
>>> from atelier.utils import i2d
>>> RecurrentEvent = cal.RecurrentEvent
>>> Recurrencies = cal.Recurrencies


Here are the standard holidays, defined by
:mod:`lino.modlib.cal.fixtures.std`::

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


Let's look at one of them, Ash Wednesday::

>>> ash_wednesday = RecurrentEvent.objects.get(**dd.str2kw('name', _("Ash Wednesday")))

The :mod:`lino.modlib.cal.fixtures.std` fixture generates
automatically all Ash Wednesday in a given range of years:

>>> rt.show(cal.EventsByController, master_instance=ash_wednesday)
============= =============== ===============
 When          Summary         Workflow
------------- --------------- ---------------
 Wed 2/13/13   Ash Wednesday   **Suggested**
 Wed 3/5/14    Ash Wednesday   **Suggested**
 Wed 2/18/15   Ash Wednesday   **Suggested**
 Wed 2/10/16   Ash Wednesday   **Suggested**
 Wed 3/1/17    Ash Wednesday   **Suggested**
 Wed 2/14/18   Ash Wednesday   **Suggested**
 Wed 3/6/19    Ash Wednesday   **Suggested**
============= =============== ===============
<BLANKLINE>

That given range of years depends on some configuration variables:

- :attr:`ignore_dates_before <lino.core.site.Site.ignore_dates_before>`
- :attr:`ignore_dates_after <lino.core.site.Site.ignore_dates_after>`
- :attr:`lino.modlib.system.SiteConfig.max_auto_events`


.. verify that no events have actually been saved:
   >>> cal.Event.objects.count()
   368

We can add our own local custom holidays which depend on easter.

We create one recurrent event for it and specify `Recurrencies.easter`
as recurrency:

>>> holidays = cal.EventType.objects.get(**dd.str2kw('name', _("Holidays")))
>>> obj = RecurrentEvent(name="Karneval in Kettenis",
...     every_unit=Recurrencies.easter,
...     start_date=i2d(20160209), event_type=holidays)
>>> obj.full_clean()
>>> obj.find_start_date(i2d(20160209))
datetime.date(2016, 2, 9)

>>> ar = rt.login()
>>> wanted = obj.get_wanted_auto_events(ar)
>>> len(wanted)
4
>>> print(ar.response['info_message'])
Generating events between 2016-02-09 and 2019-05-22.
Reached upper date limit 2019-05-22

>>> wanted[1]
Event(owner_type=20,start_date=2016-02-09,summary='Karneval in Kettenis',auto_type=1,event_type=1,state=<EventStates.suggested:10>)

.. verify that no events have actually been saved:
   >>> cal.Event.objects.count()
   368
