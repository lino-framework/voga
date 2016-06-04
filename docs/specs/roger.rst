.. _voga.specs.roger:

=================================
Specific for Lino Voga à la Roger
=================================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_roger

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *

In :mod:`lino_voga.projects.roger` they have the following rules about
"membership":

- Members get a discount on enrolments, nothing else
- Customers can freely decide whether they want to be members or not.
  They become member by paying the membership fee.
- They have a field :attr:`member_until
  <lino_voga.projects.roger.lib.courses.models.Pupil.member_until>`

There is a custom plausibility checker
:class:`lino_voga.projects.roger.lib.courses.models.MemberChecker`
    
    
>>> dd.demo_date()
datetime.date(2014, 5, 22)

>>> rt.show(courses.Pupils)
======================================== ================================= ================== ============ ===== ===== ======== ==============
 Name                                     Address                           Participant Type   Section      LFV   CKK   Raviva   Mitglied bis
---------------------------------------- --------------------------------- ------------------ ------------ ----- ----- -------- --------------
 Hans Altenberg (MEC)                     Aachener Straße, 4700 Eupen                                       No    Yes   No       31/12/2014
 Annette Arens (ME)                       Alter Malmedyer Weg, 4700 Eupen                                   No    No    No       31/12/2014
 Laurent Bastiaensen (MES)                Am Berg, 4700 Eupen                                  Eupen        No    No    No       31/12/2014
 Bernd Brecht (MS)                        Germany                                              Nidrum       No    No    No
 Ulrike Charlier (ME)                     Auenweg, 4700 Eupen                                               No    No    No       31/12/2014
 Dorothée Demeulenaere (ME)               Auf'm Rain, 4700 Eupen                                            No    No    No       31/12/2015
 Daniel Dericum (MECLS)                   August-Thonnar-Str., 4700 Eupen                      Nidrum       Yes   Yes   No       31/12/2015
 Dorothée Dobbelstein-Demeulenaere (ME)   Bahnhofstraße, 4700 Eupen                                         No    No    No       31/12/2015
 Jean Dupont (ML)                         4031 Angleur                                                      Yes   No    No
 Daniel Emonts (ME)                       Bellmerin, 4700 Eupen                                             No    No    No       31/12/2015
 Erna Emonts-Gast (ME)                    4730 Raeren                                                       No    No    No       31/12/2014
 Edgar Engels (MES)                       Bennetsborn, 4700 Eupen                              Walhorn      No    No    No       31/12/2015
 Eberhart Evers (MEC)                     Bergstraße, 4700 Eupen                                            No    Yes   No       31/12/2015
 Luc Faymonville (ME)                     Brabantstraße, 4700 Eupen                                         No    No    No       31/12/2015
 Gregory Groteclaes (ME)                  Edelstraße, 4700 Eupen                                            No    No    No       31/12/2015
 Hildegard Hilgers (MECS)                 Favrunpark, 4700 Eupen                               Herresbach   No    Yes   No       31/12/2015
 Jacqueline Jacobs (MES)                  Fränzel, 4700 Eupen                                  Eynatten     No    No    No       31/12/2015
 Jérôme Jeanémart (MCLS)                  France                                               Walhorn      Yes   Yes   No
 Josef Jonas (MEC)                        Gülcherstraße, 4700 Eupen                                         No    Yes   No       31/12/2015
 Karl Kaivers (MLS)                       Haasberg, 4700 Eupen                                 Kelmis       Yes   No    No
 Lisa Lahm (MEL)                          Germany                                                           Yes   No    No       31/12/2014
 Laura Laschet (ME)                       Habsburgerweg, 4700 Eupen                                         No    No    No       31/12/2014
 Josefine Leffin (MCS)                    Heidgasse, 4700 Eupen                                Hergenrath   No    Yes   No
 Mark Martelaer (ME)                      Amsterdam, Netherlands                                            No    No    No       31/12/2014
 Marie-Louise Meier (MS)                  Hisselsgasse, 4700 Eupen                             Hauset       No    No    No
 Alfons Radermacher (MS)                  4730 Raeren                                          Elsenborn    No    No    No
 Christian Radermacher (ME)               4730 Raeren                                                       No    No    No       31/12/2014
 Edgard Radermacher (MCS)                 4730 Raeren                                          Weywertz     No    Yes   No
 Guido Radermacher (ME)                   4730 Raeren                                                       No    No    No       31/12/2014
 Hedi Radermacher (MLS)                   4730 Raeren                                          Sonstige     Yes   No    No
 Jean Radermacher (MEC)                   4730 Raeren                                                       No    Yes   No       31/12/2014
 Marie-Louise Vandenmeulenbos (ME)        Amsterdam, Netherlands                                            No    No    No       31/12/2014
 Didier di Rupo (ME)                      4730 Raeren                                                       No    No    No       31/12/2014
 Erna Ärgerlich (MCS)                     4730 Raeren                                          Eupen        No    Yes   No
 Otto Östges (ME)                         4730 Raeren                                                       No    No    No       31/12/2014
