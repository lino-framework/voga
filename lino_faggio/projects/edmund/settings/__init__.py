# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import datetime

from lino_faggio.projects.base import *


class Site(Site):

    title = "Lino Faggio all'estone"
    languages = "et en"

    demo_fixtures = """std few_languages few_countries eesti few_cities
    demo faggio demo2""".split()
