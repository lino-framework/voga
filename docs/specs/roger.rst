.. _voga.specs.roger:

=================================
Specific for Lino Voga à la Roger
=================================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_roger

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
(membership_fee) Membership fee

>>> rt.show(ledger.MovementsByAccount, acc)
============ ========= ===================================== ============ ======== ============= =========
 Value date   Voucher   Description                           Debit        Credit   Match         Cleared
------------ --------- ------------------------------------- ------------ -------- ------------- ---------
 22/12/2015   *CSH 5*   *Faymonville Luc*                     15,00                 **CSH 5:1**   Yes
 22/12/2015   *CSH 5*   *Groteclaes Gregory*                  15,00                 **CSH 5:2**   Yes
 22/12/2015   *CSH 5*   *Hilgers Hildegard*                   15,00                 **CSH 5:3**   Yes
 22/12/2015   *CSH 5*   *Jacobs Jacqueline*                   15,00                 **CSH 5:4**   Yes
 22/12/2015   *CSH 5*   *Jonas Josef*                         15,00                 **CSH 5:5**   Yes
 22/11/2015   *CSH 4*   *Dobbelstein-Demeulenaere Dorothée*   15,00                 **CSH 4:1**   Yes
 22/11/2015   *CSH 4*   *Evers Eberhart*                      15,00                 **CSH 4:2**   Yes
 22/11/2015   *CSH 4*   *Emonts Daniel*                       15,00                 **CSH 4:3**   Yes
 22/11/2015   *CSH 4*   *Engels Edgar*                        15,00                 **CSH 4:4**   Yes
 22/10/2015   *CSH 3*   *Dericum Daniel*                      15,00                 **CSH 3:1**   Yes
 22/10/2015   *CSH 3*   *Demeulenaere Dorothée*               15,00                 **CSH 3:2**   Yes
 22/02/2015   *CSH 2*   *Charlier Ulrike*                     15,00                 **CSH 2:1**   Yes
 22/01/2015   *CSH 1*   *Arens Annette*                       15,00                 **CSH 1:1**   Yes
 22/01/2015   *CSH 1*   *Altenberg Hans*                      15,00                 **CSH 1:2**   Yes
 22/01/2015   *CSH 1*   *Bastiaensen Laurent*                 15,00                 **CSH 1:3**   Yes
                        **Balance 225.00 (15 movements)**     **225,00**
============ ========= ===================================== ============ ======== ============= =========
<BLANKLINE>



Menu walk
=========

Here is the output of :func:`walk_menu_items
<lino.api.doctests.walk_menu_items>` for this database:

