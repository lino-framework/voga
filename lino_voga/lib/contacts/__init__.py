# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Extends :mod:`lino_xl.lib.contacts` for :ref:`voga`.

.. autosummary::
   :toctree:

    models
    management.commands.garble_persons
    fixtures.std
    fixtures.demo

"""


from lino_xl.lib.contacts import Plugin


class Plugin(Plugin):

    extends_models = ['Person']
