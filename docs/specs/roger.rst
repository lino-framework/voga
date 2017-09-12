.. _voga.specs.roger:

=================================
Specific for Lino Voga à la Roger
=================================

..  to test only this doc:

    $ doctest docs/specs/roger.rst

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *


A customized management of membership fees
==========================================

In :mod:`lino_voga.projects.roger` they have the following rules for
handling memberships:

- Membership costs 15€  per year.
- Members get a discount on enrolments to courses.
- Customers can freely decide whether they want to be members or not.
- They become member by paying the membership fee.

To handle these rules, we have an additional field :attr:`member_until
<lino_voga.projects.roger.lib.courses.models.Pupil.member_until>` on
each pupil.

There is a custom plausibility checker
:class:`lino_voga.projects.roger.lib.courses.models.MemberChecker`
    
    
>>> dd.demo_date()
datetime.date(2015, 5, 22)


>>> rt.show(rt.actors.courses.Pupils)
... #doctest: +ELLIPSIS
======================================== ================================= ================== ============ ===== ===== ======== ==============
 Name                                     Address                           Participant Type   Section      LFV   CKK   Raviva   Mitglied bis
---------------------------------------- --------------------------------- ------------------ ------------ ----- ----- -------- --------------
 Hans Altenberg (MEC)                     Aachener Straße, 4700 Eupen       Member                          No    Yes   No       31/12/2015
 Annette Arens (ME)                       Alter Malmedyer Weg, 4700 Eupen   Helper                          No    No    No       31/12/2015
 Laurent Bastiaensen (MES)                Am Berg, 4700 Eupen               Non-member         Eupen        No    No    No       31/12/2015
 Bernd Brecht (MS)                        Germany                           Member             Nidrum       No    No    No
 Ulrike Charlier (ME)                     Auenweg, 4700 Eupen               Helper                          No    No    No       31/12/2015
 Dorothée Demeulenaere (ME)               Auf'm Rain, 4700 Eupen            Non-member                      No    No    No       31/12/2016
 Daniel Dericum (MECLS)                   August-Thonnar-Str., 4700 Eupen   Member             Nidrum       Yes   Yes   No       31/12/2016
...
 Hedi Radermacher (MLS)                   4730 Raeren                       Non-member         Sonstige     Yes   No    No
 Jean Radermacher (MEC)                   4730 Raeren                       Member                          No    Yes   No       31/12/2015
 Marie-Louise Vandenmeulenbos (ME)        Amsterdam, Netherlands            Helper                          No    No    No       31/12/2015
 Didier di Rupo (ME)                      4730 Raeren                       Non-member                      No    No    No       31/12/2015
 Erna Ärgerlich (MCS)                     4730 Raeren                       Member             Eupen        No    Yes   No
 Otto Östges (ME)                         4730 Raeren                       Helper                          No    No    No       31/12/2015
======================================== ================================= ================== ============ ===== ===== ======== ==============
<BLANKLINE>


>>> print(dd.plugins.ledger.force_cleared_until)
None

>>> rt.show(plausibility.ProblemsByChecker, 'courses.MemberChecker')
============= ===================================== ==========================================
 Responsible   Controlled by                         Message
------------- ------------------------------------- ------------------------------------------
 Robin Rood    *Laura Laschet (ME)*                  Member until 2015-12-31, but no payment.
 Robin Rood    *Erna Emonts-Gast (ME)*               Member until 2015-12-31, but no payment.
 Robin Rood    *Christian Radermacher (ME)*          Member until 2015-12-31, but no payment.
 Robin Rood    *Guido Radermacher (ME)*              Member until 2015-12-31, but no payment.
 Robin Rood    *Jean Radermacher (MEC)*              Member until 2015-12-31, but no payment.
 Robin Rood    *Didier di Rupo (ME)*                 Member until 2015-12-31, but no payment.
 Robin Rood    *Otto Östges (ME)*                    Member until 2015-12-31, but no payment.
 Robin Rood    *Mark Martelaer (ME)*                 Member until 2015-12-31, but no payment.
 Robin Rood    *Marie-Louise Vandenmeulenbos (ME)*   Member until 2015-12-31, but no payment.
 Robin Rood    *Lisa Lahm (MEL)*                     Member until 2015-12-31, but no payment.
============= ===================================== ==========================================
<BLANKLINE>

>>> acc = rt.models.accounts.Account.get_by_ref(dd.plugins.courses.membership_fee_account)
>>> print(acc)
(7310) Membership fee

>>> rt.show(ledger.MovementsByAccount, acc)
============ ========= ===================================== ============ ======== =============
 Value date   Voucher   Description                           Debit        Credit   Match
