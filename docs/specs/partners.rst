.. _voga.specs.checkdata:

=====================
Partners in Lino Voga
=====================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_partners

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *


Lino Voga differentiates the following subclasses of Partner:

.. django2rst:: contacts.Partner.print_subclasses_graph()


>>> courses.Pupil
<class 'lino_voga.projects.roger.lib.courses.models.Pupil'>
>>> issubclass(courses.Pupil, contacts.Person)
True
>>> issubclass(courses.Teacher, contacts.Person)
True
>>> issubclass(courses.Teacher, contacts.Partner)
True
