.. _faggio.changes: 

========================
Changes in Lino-Faggio
========================

See the author's :ref:`Developer Blog <blog>`
to get detailed news.
The final truth about what's going on is only 
`The Source Code <http://code.google.com/p/lino-faggio/source/list>`_.


Version 0.0.3 (not yet released)
============================================

- Beim Generieren von Terminen (Eingabe der Kurse) waren noch einige
  Bugs im Algoritmus selber sowie der Berichterstattung (d.h. er
  Rückmeldung an den Benutzer).

- Den Blitz-Button müsst ihr auch jetzt noch klicken, damit er die
  Termine neu berechnet.

- Um den Termin "ausfallen zu lasssen", d.h. das Datum auf die Woche
  danach zu verlegen, kannst du jetzt rechten Mausklick machen und im
  Kontextmenü "Move down" wählen.

- Das Datum eines Termins (in der Liste der Termine pro Kurs) ist
  jetzt anklickbar und führt zu einer Tabelle mit allen Terminen an
  diesem Tag.  Schien mir praktisch.

- Bei Konflikten meldet er jetzt ein bisschen deutlicher, welche
  Termine sich beissen.



Version 0.0.2 (released :blogref:`20140206`)
============================================

- Termine kann man jetzt "Zurücksetzen" (nützlich z.B. wenn man
  versehentlich auf "Stattgefunden" geklickt hatte).

- Wenn man eine Angabe im Detail-Fenster eines Kurses änderte
  (z.B. Uhrzeit oder Anzahl Plätze) und dann auf "Registriert"
  klickte, ohne vorher gespeichert zu haben, dann gingen diese
  Änderungen verloren. Jetzt nicht mehr. Wenn man jetzt im
  Arbeitsablauf klickt, dann wird automatisch gespeichert.

- Die Bezeichnungen der Aktionen im Arbeitsablauf eines Kurses sind
  jetzt "Entwurf" statt "Zurücksetzen" und "Storniert" statt
  "Stornieren" (d.h. man sieht exakt den Namen des Zustands, in den
  der Kurs durch Klick versetzt werden soll)

- Wenn man den Zustand eines Kurses (Arbeitsablauf) ändert, dann wird
  jetzt automatisch der "Blitz" ausgeführt.

  N.B. Wenn man eine Stunde verschiebt, dann muss man auch jetzt noch
  selber auf den Blitz klicken, um die anderen Termine
  anzupassen. (Denn wenn ich das auch dort immer automatisch nach
  jeder Änderung aufriefe, könnte das möglicherweise irritierende oder
  lästige Auswirkungen haben. à suivre.)

- Bei Auswahl Kursleiter steht jetzt nicht mehr die Kursleiterart in
  Klammern hinter dem Namen.
- Kursserie einfügen: auch Felder "Thema" und "Kursleiter"
- Neue Partner (Kursleiter, Schüler, Organisationen, sonstige) haben
  jetzt par défaut "Belgien" als Land (genauer gesagt das Land des
  Site-Besitzers (:ddref:`system.SiteConfig.site_company`)




Version 0.0.1 (released :blogref:`20131210`)
============================================

This is a first prototype.