------------ --------- ------------------------------------- ------------ -------- -------------
 22/12/2015   *CSH 5*   *Faymonville Luc*                     15,00                 **CSH 5:1**
 22/12/2015   *CSH 5*   *Groteclaes Gregory*                  15,00                 **CSH 5:2**
 22/12/2015   *CSH 5*   *Hilgers Hildegard*                   15,00                 **CSH 5:3**
 22/12/2015   *CSH 5*   *Jacobs Jacqueline*                   15,00                 **CSH 5:4**
 22/12/2015   *CSH 5*   *Jonas Josef*                         15,00                 **CSH 5:5**
 22/11/2015   *CSH 4*   *Dobbelstein-Demeulenaere Dorothée*   15,00                 **CSH 4:1**
 22/11/2015   *CSH 4*   *Emonts Daniel*                       15,00                 **CSH 4:3**
 22/11/2015   *CSH 4*   *Engels Edgar*                        15,00                 **CSH 4:4**
 22/11/2015   *CSH 4*   *Evers Eberhart*                      15,00                 **CSH 4:2**
 22/10/2015   *CSH 3*   *Demeulenaere Dorothée*               15,00                 **CSH 3:2**
 22/10/2015   *CSH 3*   *Dericum Daniel*                      15,00                 **CSH 3:1**
 22/02/2015   *CSH 2*   *Charlier Ulrike*                     15,00                 **CSH 2:1**
 22/01/2015   *CSH 1*   *Altenberg Hans*                      15,00                 **CSH 1:2**
 22/01/2015   *CSH 1*   *Arens Annette*                       15,00                 **CSH 1:1**
 22/01/2015   *CSH 1*   *Bastiaensen Laurent*                 15,00                 **CSH 1:3**
                        **Balance 225.00 (15 movements)**     **225,00**
============ ========= ===================================== ============ ======== =============
<BLANKLINE>


Menu walk
=========

Here is the output of :func:`walk_menu_items
<lino.api.doctests.walk_menu_items>` for this database:

