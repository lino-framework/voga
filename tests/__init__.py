"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load  SETUP_INFO:
execfile(ROOTDIR.child('lino_faggio','project_info.py'),globals())

from djangosite.utils.pythontest import TestCase

import os
os.environ['DJANGO_SETTINGS_MODULE'] = "lino_faggio.settings.test"

class BaseTestCase(TestCase):
    #~ default_environ = dict(DJANGO_SETTINGS_MODULE="lino_faggio.demo.settings")
    project_root = ROOTDIR
    
    
class QuickTests(BaseTestCase):
    #~ demo_settings_module = "lino_faggio.settings.test"
    def test_faggio(self): return self.run_docs_doctests('tested/faggio.rst')
    def test_general(self): return self.run_docs_doctests('tested/general.rst')
    #~ def test_demo(self): return self.run_unittest('tests.faggio_demo_tests')
    def test_packages(self): self.run_packages_test(SETUP_INFO['packages'])

class DemoTests(BaseTestCase):
    """
    $ python setup.py test -s tests.DemoTests.test_admin
    """
    #~ demo_settings_module = "lino_faggio.settings.demo"
    def test_admin(self): self.run_django_admin_test('lino_faggio.settings.demo')


