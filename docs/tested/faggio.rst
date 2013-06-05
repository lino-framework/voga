.. _faggio.tested.faggio:

Faggio
=======

.. include:: /include/tested.rst

The following statement imports a set of often-used global names::

>>> from lino.runtime import *
>>> from lino import dd
>>> from pprint import pprint
>>> from django.test.client import Client
>>> import json

We can now refer to every installed app via it's `app_label`.
For example here is how we can verify here that the demo database 
has 23 pupils and 7 teachers:

>>> school.Pupil.objects.count()
35
>>> school.Teacher.objects.count()
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
>>> url = '/api/cal/MyEvents?fmt=json&limit=15&start=0&pv=%s&pv=%s&pv=&pv=&pv=&pv=false' % (d,d)
>>> res = client.get(url,REMOTE_USER='rolf')
>>> pprint(res.status_code)
200
>>> result = json.loads(res.content)
>>> pprint(result.keys())
[u'count', u'rows', u'success', u'no_data_text', u'title', u'param_values']
>>> pprint(len(result['rows']))
2
>>> pprint(result['rows'][0][0])
u'2013 Dez 25 (Mi.)'

