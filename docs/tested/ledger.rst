.. _faggio.tested.ledger:

Ledger
=======

.. include:: /include/tested.rst

>>> from lino.runtime import *
>>> from lino import dd
>>> from django.test.client import Client
>>> from django.utils.translation import get_language
>>> from django.utils import translation
>>> import json

Journals
--------

>>> ses.show(ledger.Journals,column_names="ref name trade_type account dc")
==================== =============================== ============ ====================================== ========
 ref                  Designation                     Trade Type   Account                                dc
-------------------- ------------------------------- ------------ -------------------------------------- --------
 S                    Sales invoices                  Sales                                               Credit
 P                    Purchase invoices               Purchases                                           Debit
 B                    Bestbank                                     (bestbank) Bestbank                    Debit
 PO                   Payment Orders                  Purchases    (bestbankpo) Payment Orders Bestbank   Debit
 C                    Cash                                         (cash) Cash                            Debit
 M                    Miscellaneous Journal Entries                                                       Debit
 **Total (6 rows)**                                                                                       **5**
==================== =============================== ============ ====================================== ========
<BLANKLINE>

