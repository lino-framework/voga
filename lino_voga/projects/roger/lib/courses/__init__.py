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

"""
An extension of :mod:`lino_voga.lib.courses`

.. autosummary::
   :toctree:

    management.commands.eiche2lino
    models

"""

from lino_voga.lib.courses import Plugin


class Plugin(Plugin):
    # see blog 20160409
    extends_models = ['Pupil', 'Course', 'Enrolment', 'Line']
    # extends_models = ['Pupil', 'Course', 'Enrolment']
    # extends_models = ['Pupil', 'Course', 'Line']
