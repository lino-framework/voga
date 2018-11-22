# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Rumma & Ko Ltd
# This file is part of Lino Voga.
#
# Lino Voga is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Voga is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Voga.  If not, see
# <http://www.gnu.org/licenses/>.

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
