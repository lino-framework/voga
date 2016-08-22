"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_cal

"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

import lino_voga

from lino.utils.pythontest import TestCase


class BaseTestCase(TestCase):
    project_root = ROOTDIR
    django_settings_module = 'lino_voga.projects.docs.settings.doctests'


class PackagesTests(TestCase):

    def test_packages(self):
        self.run_packages_test(lino_voga.SETUP_INFO['packages'])


class SpecsTests(BaseTestCase):

    def test_print_labels(self):
        return self.run_simple_doctests('docs/specs/print_labels.rst')

    def test_partners(self):
        return self.run_simple_doctests('docs/specs/partners.rst')

    def test_pupils(self):
        return self.run_simple_doctests('docs/specs/pupils.rst')

    def test_checkdata(self):
        return self.run_simple_doctests('docs/specs/checkdata.rst')

    def test_profiles(self):
        return self.run_simple_doctests('docs/specs/profiles.rst')

    def test_roger(self):
        return self.run_simple_doctests('docs/specs/roger.rst')

    def test_invoicing(self):
        return self.run_simple_doctests('docs/specs/invoicing.rst')


class DocsTests(BaseTestCase):
    def test_cal(self):
        return self.run_simple_doctests('docs/specs/cal.rst')

    def test_holidays(self):
        return self.run_simple_doctests('docs/specs/holidays.rst')

    def test_sales(self):
        return self.run_simple_doctests('docs/specs/sales.rst')

    def test_ledger(self):
        return self.run_simple_doctests('docs/specs/ledger.rst')

    def test_courses(self):
        return self.run_simple_doctests('docs/specs/courses.rst')

    def test_presences(self):
        return self.run_simple_doctests('docs/specs/presences.rst')

    def test_voga(self):
        return self.run_simple_doctests('docs/specs/voga.rst')

    def test_general(self):
        return self.run_simple_doctests('docs/specs/general.rst')


class DemoTests(BaseTestCase):
    """
    $ python setup.py test -s tests.DemoTests.test_admin
    """

    def test_admin(self):
        self.run_django_manage_test('lino_voga/projects/roger')
        self.run_django_manage_test('lino_voga/projects/edmund')


