.. _voga.tested.general:

=======
General
=======

.. To run only this test::

    $ python setup.py test -s tests.DocsTests.test_general

    doctest init:

    >>> import lino
    >>> lino.startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *

The demo database has 35 pupils and 8 teachers:

>>> rt.modules.courses.Pupil.objects.count()
35
>>> rt.modules.courses.Teacher.objects.count()
8


