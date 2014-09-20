.. _faggio.courses:

=======
Courses
=======


Anleitung zum Erstellen von Kursserien
======================================

- Menü :menuselection:`Konfiguration --> Kurse --> Kursserien`

- Icon "+": Neuen Datensatz erstellen

- Bezeichnung: Kurstitel eingeben (Bsp. "Ubuntu 14.04 leicht gemacht")

- Im Feld :ddref:`courses.Line.every_unit` kommt die
  Wiederholungsmethode zu stehen, die Lino für alle neuen Kurse 
  dieser Serie als Standard vorschlagen soll.

  Die häufigste Methode ist "Pro Wochentag".
  Siehe auch :ref:`faq.weekday`.

- Schaltfläche "Erstellen" klicken. Lino öffnet ein neues Fenster

- Teilnahmegebühr: Produkt auswählen

- Ereignisart: Kurse

- Icon "Speichern"

- Beginnt am: Doppelklick auf leerem Feld

- Startdatum eingeben: Beginnt am tt.mm.jjjj

- Kursleiter auswählen

- Schaltfläche "Erstellen" klicken.

Neues Fenster

- Uhrzeiten eingeben: Beginn-Ende (Dropdown-Menü)
  Siehe auch :ref:`faq.timefield`.

- Kursleiter auswählen

- Entweder in :ddref:`courses.Course.max_events` die Anzahl der
  Termine oder in :ddref:`courses.Course.max_date` ein Enddatum
  eingeben.  Wenn Sie beide Felder ausfüllen, werden nur Termine
  generiert bis zur ersten Grenze.

-  Wochentag auswählen

- Icon "Änderungen in diesem Datensatz speichern"

- Schaltfläche "Registriert" klicken

- Icon "Blitz" (Termine generierenaktualisieren) klicken

- Vorgeschlagene Termine überprüfen


Benutzerfragen
==============

"In den Terminen eines Kurses habe ich versehentlich einen Termin auf
"Stattgefunden" gesetzt.  Wie kann ich ihn wieder auf "Entwurf"
setzen?"

- Ab Version 0.0.2 erübrigt sich die Frage.

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
  
    .. django2rst:: rt.login('robin').show(courses.Lines)
  
  
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
