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
