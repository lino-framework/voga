# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino-Faggio project.
## Lino-Faggio is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-Faggio is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.


from lino.utils.instantiator import Instantiator, i2d
from django.utils.translation import ugettext_lazy as _


from django.conf import settings
from north.dbutils import babelkw
from lino  import dd

courses = dd.resolve_app('courses')

def objects():
  
    yield courses.PupilType(**babelkw('name',de="LFV"))
    yield courses.PupilType(**babelkw('name',de="COK"))
    yield courses.PupilType(**babelkw('name',de="Buche"))
    yield courses.PupilType(**babelkw('name',de="Gast"))
    
    yield courses.TeacherType(**babelkw('name',de="Selbstständig"))
    yield courses.TeacherType(**babelkw('name',de="Ehrenamtlich pauschal"))
    yield courses.TeacherType(**babelkw('name',de="Ehrenamtlich real"))
    yield courses.TeacherType(**babelkw('name',de="LBA"))
    yield courses.TeacherType(**babelkw('name',de="Sonstige"))
    
    mailType = Instantiator('notes.NoteType').build
    
    yield mailType(**babelkw('name',
        en="Enrolment",
        fr=u'Inscription',de=u"Einschreibeformular"))
    yield mailType(**babelkw('name',
        en="Timetable",
        fr=u'Horaire',de=u"Stundenplan"))
    yield mailType(**babelkw('name',
        en="Letter",
        fr=u'Lettre',de=u"Brief"))
