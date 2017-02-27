# Copyright 2013-2016 Luc Saffre
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

"""Extends :mod:`lino_xl.lib.courses` for :ref:`voga`.

.. autosummary::
   :toctree:

    models
    desktop
    fixtures.demo

"""


from lino_xl.lib.courses import Plugin
from lino.api import _


class Plugin(Plugin):

    # verbose_name = _("Activities")

    teacher_model = 'courses.Teacher'
    """The name of the model to be used for "teachers" (i.e. the person
    who is responsible for a course).

    """
    pupil_model = 'courses.Pupil'
    """The name of the model to be used for "pupils" (i.e. the persons who
    participate in a course).

    """
    extends_models = ['Enrolment', 'Course', 'Line']
    needs_plugins = [
        'lino_xl.lib.cal', 'lino_xl.lib.invoicing', 'lino_xl.lib.sales']
    # needs_plugins = ['lino_xl.lib.cal', 'lino_cosi.lib.auto.sales']

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.Pupils')
        m.add_action('courses.Teachers')
        m.add_separator()
        for ca in site.models.courses.CourseAreas.objects():
            m.add_action(ca.courses_table)
        # m.add_action('courses.Courses')
        m.add_separator()
        m.add_action('courses.Topics')
        m.add_action('courses.Lines')
        # m.add_separator()
        # m.add_action('courses.DraftCourses')
        # m.add_action('courses.InactiveCourses')
        # m.add_action('courses.ActiveCourses')
        # m.add_action('courses.ClosedCourses')
        m.add_separator()
        m.add_action('courses.PendingRequestedEnrolments')
        m.add_action('courses.PendingConfirmedEnrolments')

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.CourseTypes')
        m.add_action('courses.TeacherTypes')
        m.add_action('courses.PupilTypes')
        m.add_action('courses.Slots')

    def setup_reports_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.StatusReport')

