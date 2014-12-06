"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

import lino_faggio

from lino.utils.pythontest import TestCase

import os
os.environ['DJANGO_SETTINGS_MODULE'] = "lino_faggio.projects.docs.settings.doctests"


class BaseTestCase(TestCase):
    project_root = ROOTDIR
    demo_settings_module = 'lino_faggio.projects.docs.settings.doctests'


class DocsTests(BaseTestCase):
    def test_cal(self):
        return self.run_docs_doctests('tested/cal.rst')

    def test_ledger(self):
        return self.run_docs_doctests('tested/ledger.rst')

    def test_courses(self):
        return self.run_docs_doctests('tested/courses.rst')

    def test_faggio(self):
        return self.run_docs_doctests('tested/faggio.rst')

    def test_general(self):
        return self.run_docs_doctests('tested/general.rst')

    def test_packages(self):
        self.run_packages_test(lino_faggio.SETUP_INFO['packages'])


class DemoTests(BaseTestCase):
    """
    $ python setup.py test -s tests.DemoTests.test_admin
    """

    def test_admin(self):
        self.run_django_manage_test('lino_faggio/projects/docs')
        self.run_django_manage_test('lino_faggio/projects/roger')
        self.run_django_manage_test('lino_faggio/projects/edmund')


