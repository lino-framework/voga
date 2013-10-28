.. _faggio.tested.faggio:

Faggio
=======

.. include:: /include/tested.rst

>>> from django.conf import settings
>>> from lino.runtime import *
>>> from lino import dd
>>> from django.test.client import Client
>>> import json


A web request
-------------

The following snippet reproduces a one-day bug 
discovered 2013-06-04 
in :func:`lino.modlib.cal.utils.when_text` 
on calendar events whose **time** fields are empty.

>>> client = Client()
>>> d = settings.SITE.demo_date().replace(month=12,day=25)
>>> d = d.strftime(settings.SITE.date_format_strftime)
>>> print(d)
25.12.2013
>>> url = '/api/cal/MyEvents?start=0&limit=16&fmt=json&pv=%s&pv=%s&pv=&pv=&pv=&pv=&pv=&pv=' % (d,d)
>>> res = client.get(url,REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result.keys())
[u'count', u'rows', u'success', u'no_data_text', u'title', u'param_values']
>>> print(len(result['rows']))
2
>>> print(result['rows'][0][0])
<a href="javascript:Lino.cal.OneEvent.detail.run(null,{ &quot;record_id&quot;: 40 })">2013 Dez. 25 (Mi.)</a>



Printing an invoice
-------------------

We take a sales invoice, clear the cache, ask Lino to print it and 
check whether we get the expected response.

>>> ses = settings.SITE.login("robin")
>>> obj = sales.Invoice.objects.get(pk=1)
>>> obj.clear_cache()
>>> print(ses.run(obj.do_print)) #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
{'refresh': True, 'open_url': u'/media/cache/appypdf/sales.Invoice-1.pdf', 'message': u'S#1 printable has been built.', 'success': True}
 
Note that this test should fail if you run the test suite without a 
LibreOffice server running.


Basic truths of accounting
--------------------------

- A purchases invoice creditates the partner.
- A sales invoice debitates the partner.
- The payment of a purchases invoice debitates  the partner.
- The payment of a sales invoice creditates the partner.

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

