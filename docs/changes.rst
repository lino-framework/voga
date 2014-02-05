.. _faggio.changes: 

========================
Changes in Lino-Faggio
========================

See the author's :ref:`Developer Blog <blog>`
to get detailed news.
The final truth about what's going on is only 
`The Source Code <http://code.google.com/p/lino-faggio/source/list>`_.


Version 0.0.2 (in development)
==============================

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


Version 0.0.1 (released :blogref:`20131210`)
============================================

This is a first prototype.
