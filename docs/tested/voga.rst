.. _voga.tested.voga:

Voga
=======

..
  To run only this test::

  $ python setup.py test -s tests.DocsTests.test_voga

.. include:: /include/tested.rst

>>> from django.conf import settings
>>> from lino.api.shell import *
>>> from django.test.client import Client
>>> from django.utils.translation import get_language
>>> from django.utils import translation
>>> import json

>>> print(settings.SETTINGS_MODULE)
lino_voga.projects.docs.settings.doctests
>>> print([lng.name for lng in settings.SITE.languages])
['en']


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
>>> url = '/api/cal/MyEvents?start=0&limit=16&fmt=json&pv=%s&pv=%s&pv=&pv=&pv=&pv=&pv=&pv=&pv=' % (d,d)
>>> res = client.get(url, REMOTE_USER='robin')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result.keys())
[u'count', u'rows', u'success', u'no_data_text', u'title', u'param_values']


Printable documents
-------------------

We take a sales invoice, clear the cache, ask Lino to print it and 
check whether we get the expected response.

>>> ses = settings.SITE.login("robin")
>>> translation.activate('en')
>>> obj = sales.VatProductInvoice.objects.get(pk=1)
>>> obj.clear_cache()
>>> rv = ses.run(obj.do_print) 
>>> print(rv['success']) 
True
>>> print(rv['open_url']) #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
/media/userdocs/appyodt/sales.VatProductInvoice-1.odt
>>> print(rv['message']) #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Your printable document (filename sales.VatProductInvoice-1.odt)
should now open in a new browser window. If it doesn't, please consult
<a href="http://www.lino-framework.org/help/print.html"
target="_blank">the documentation</a> or ask your system
administrator.

Same for a calendar Event.  This is mainly to see whether the
templates directory has been inherited.  Note that the first few dozen
events have no `user` and would currently fail to print

>>> obj = cal.Event.objects.get(pk=100)
>>> obj.clear_cache()
>>> rv = ses.run(obj.do_print)
>>> print(rv['success'])
True
>>> print(rv['message']) #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Your printable document (filename cal.Event-100.odt) should now open
in a new browser window. If it doesn't, please consult <a
href="http://www.lino-framework.org/help/print.html"
target="_blank">the documentation</a> or ask your system
administrator.

Note that this test should fail if you run the test suite without a 
LibreOffice server running.


