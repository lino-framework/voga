# -*- coding: UTF-8 -*-
# Copyright 2017-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""The default :attr:`custom_layouts_module
<lino.core.site.Site.custom_layouts_module>` for Lino Voga.

"""

from lino.api import rt

rt.models.system.SiteConfigs.set_detail_layout("""
site_company next_partner_id:10
default_build_method simulate_today
site_calendar default_event_type pupil_guestrole
max_auto_events hide_events_before
""", window_size=(60, 'auto'))
