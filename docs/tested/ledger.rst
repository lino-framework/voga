.. _faggio.tested.ledger:

Ledger
=======

.. include:: /include/tested.rst

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
==================== =============================== ============ ====================================== ========
 Reference            Designation                     Trade Type   Account                                dc
-------------------- ------------------------------- ------------ -------------------------------------- --------
 SLS                  Sales invoices                  Sales                                               Credit
 PRC                  Purchase invoices               Purchases                                           Debit
 BNK                  Bestbank                        Purchases    (bestbank) Bestbank                    Debit
 PMO                  Payment Orders                  Purchases    (bestbankpo) Payment Orders Bestbank   Debit
 CSH                  Cash                                         (cash) Cash                            Debit
 MSG                  Miscellaneous Journal Entries                (cash) Cash                            Debit
 **Total (6 rows)**                                                                                       **5**
==================== =============================== ============ ====================================== ========
<BLANKLINE>
