# -*- coding: UTF-8 -*-
# Copyright 2016-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Adds some specific fields for managing the member fee.

"""


from lino.api import dd, _
from lino_voga.lib.courses.desktop import *


Courses = ActivitiesByLayout

# class Courses(ActivitiesByLayout):
#     # required_roles = dd.login_required(CoursesUser)
#     _activity_layout = ActivityLayouts.default
#     required_roles = dd.login_required(CoursesUser)


class EnrolmentsByHike(EnrolmentsByCourse):
    column_names = 'request_date pupil '\
                   'places:8 remark fee option amount ' \
                   'workflow_buttons *'
    insert_layout = """
    pupil
    places option
    remark
    request_date user
    """


class EnrolmentsByJourney(EnrolmentsByHike):
    pass


class HikeDetail(CourseDetail):
    enrolments = dd.Panel("""
    enrolments_top
    EnrolmentsByHike
    """, label=_("Enrolments"))


class JourneyDetail(CourseDetail):
    enrolments = dd.Panel("""
    enrolments_top
    EnrolmentsByJourney
    """, label=_("Enrolments"))


class Hikes(ActivitiesByLayout):
    activity_layout = 'hikes'
    detail_layout = HikeDetail()
    column_names = "ref name start_date enrolments_until line " \
                   "workflow_buttons *"


class Journeys(ActivitiesByLayout):
    activity_layout = 'journeys'
    detail_layout = JourneyDetail()
    column_names = "ref name start_date end_date enrolments_until line " \
                   "workflow_buttons *"


class PupilDetail(PupilDetail):
    # main = "general courses.EnrolmentsByPupil"
    # main = contacts.PersonDetail.main + ' courses_tab'

    # general = dd.Panel(contacts.PersonDetail.main, label=_("General"))
    # box5 = "remarks"

    courses = dd.Panel("""
    legacy_id member_until section is_lfv is_ckk is_raviva
    courses.EnrolmentsByPupil
    """, label=dd.plugins.courses.verbose_name)


Pupils.detail_layout = PupilDetail()
Pupils.insert_layout = """
first_name last_name
gender language
pupil_type section member_until
is_lfv is_ckk is_raviva
"""
Pupils.params_layout = "course partner_list #aged_from #aged_to gender "\
                       "show_members show_lfv show_ckk show_raviva"
Pupils.column_names = (
    'name_column address_column '
    'pupil_type section is_lfv is_ckk is_raviva member_until *')
