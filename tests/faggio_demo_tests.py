# -*- coding: UTF-8 -*-
## Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

To run only this test::

  $ go faggio
  $ python setup.py test -s tests.faggio_demo_tests

 

"""
from lino.utils.test import DemoTestCase
from lino.api.shell import *


class MyTestCase(DemoTestCase):
    
    def test_001(self):
        
        ContentType = rt.modules.contenttypes.ContentType
        json_fields = 'count rows title success no_data_text param_values'
        kw = dict(fmt='json', limit=10, start=0)
        mt = ContentType.objects.get_for_model(courses.Line).pk

        self.demo_get(
            'robin',
            'api/courses/CoursesByLine', json_fields, 3, mt=mt, mk=1, **kw)


