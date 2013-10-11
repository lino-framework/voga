.. _faggio.cal:

========
Calendar
========

Important models are 
:ddref:`cal.Event`
and
:ddref:`cal.Guest`
and
:ddref:`cal.Task`...

.. contents:: 
   :local:
   :depth: 2

Anonymous calendar events
-------------------------

A calendar event with an empty :ddref:`cal.Event.user`
field is called "anonymous" or "public".


Site parameters
---------------


:ddref:`system.SiteConfig.max_auto_events`

farest_future 
default_calendar 
holiday_calendar

.. actor:: cal.CalendarPanel



.. actor:: cal.Event

    Possible values for the state of an :ddref: `cal.Event`:

    .. django2rst:: 

        settings.SITE.login('robin').show(cal.EventStates)


.. actor:: cal.Guest

    Possible values for the state of a :ddref: `cal.Guest`:

    .. django2rst:: 

        settings.SITE.login('robin').show(cal.GuestStates)

.. actor:: cal.Task

    Possible values for the state of a :ddref: `cal.Task`:

    .. django2rst:: 

        settings.SITE.login('robin').show(cal.TaskStates)

.. actor:: cal.Calendar
.. actor:: cal.Subscription
.. actor:: cal.Room
.. actor:: cal.Priority
.. actor:: cal.GuestRole


