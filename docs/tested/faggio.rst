.. _faggio.tested.faggio:

Faggio
=======

.. include:: /include/tested.rst

>>> from django.conf import settings
>>> from lino.runtime import *
>>> from lino import dd
>>> from django.test.client import Client
>>> from django.utils.translation import get_language
>>> from django.utils import translation
>>> import json

>>> print(settings.SETTINGS_MODULE)
lino_faggio.settings.test
>>> print([lng.name for lng in settings.SITE.languages])
['en', 'de', 'fr']


A web request
-------------

The following snippet reproduces a one-day bug 
on calendar events whose **time** fields are empty.
Fixed 2013-06-04 
in :func:`lino.modlib.cal.utils.when_text`.

>>> print(get_language())
en
>>> client = Client()
>>> d = settings.SITE.demo_date().replace(month=12,day=25)
>>> d = d.strftime(settings.SITE.date_format_strftime)
>>> print(d)
25.12.2014
>>> url = '/api/cal/MyEvents?start=0&limit=16&fmt=json&pv=%s&pv=%s&pv=&pv=&pv=&pv=&pv=&pv=' % (d,d)
>>> res = client.get(url, REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result.keys())
[u'count', u'rows', u'success', u'no_data_text', u'title', u'param_values']
>>> print(len(result['rows']))
2
>>> print(result['rows'][0][0]) 
... #doctest: +ELLIPSIS
<a href="javascript:Lino.cal.OneEvent.detail.run(null,{ &quot;record_id&quot;: ... })">2014 Dez. 25 (Do.)</a>

Note that the language remains "de" because the web request caused it to
switch to rolf's language:

>>> print(get_language())
de



Printable documents
-------------------

We take a sales invoice, clear the cache, ask Lino to print it and 
check whether we get the expected response.

>>> ses = settings.SITE.login("robin")
>>> translation.activate('en')
>>> obj = sales.Invoice.objects.get(pk=1)
>>> obj.clear_cache()
>>> rv = ses.run(obj.do_print) 
>>> print(rv['success']) 
True
>>> print(rv['open_url']) #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
/media/cache/appypdf/sales.Invoice-1.pdf
>>> print(rv['message']) #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
sales.Invoice-1.pdf has been built.

Same for a calendar Event.  This is mainly to see whether the
templates directory has been inherited.  Note that the first few dozen
events have no `user` and would currently fail to print

>>> obj = cal.Event.objects.get(pk=100)
>>> obj.clear_cache()
>>> rv = ses.run(obj.do_print)
>>> print(rv['success'])
True
>>> print(rv['message'])
cal.Event-100.pdf has been built.

Note that this test should fail if you run the test suite without a 
LibreOffice server running.


