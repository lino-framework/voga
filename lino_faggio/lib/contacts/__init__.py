# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Extends :mod:`lino.modlib.contacts` for :ref:`faggio`.

.. autosummary::
   :toctree:

    models
    management.commands.garble_persons
    fixtures.std
    fixtures.demo

"""


from lino.modlib.contacts import Plugin


class Plugin(Plugin):

    extends_models = ['Person']
