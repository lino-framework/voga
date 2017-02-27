# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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

"""The :ref:`voga` extension of :mod:`lino_xl.lib.invoicing`.

This adds a new field :attr:`course
<lino_voga.lib.invoicing.models.Plan.course>` to the invoicing plan
and a "basket" button to the Course model.

.. autosummary::
   :toctree:

    models
    fixtures.demo_bookings


"""

from lino_xl.lib.invoicing import Plugin, _


class Plugin(Plugin):

    extends_models = ['Plan']