>>> walk_menu_items('rolf')
... #doctest: -ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte --> Personen : 73
- Kontakte --> Organisationen : 30
- Kontakte --> Partnerlisten : 9
- Büro --> Meine Datenkontrollliste : 0
- Büro --> Meine Benachrichtigungen : 2
- Büro --> Meine Notizen : 34
- Büro --> Meine Uploads : 1
- Büro --> Mein E-Mail-Ausgang : 1
- Büro --> Meine Auszüge : 0
- Kalender --> Meine Termine : 58
- Kalender --> Überfällige Termine : 29
- Kalender --> Unbestätigte Termine : 3
- Kalender --> Meine Aufgaben : 1
- Kalender --> Meine Gäste : 1
- Kalender --> Meine Anwesenheiten : 1
- Kalender --> Meine überfälligen Termine : 5
- Kalender --> Buchungen : 4
- Buchhaltung --> Verkauf --> Verkaufsrechnungen (SLS) : 0
- Buchhaltung --> Verkauf --> Gutschriften Verkauf (SLC) : 0
- Buchhaltung --> Einkauf --> Einkaufsrechnungen (PRC) : 0
- Buchhaltung --> Finanzjournale --> Zahlungsaufträge (PMO) : 0
- Buchhaltung --> Finanzjournale --> Kasse (CSH) : 0
- Buchhaltung --> Finanzjournale --> Bestbank (BNK) : 0
- Buchhaltung --> Finanzjournale --> Diverse Buchungen (MSC) : 0
- Aktivitäten --> Teilnehmer : 36
- Aktivitäten --> Kursleiter : 10
- Aktivitäten --> Kurse : 24
- Aktivitäten --> Ausfahrten : 1
- Aktivitäten --> Reisen : 3
- Aktivitäten --> Themen : 6
- Aktivitäten --> Aktivitätenreihen : 11
- Aktivitäten --> Offene Einschreibungsanfragen : 10
- Aktivitäten --> Auszustellende Teilnahmebescheinigungen : 69
- Berichte --> Buchhaltung --> Schuldner : 0
- Berichte --> Buchhaltung --> Gläubiger : 14
- Berichte --> MwSt. --> Offene Rechnungen : 18
- Konfigurierung --> System --> Benutzer : 7
- Konfigurierung --> System --> Hilfetexte : 3
- Konfigurierung --> Orte --> Länder : 9
- Konfigurierung --> Orte --> Orte : 79
- Konfigurierung --> Kontakte --> Organisationsarten : 17
- Konfigurierung --> Kontakte --> Funktionen : 6
- Konfigurierung --> Kontakte --> Listenarten : 4
- Konfigurierung --> Kalender --> Kalenderliste : 9
- Konfigurierung --> Kalender --> Räume : 8
- Konfigurierung --> Kalender --> Prioritäten : 5
- Konfigurierung --> Kalender --> Regelmäßige Ereignisse : 17
- Konfigurierung --> Kalender --> Gastrollen : 4
- Konfigurierung --> Kalender --> Kalendereintragsarten : 9
- Konfigurierung --> Kalender --> Wiederholungsregeln : 7
- Konfigurierung --> Kalender --> Externe Kalender : 1
- Konfigurierung --> Tarife --> Tarife : 12
- Konfigurierung --> Tarife --> Tarifkategorien : 6
- Konfigurierung --> Buchhaltung --> Kontengruppen : 8
- Konfigurierung --> Buchhaltung --> Konten : 14
- Konfigurierung --> Buchhaltung --> Journale : 8
- Konfigurierung --> Buchhaltung --> Buchungsperioden : 18
- Konfigurierung --> Buchhaltung --> Zahlungsbedingungen : 9
- Konfigurierung --> MwSt. --> MwSt-Regeln : 12
- Konfigurierung --> MwSt. --> Papierarten : 3
- Konfigurierung --> Aktivitäten --> Aktivitätsarten : 1
- Konfigurierung --> Aktivitäten --> Kursleiterarten : 5
- Konfigurierung --> Aktivitäten --> Teilnehmerarten : 4
- Konfigurierung --> Aktivitäten --> Timetable Slots : 1
- Konfigurierung --> Büro --> Notizarten : 4
- Konfigurierung --> Büro --> Ereignisarten : 2
- Konfigurierung --> Büro --> Upload-Arten : 1
- Konfigurierung --> Büro --> Auszugsarten : 12
- Explorer --> System --> Vollmachten : 1
- Explorer --> System --> Benutzerarten : 5
- Explorer --> System --> Datenbankmodelle : 79
- Explorer --> System --> Datentests : 10
- Explorer --> System --> Datenprobleme : 15
- Explorer --> System --> Benachrichtigungen : 7
- Explorer --> System --> Änderungen : 0
- Explorer --> Kontakte --> Kontaktpersonen : 1
- Explorer --> Kontakte --> Partner : 102
- Explorer --> Kontakte --> Listenmitgliedschaften : 1
- Explorer --> Kalender --> Kalendereinträge : 714
- Explorer --> Kalender --> Aufgaben : 1
- Explorer --> Kalender --> Anwesenheiten : 1
- Explorer --> Kalender --> Abonnements : 36
- Explorer --> Kalender --> Termin-Zustände : 4
- Explorer --> Kalender --> Gast-Zustände : 4
- Explorer --> Kalender --> Aufgaben-Zustände : 5
- Explorer --> Buchhaltung --> Ausgleichungsregeln : 12
- Explorer --> Buchhaltung --> Belege : 205
- Explorer --> Buchhaltung --> Belegarten : 5
- Explorer --> Buchhaltung --> Bewegungen : 697
- Explorer --> Buchhaltung --> Geschäftsjahre : 7
- Explorer --> Buchhaltung --> Handelsarten : 4
- Explorer --> Buchhaltung --> Journalgruppen : 4
- Explorer --> MwSt. --> MwSt.-Regimes : 9
- Explorer --> MwSt. --> MwSt.-Klassen : 3
- Explorer --> MwSt. --> Produktrechnungen : 84
- Explorer --> MwSt. --> Produktrechnungszeilen : 102
- Explorer --> MwSt. --> Fakturationspläne : 2
- Explorer --> Aktivitäten --> Aktivitäten : 26
- Explorer --> Aktivitäten --> Einschreibungen : 78
- Explorer --> Aktivitäten --> Einschreibungs-Zustände : 4
- Explorer --> Finanzjournale --> Kontoauszüge : 22
- Explorer --> Finanzjournale --> Diverse Buchungen : 1
- Explorer --> Finanzjournale --> Zahlungsaufträge : 17
- Explorer --> SEPA --> Bankkonten : 18
- Explorer --> Büro --> Notizen : 101
- Explorer --> Büro --> Uploads : 1
- Explorer --> Büro --> Upload-Bereiche : 1
- Explorer --> Büro --> E-Mail-Ausgänge : 1
- Explorer --> Büro --> Anhänge : 1
- Explorer --> Büro --> Auszüge : 0
<BLANKLINE>
