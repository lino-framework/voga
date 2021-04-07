# -*- coding: UTF-8 -*-
# Copyright 2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""In Voga we have only one invoicing area because at least
:ref:`voga.specs.invoicing` relies on it when it inspects the invoicing plan.

"""
#from lino_xl.lib.invoicing.fixtures.demo import *

from lino.api import dd, rt, _


def DEP(name, **kwargs):
    kwargs = dd.str2kw('designation', name, **kwargs)
    # kwargs.update(designation=name)
    return rt.models.invoicing.Area(**kwargs)


def objects():
    yield DEP(_("First"))
    # yield DEP(_("Second"))
    # yield DEP(_("Third"))

