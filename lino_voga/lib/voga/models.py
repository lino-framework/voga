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

"""
The :xfile:`models.py` for the :mod:`lino_voga` app.
"""

from lino.api import dd

from lino_xl.lib.courses import workflows


# if False:
#     # 20131025 fails because MergeAction.__init__ tries to use _lino_ddh
#     # which hasn't yet been installed

#     @dd.when_prepared('contacts.Person', 'contacts.Company')
#     def add_merge_action(model):
#         model.define_action(merge_row=dd.MergeAction(model))

# else:

#     @dd.receiver(dd.pre_analyze)
#     def add_merge_action(sender, **kw):
#         apps = sender.modules
#         # for m in (apps.contacts.Person, apps.contacts.Company):
#         for m in (apps.courses.Pupil, apps.contacts.Company):
#             m.define_action(merge_row=dd.MergeAction(m))


# def site_setup(site):

#     site.actors.system.SiteConfigs.set_detail_layout(
#         """
#         site_company next_partner_id:10
#         default_build_method simulate_today
#         clients_account   sales_account
#         suppliers_account purchases_account
#         site_calendar default_event_type pupil_guestrole
#         max_auto_events hide_events_before
#         """)

