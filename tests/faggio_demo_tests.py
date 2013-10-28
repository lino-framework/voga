"""

To run only this test::

  $ export DJANGO_SETTINGS_MODULE=lino_faggio.settings.test
  $ python -m unittest tests.faggio_demo_test
 

"""
from lino.utils.test import DemoTestCase
from django.contrib.contenttypes.models import ContentType
from lino.runtime import *

class MyTestCase(DemoTestCase):
    
    def test_001(self):
        
        json_fields = 'count rows title success no_data_text param_values'
        kw = dict(fmt='json',limit=10,start=0)
        mt = ContentType.objects.get_for_model(courses.Line).pk

        self.demo_get('rolf','api/courses/CoursesByLine',json_fields,4,mt=mt,mk=1,**kw)


