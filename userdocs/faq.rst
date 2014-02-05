================================
FAQ (Frequently Asked Questions)
================================

.. contents:: 
   :local:
   :depth: 1

.. _faq.timefield:

Wie kann ich Uhrzeiten per Tastatur eingeben?
---------------------------------------------

In allen Uhrzeit-Feldern kann man auch per Tastatur eingeben.
Wichtig ist, die Eingabe nicht mit ENTER zu beenden,
sondern mit der TAB-Taste oder durch Klick in ein anderes Eingabefeld.

======= ========
Eingabe Resultat
------- --------
825     08:25
030     00:30
2350    23:50
======= ========


.. _faq.weekday:

Was ist der Unterschied zwischen "Pro Wochentag" und "Wöchentlich"?
-------------------------------------------------------------------

Die häufigste Wiederholungsmethode bei Kursen ist "Pro Wochentag".
Nur dann sind die darunterstehenden Ankreuzfelder aktiviert, mit denen
Sie einen oder mehrere Wochentage eingeben können. Das Datum des
ersten Termins entspricht dann nicht unbedingt dem Beginndatum des
Kurses, sondern Lino nimmt den ersten passenden Wochentag **ab**
diesem Datum.

Alle anderen Methoden bedeuten, dass das Beginndatum den Wochentag
bestimmt.

.. _faq.menu:

Nach welcher Logik ist das Hauptmenü strukturiert?
--------------------------------------------------

Zur Struktur des Menüs: 

- Alle Benutzer haben eigentlich das gleiche Menü, aber die einzelnen
  Untermenüs "wachsen" oder "schrumpfen" je nach den Zugriffsrechten.
  
- Wir unterscheiden **drei Arten von Menü-Titeln**.
  Zunächst haben wir pro "funktionaler Gruppe" jeweils einen Titel
  mit "täglichen" Befehlen: 

  - :menuselection:`Kontakte`,
    :menuselection:`Kurse`, :menuselection:`Kalender`,
    :menuselection:`Produkte` usw.
    
- Darauf folgen drei besondere Titel ":menuselection:`Berichte`"
  ":menuselection:`Konfigurierung`" und
  ":menuselection:`Explorer`" weniger alltäglichen Befehlen: 
    
  - :menuselection:`Berichte` enthält auswertende oder
    zusammenfassende Ansichten.
      
  - :menuselection:`Konfigurierung` enthält Befehle zur Konfigurierung 
    des Gesamtsystems.
      
  - :menuselection:`Explorer` zeigt Gesamtansichten gewisser
    Tabellen, die theoretisch nicht nötig sind, sondern eher "für
    Neugierige" dort sind und in Ausnahmesituationen nützlich sein
    können.
    
  Diese drei Titel sind *jeweils wieder pro funktionaler Gruppe
  unterteilt*.

- Sowie die drei speziellen Titel :menuselection:`Site`,
  :menuselection:`Startseite` und das "Benutzermenü" oben rechts (das
  den Namen des Benutzers anzeigt).


Wieso überspringt Lino das Datum X beim Generieren meiner Termine?
------------------------------------------------------------------

Mögliche Gründe:

- Ist das Datum ein Feiertag?
  (:menuselection:`Konfigurierung --> Kalender --> Feiertage`)

- Findet an dem Tag ein anderer Termin im gleichen Raum statt?

Falls das noch nicht hilft, können Sie (mit Firefox oder Chromium) die
Javascript-Console Ihres Browsers öffnen, auf den Blitz klicken (um
die Aktion nochmals auszuführen) und schauen, was er in die Konsole
schreibt. Dort berichtet Lino, was er sich beim Generieren der Termine
gedacht hat.

.. _faq.delete_event:

Einzelne Termine ausfallen lassen
---------------------------------

Wie kann ich Lino daran hindern, am Karnevalstag einen Termin zu
generieren?  Lino generiert beharrlich einen Termin am 5. März
(Karneval) jedesmal wieder neu, wenn ich ihn lösche.

Löschen reicht nicht, dann generiert er ihn neu. Aber die Idee ist
gut: wenn man einen automatisch generierten Termin löscht, dann sollte
Lino dies als "Stunde fällt aus, ist aber nicht storniert, sondern
wird in der Woche darauf nachgeholt" verstehen und automatisch die
folgenden Termine neu nummerieren.

Momentan musst du:

- in der Tabellenansicht aufs Datumsfeld klicken
- [F2] drücken um zu sagen "Ich will das Feld bearbeiten"
- [Alt+PfeilNachUnten] um den Auswahlkalender aufzuklappen
- [PfeilNachUnten] um auf die Woche danach zu springen
- [Enter] um das neue Datum auszuwählen
- [Enter] oder [Tab] um die Feldbearbeitung zu beenden

Oder noch besser: gehe in `Konfigurierung --> Kalender --> Periodische
Termine` und sage dort, dass Karneval ein Feiertag ist:

- Auf `+` klicken oder Doppelklick auf der leeren untersten Zeile
- Im Feld :ddref:`cal.RecurrentEvents.name` z.B. "Karneval" eingeben
- Im Feld :ddref:`cal.RecurrentEvents.event_type` "Feiertag" auswählen
- [Enter] drücken (oder auf `Erstellen` klicken), um das Dialogfenster zu
  schließen. Lino zeigt nun die neu erstellte Terminvorlage im Detail.
- Im Feld :ddref:`cal.RecurrentEvents.every_unit` "once" auswählen.
  (eine Regel "40 Tage vor Ostern" hat Lino noch nicht, deshalb müssen
  Ostern und Karneval jedes Jahr manuell erstellt werden)
- Auf den Blitz klicken, um den eigentlichen Termin zu generieren.


