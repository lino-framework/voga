.. _voga.specs.ledger:

Ledger
=======

.. how to test just this document:

    $ python setup.py test -s tests.DocsTests.test_ledger

    doctest init:

    >>> from lino.api.shell import *
    >>> from lino.api import dd
    >>> from django.test.client import Client
    >>> from django.utils.translation import get_language
    >>> from django.utils import translation
    >>> import json

Journals
--------

>>> ses = settings.SITE.login('robin')
>>> ses.show(ledger.Journals,column_names="ref name trade_type account dc")
=========== =============================== ============ ====================================== ===========================
 Reference   Designation                     Trade type   Account                                Primary booking direction
----------- ------------------------------- ------------ -------------------------------------- ---------------------------
 SLS         Sales invoices                  Sales                                               Debit
 PRC         Purchase invoices               Purchases                                           Credit
 PMO         Payment Orders                  Purchases    (bestbankpo) Payment Orders Bestbank   Credit
 CSH         Cash                                         (cash) Cash                            Debit
 BNK         Bestbank                                     (bestbank) Bestbank                    Debit
 MSC         Miscellaneous Journal Entries                (cash) Cash                            Debit
=========== =============================== ============ ====================================== ===========================
<BLANKLINE>


>>> rt.show(accounts.Accounts)
================ ========================= ==========================
 Reference        Designation               Account Group
---------------- ------------------------- --------------------------
 bestbank         Bestbank                  Banks
 bestbankpo       Payment Orders Bestbank   Running transactions
 cash             Cash                      Banks
 customers        Customers                 Commercial receivable(?)
 goods            Purchase of goods         Expenses
 investments      Purchase of investments   Expenses
 membership_fee   Membership fee            Revenues
 services         Purchase of services      Expenses
 suppliers        Suppliers                 Commercial receivable(?)
 vat_deductible   VAT deductible            VAT to pay
 vat_due          VAT due                   VAT to pay
 vatdcl           VAT to declare            Running transactions
================ ========================= ==========================
<BLANKLINE>
