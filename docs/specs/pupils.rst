.. _voga.specs.pupils:

==================================
Managing participants in Lino Voga
==================================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_pupils

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *
    


Displaying all pupils who are either Member or Non-Member (using
gridfilter):


>>> from django.utils.http import urlquote
>>> url = '/api/courses/Pupils?'
>>> url += 'limit=10&start=0&fmt=json&'
>>> # url += "rp=ext-comp-1213&"
>>> # url += "pv=&pv=&pv=&pv=&pv=&pv=&pv=&"
>>> url += "filter=" + urlquote('[{"type":"string","value":"mem","field":"pupil_type"}]')
>>> res = test_client.get(url, REMOTE_USER='robin')
>>> print(res.status_code)
200

The response to this AJAX request is in JSON:

>>> d = json.loads(res.content)
>>> d['count']
24


