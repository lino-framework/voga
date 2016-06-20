.. _voga.specs.ledger:

Ledger
=======

.. how to test just this document:

    $ python setup.py test -s tests.DocsTests.test_ledger

    doctest init:

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *

Journals
--------

>>> ses = settings.SITE.login('robin')
>>> ses.show(ledger.Journals, column_names="ref name trade_type account dc")
=========== =============================== ==================== ===================== ============ ================================ ===========================
 Reference   Designation                     Designation (de)     Designation (fr)      Trade type   Account                          Primary booking direction
----------- ------------------------------- -------------------- --------------------- ------------ -------------------------------- ---------------------------
 SLS         Sales invoices                  Verkaufsrechnungen   Factures vente        Sales                                         Debit
 SLC         Sales credit notes              Sales credit notes   Sales credit notes    Sales                                         Credit
 PRC         Purchase invoices               Einkaufsrechnungen   Factures achat        Purchases                                     Credit
 PMO         Payment Orders                  Zahlungsaufträge     Payment Orders        Purchases    (5810) Payment Orders Bestbank   Credit
 CSH         Cash                            Kasse                Caisse                             (5700) Cash                      Debit
 BNK         Bestbank                        Bestbank             Bestbank                           (5500) Bestbank                  Debit
 MSC         Miscellaneous Journal Entries   Diverse Buchungen    Opérations diverses                (5700) Cash                      Debit
=========== =============================== ==================== ===================== ============ ================================ ===========================
<BLANKLINE>


>>> rt.show(accounts.Accounts)
================ ========================= =========================== ============================= ==========================
 Reference        Designation               Designation (de)            Designation (fr)              Account Group
---------------- ------------------------- --------------------------- ----------------------------- --------------------------
 4000             Customers                 Kunden                      Clients                       Commercial receivable(?)
 4400             Suppliers                 Lieferanten                 Fournisseurs                  Commercial receivable(?)
 4510             VAT due                   Geschuldete MWSt            TVA due                       VAT to pay
 4512             VAT deductible            Abziehbare MWSt             TVA déductible                VAT to pay
 4513             VAT to declare            MWSt zu deklarieren         TVA à declarer                Running transactions
 5500             Bestbank                  Bestbank                    Bestbank                      Banks
 5700             Cash                      Kasse                       Caisse                        Banks
 5810             Payment Orders Bestbank   Zahlungsaufträge Bestbank   Ordres de paiement Bestbank   Running transactions
 6010             Purchase of services      Dienstleistungen            Services et biens divers      Expenses
 6020             Purchase of investments   Anlagen                     Investissements               Expenses
 6040             Purchase of goods         Wareneinkäufe               Achat de marchandise          Expenses
 7310             Membership fee            Mitgliedsbeitrag            Cotisation                    Revenues
 membership_fee   Membership fee            Mitgliedsbeitrag            Membership fee
================ ========================= =========================== ============================= ==========================
<BLANKLINE>