======================================== ================================= ================== ============ ===== ===== ======== ==============
<BLANKLINE>


>>> rt.show(plausibility.Checkers)
================================= ===============================================
 value                             text
--------------------------------- -----------------------------------------------
 printing.CachedPrintableChecker   Check for missing target files
 countries.PlaceChecker            Check plausibility of geographical places.
 beid.BeIdCardHolderChecker        Check for invalid SSINs
 sepa.BankAccountChecker           Check for partner mismatches in bank accounts
 ledger.VoucherChecker             Check integrity of ledger movements
 cal.EventGuestChecker             Check for missing participants
 cal.ConflictingEventsChecker      Check for conflicting events
 courses.MemberChecker             Check membership payments
================================= ===============================================
<BLANKLINE>

>>> print(dd.plugins.ledger.force_cleared_until)
None

>>> rt.show(plausibility.ProblemsByChecker, 'courses.MemberChecker')
============= ===================================== ==========================================
 Responsible   Controlled by                         Message
------------- ------------------------------------- ------------------------------------------
 Robin Rood    *Laura Laschet (ME)*                  Member until 2014-12-31, but no payment.
 Robin Rood    *Erna Emonts-Gast (ME)*               Member until 2014-12-31, but no payment.
 Robin Rood    *Christian Radermacher (ME)*          Member until 2014-12-31, but no payment.
 Robin Rood    *Guido Radermacher (ME)*              Member until 2014-12-31, but no payment.
 Robin Rood    *Jean Radermacher (MEC)*              Member until 2014-12-31, but no payment.
 Robin Rood    *Didier di Rupo (ME)*                 Member until 2014-12-31, but no payment.
 Robin Rood    *Otto Östges (ME)*                    Member until 2014-12-31, but no payment.
 Robin Rood    *Mark Martelaer (ME)*                 Member until 2014-12-31, but no payment.
 Robin Rood    *Marie-Louise Vandenmeulenbos (ME)*   Member until 2014-12-31, but no payment.
 Robin Rood    *Lisa Lahm (MEL)*                     Member until 2014-12-31, but no payment.
============= ===================================== ==========================================
<BLANKLINE>

>>> acc = rt.models.accounts.Account.get_by_ref(dd.plugins.courses.membership_fee_account)
>>> print(acc)
(membership_fee) Membership fee

>>> rt.show(ledger.MovementsByAccount, acc)
============ ========= ===================================== ============ ======== ============= =========
 Value date   Voucher   Description                           Debit        Credit   Match         Cleared
------------ --------- ------------------------------------- ------------ -------- ------------- ---------
 22/12/2014   *CSH 5*   *Faymonville Luc*                     15,00                 **CSH 5:1**   Yes
 22/12/2014   *CSH 5*   *Groteclaes Gregory*                  15,00                 **CSH 5:2**   Yes
 22/12/2014   *CSH 5*   *Hilgers Hildegard*                   15,00                 **CSH 5:3**   Yes
 22/12/2014   *CSH 5*   *Jacobs Jacqueline*                   15,00                 **CSH 5:4**   Yes
 22/12/2014   *CSH 5*   *Jonas Josef*                         15,00                 **CSH 5:5**   Yes
 22/11/2014   *CSH 4*   *Dobbelstein-Demeulenaere Dorothée*   15,00                 **CSH 4:1**   Yes
 22/11/2014   *CSH 4*   *Evers Eberhart*                      15,00                 **CSH 4:2**   Yes
 22/11/2014   *CSH 4*   *Emonts Daniel*                       15,00                 **CSH 4:3**   Yes
 22/11/2014   *CSH 4*   *Engels Edgar*                        15,00                 **CSH 4:4**   Yes
 22/10/2014   *CSH 3*   *Dericum Daniel*                      15,00                 **CSH 3:1**   Yes
 22/10/2014   *CSH 3*   *Demeulenaere Dorothée*               15,00                 **CSH 3:2**   Yes
 22/02/2014   *CSH 2*   *Charlier Ulrike*                     15,00                 **CSH 2:1**   Yes
 22/01/2014   *CSH 1*   *Arens Annette*                       15,00                 **CSH 1:1**   Yes
 22/01/2014   *CSH 1*   *Altenberg Hans*                      15,00                 **CSH 1:2**   Yes
 22/01/2014   *CSH 1*   *Bastiaensen Laurent*                 15,00                 **CSH 1:3**   Yes
                        **Balance 225.00 (15 movements)**     **225,00**
============ ========= ===================================== ============ ======== ============= =========
<BLANKLINE>
