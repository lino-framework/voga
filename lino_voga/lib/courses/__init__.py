# Copyright 2013-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Extends :mod:`lino_cosi.lib.courses` for :ref:`voga`.

.. autosummary::
   :toctree:

    models
    fixtures.demo

"""


from lino_cosi.lib.courses import Plugin


class Plugin(Plugin):

    teacher_model = 'courses.Teacher'
    pupil_model = 'courses.Pupil'
    extends_models = []

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.Pupils')
        m.add_action('courses.Teachers')
        m.add_separator()
        m.add_action('courses.Topics')
        m.add_action('courses.Lines')
        m.add_action('courses.Courses')
        m.add_separator()
        m.add_action('courses.PendingRequestedEnrolments')
        m.add_action('courses.PendingConfirmedEnrolments')

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.TeacherTypes')
        m.add_action('courses.PupilTypes')
        m.add_action('courses.Slots')
