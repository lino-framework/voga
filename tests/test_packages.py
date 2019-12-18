from lino.utils.pythontest import TestCase
from lino_voga import SETUP_INFO


class PackagesTests(TestCase):
    def test_01(self):
        self.run_packages_test(SETUP_INFO['packages'])
