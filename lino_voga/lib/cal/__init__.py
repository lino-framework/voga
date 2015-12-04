# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Extends :mod:`lino.modlib.cal` for :ref:`voga`.

.. autosummary::
   :toctree:

    models
    fixtures.std
    fixtures.demo2

"""


from lino.modlib.cal import Plugin


class Plugin(Plugin):

    extends_models = ['Event', 'Room']