>>> walk_menu_items('rolf', severe=False)
... #doctest: -ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte --> Personen : 72
- Kontakte --> Organisationen : 29
- Kontakte --> Partnerlisten : 8
- Büro --> Meine Datenkontrollliste : 0
- Büro --> Meine Benachrichtigungen : 2
- Büro --> Meine Notizen : 34
- Büro --> Meine Uploads : 0
- Büro --> Mein E-Mail-Ausgang : 0
- Büro --> Meine Auszüge : 0
- Kalender --> Meine Termine : 57
- Kalender --> Überfällige Termine : 28
- Kalender --> Unbestätigte Termine : 4
- Kalender --> Meine Aufgaben : 1
- Kalender --> Meine Gäste : 1
- Kalender --> Meine Anwesenheiten : 1
- Kalender --> Meine überfälligen Termine : 4
- Kalender --> Buchungen : 3
- Buchhaltung --> Verkauf --> Verkaufsrechnungen (SLS) : 0
- Buchhaltung --> Verkauf --> Gutschriften Verkauf (SLC) : 0
- Buchhaltung --> Einkauf --> Einkaufsrechnungen (PRC) : 0
- Buchhaltung --> Finanzjournale --> Zahlungsaufträge (PMO) : 0
- Buchhaltung --> Finanzjournale --> Kasse (CSH) : 0
- Buchhaltung --> Finanzjournale --> Bestbank (BNK) : 0
- Buchhaltung --> Finanzjournale --> Diverse Buchungen (MSC) : 0
- Aktivitäten --> Teilnehmer : 35
- Aktivitäten --> Kursleiter : 9
- Aktivitäten --> Kurse : 23
- Aktivitäten --> Ausfahrten : 0
- Aktivitäten --> Reisen : 2
- Aktivitäten --> Themen : 6
- Aktivitäten --> Aktivitätenreihen : 10
- Aktivitäten --> Offene Einschreibungsanfragen : 10
- Aktivitäten --> Auszustellende Teilnahmebescheinigungen : 69
- Berichte --> Buchhaltung --> Saldenliste Generalkonten : 10
- Berichte --> Buchhaltung --> Saldenliste Kunden : 20
- Berichte --> Buchhaltung --> Saldenliste Lieferanten : 3
- Berichte --> Buchhaltung --> Schuldner : 0
- Berichte --> Buchhaltung --> Gläubiger : 5
- Berichte --> Buchhaltung --> Purchase journal : 0
- Berichte --> Buchhaltung --> Intra-Community purchases : 85
- Berichte --> Buchhaltung --> Intra-Community sales : 0
- Berichte --> Buchhaltung --> Offene Rechnungen : 2
- Berichte --> Buchhaltung --> Sales invoice journal : 0
- Konfigurierung --> System --> Benutzer : 6
- Konfigurierung --> System --> Hilfetexte : 3
- Konfigurierung --> Orte --> Länder : 8
- Konfigurierung --> Orte --> Orte : 79
- Konfigurierung --> Kontakte --> Organisationsarten : 17
- Konfigurierung --> Kontakte --> Funktionen : 6
- Konfigurierung --> Kontakte --> Listenarten : 4
- Konfigurierung --> Kalender --> Kalenderliste : 8
- Konfigurierung --> Kalender --> Räume : 7
- Konfigurierung --> Kalender --> Prioritäten : 5
- Konfigurierung --> Kalender --> Regelmäßige Ereignisse : 16
- Konfigurierung --> Kalender --> Gastrollen : 4
- Konfigurierung --> Kalender --> Kalendereintragsarten : 8
- Konfigurierung --> Kalender --> Wiederholungsregeln : 7
- Konfigurierung --> Kalender --> Externe Kalender : 1
- Konfigurierung --> Tarife --> Tarife : 11
- Konfigurierung --> Tarife --> Tarifkategorien : 6
- Konfigurierung --> Buchhaltung --> Kontengruppen : 7
- Konfigurierung --> Buchhaltung --> Konten : 15
- Konfigurierung --> Buchhaltung --> Journale : 7
- Konfigurierung --> Buchhaltung --> Buchungsperioden : 18
- Konfigurierung --> Buchhaltung --> Zahlungsbedingungen : 9
- Konfigurierung --> MwSt. --> MwSt-Regeln : 7
- Konfigurierung --> MwSt. --> Papierarten : 3
- Konfigurierung --> Aktivitäten --> Aktivitätsarten : 1
- Konfigurierung --> Aktivitäten --> Kursleiterarten : 5
- Konfigurierung --> Aktivitäten --> Teilnehmerarten : 4
- Konfigurierung --> Aktivitäten --> Timetable Slots : 0
- Konfigurierung --> Büro --> Notizarten : 3
- Konfigurierung --> Büro --> Ereignisarten : 2
- Konfigurierung --> Büro --> Upload-Arten : 0
- Konfigurierung --> Büro --> Auszugsarten : 11
- Explorer --> System --> Vollmachten : 1
- Explorer --> System --> Benutzerarten : 5
- Explorer --> System --> Datenbankmodelle : 79
- Explorer --> System --> Datentests : 10
- Explorer --> System --> Datenprobleme : 15
- Explorer --> System --> Benachrichtigungen : 7
- Explorer --> System --> Änderungen : 0
- Explorer --> Kontakte --> Kontaktpersonen : 1
- Explorer --> Kontakte --> Partner : 101
- Explorer --> Kontakte --> Listenmitgliedschaften : 1
- Explorer --> Kalender --> Kalendereinträge : 713
- Explorer --> Kalender --> Aufgaben : 1
- Explorer --> Kalender --> Anwesenheiten : 1
- Explorer --> Kalender --> Abonnements : 36
- Explorer --> Kalender --> Termin-Zustände : 4
- Explorer --> Kalender --> Gast-Zustände : 4
- Explorer --> Kalender --> Aufgaben-Zustände : 5
- Explorer --> Buchhaltung --> Begleichungsregeln : 12
- Explorer --> Buchhaltung --> Belege : 205
- Explorer --> Buchhaltung --> Belegarten : 5
- Explorer --> Buchhaltung --> Bewegungen : 627
- Explorer --> Buchhaltung --> Geschäftsjahre : 7
- Explorer --> Buchhaltung --> Handelsarten : 5
- Explorer --> Buchhaltung --> Journalgruppen : 5
- Explorer --> MwSt. --> MwSt.-Regimes : 3
- Explorer --> MwSt. --> MwSt.-Klassen : 3
- Explorer --> MwSt. --> VAT columns : 0
- Explorer --> MwSt. --> Rechnungen : 85
- Explorer --> MwSt. --> Produktrechnungen : 83
- Explorer --> MwSt. --> Produktrechnungszeilen : 102
- Explorer --> MwSt. --> Fakturationspläne : 2
- Explorer --> Aktivitäten --> Aktivitäten : 25
- Explorer --> Aktivitäten --> Einschreibungen : 78
- Explorer --> Aktivitäten --> Einschreibungs-Zustände : 4
- Explorer --> Finanzjournale --> Kontoauszüge : 21
- Explorer --> Finanzjournale --> Diverse Buchungen : 0
- Explorer --> Finanzjournale --> Zahlungsaufträge : 16
- Explorer --> SEPA --> Bankkonten : 19
- Explorer --> Büro --> Notizen : 101
- Explorer --> Büro --> Uploads : 0
- Explorer --> Büro --> Upload-Bereiche : 1
- Explorer --> Büro --> E-Mail-Ausgänge : 0
- Explorer --> Büro --> Anhänge : 1
- Explorer --> Büro --> Auszüge : 0
<BLANKLINE>

