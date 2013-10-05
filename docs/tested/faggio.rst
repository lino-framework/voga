.. _faggio.tested.faggio:

Faggio
=======

.. include:: /include/tested.rst

The following statement imports a set of often-used global names::

>>> from django.conf import settings
>>> from lino.runtime import *
>>> from lino import dd
>>> from pprint import pprint
>>> from django.test.client import Client
>>> import json

We can now refer to every installed app via it's `app_label`.
For example here is how we can verify here that the demo database 
has 23 pupils and 7 teachers:

>>> courses.Pupil.objects.count()
35
>>> courses.Teacher.objects.count()
8

A web request
-------------

The following snippet reproduces a one-day bug 
discovered 2013-06-04 
in :func:`lino.modlib.cal.utils.when_text`:

>>> client = Client()
>>> d = settings.SITE.demo_date().replace(month=12,day=25)
>>> d = d.strftime(settings.SITE.date_format_strftime)
>>> pprint(d)
'25.12.2013'
>>> url = '/api/cal/MyEvents?start=0&limit=16&fmt=json&pv=%s&pv=%s&pv=&pv=&pv=&pv=&pv=&pv=&pv=' % (d,d)
>>> res = client.get(url,REMOTE_USER='rolf')
>>> pprint(res.status_code)
200
>>> result = json.loads(res.content)
>>> pprint(result.keys())
[u'count', u'rows', u'success', u'no_data_text', u'title', u'param_values']
>>> pprint(len(result['rows']))
2
>>> pprint(result['rows'][0][0])
u'<a href="javascript:Lino.cal.OneEvent.detail.run(null,{ &quot;record_id&quot;: 270 })">2013 Dez. 25 (Mi.)</a>'



Printing an invoice
-------------------

>>> ses = settings.SITE.login("robin")
>>> obj = sales.Invoice.objects.get(pk=127)
>>> obj.clear_cache()
>>> pprint(ses.run(obj.do_print)) #doctest: +NORMALIZE_WHITESPACE
{'message': u'S#127 printable has been built.',
 'open_url': u'/media/cache/appypdf/sales.Invoice-127.pdf',
 'refresh': True,
 'success': True}

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
 C                    Cash                                         (cash) Cash                            Debit
 PO                   Payment Orders                               (bestbankpo) Payment Orders Bestbank   Debit
 M                    Miscellaneous Journal Entries                                                       Debit
 **Total (6 rows)**                                                                                       **5**
==================== =============================== ============ ====================================== ========
<BLANKLINE>
