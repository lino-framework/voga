# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.modlib.courses import Plugin


class Plugin(Plugin):

    teacher_model = 'courses.Teacher'
    pupil_model = 'courses.Pupil'
