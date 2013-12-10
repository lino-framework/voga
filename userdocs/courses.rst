.. _faggio.courses:

=======
Courses
=======

Benutzerfragen
==============

"In den Terminen eines Kurses habe ich versehentlich einen Termin 
auf "Stattgefunden" gesetzt. 
Wie kann ich ihn wieder auf "Entwurf" setzen?"

- Ins Detail des Termins gehen, den Reiter "Mehr" aktivieren, 
  Feld "Zustand" manuell auf "Vorgeschlagen" setzen, Speichern.
- Oder (wenn mehrere Termine zu korrigieren sind): Kolonne "Zustand"
  sichtbar machen und (mit :kbd:`F2`) direkt in der Tabelle bearbeiten.

"Wie kann ich ihn wieder auf "Vorschlag" setzen?""

- Manuell geht das nicht, weil "Vorschlag" bedeutet, dass 
  der Termin noch nicht manuell bearbeitet wurden.
  Um jegliche manuelle Änderung zu vergessen, löschen Sie den 
  Termin einfach und lassen den Kurs dann seine Termine neu generieren.





Reference
=========

.. actor:: courses.Pupil
.. actor:: courses.Teacher
.. actor:: courses.Line

    A line (of :ddref:`courses.Course`) is a series which groups
    courses into a configurable list of categories. 
    The default database has  the following list of Course Lines:
  
    .. django2rst:: settings.SITE.login('robin').show(courses.Lines)
  
  
.. actor:: courses.Course

    Notes about automatic event generation:
    
    - When an automatically generated event is to be reported to another
      date, e.g. because it falls into a vacation period,
      then you simply change it's date. 
      Lino will automatically adapt all subsequent events.
      
    - Marking an automatically generated event as "Cancelled" will not
      create a replacement event.




.. actor:: courses.Topic
.. actor:: courses.Enrolment
.. actor:: courses.Slot
.. actor:: courses.PupilType
.. actor:: courses.TeacherType
