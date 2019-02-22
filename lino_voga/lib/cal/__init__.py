# -*- coding: UTF-8 -*-
# Copyright 2013-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Extends :mod:`lino_xl.lib.cal` for :ref:`voga`.

.. autosummary::
   :toctree:

    models
    fixtures.std
    fixtures.demo2

"""


from lino_xl.lib.cal import Plugin


class Plugin(Plugin):

    extends_models = ['Event', 'Room']
