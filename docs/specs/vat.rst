.. _voga.specs.vat:

============================
VAT declaration in Lino Voga
============================

..  to test only this doc:

    $ doctest docs/specs/vat.rst

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *


Test cases
==========

The following covers a bug that was was fixed :blogref:`20170905`


>>> rt.show(vat.IntracomSales)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
No data to display

>>> #rt.show(vat.IntracomPurchases)

>>> url = "/api/vat/IntracomPurchases?fmt=json&rp=ext-comp-1224&limit=17&start=0"
>>> # test_client.get(url)
>>> json_fields = 'count rows title success no_data_text param_values'
>>> kwargs = dict(fmt='json', limit=5, start=0)
>>> demo_get('robin', "api/vat/IntracomPurchases", json_fields, 85, **kwargs)
