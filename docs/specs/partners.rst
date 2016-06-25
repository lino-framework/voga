.. _voga.specs.partners:

=====================
Partners in Lino Voga
=====================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_partners

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *


Partners in Lino Voga are :class:`polymorphic
<lino.mixins.polymorphic.Polymorphic>`, i.e. the database has a series
of models which are more or less specialized subclasses of a partner.

In Lino Voga we differentiate the following subclasses of Partner:

.. django2rst:: contacts.Partner.print_subclasses_graph()


..
    >>> from lino.mixins.polymorphic import Polymorphic
    >>> issubclass(contacts.Person, Polymorphic)
    True
    >>> issubclass(contacts.Person, contacts.Partner)
    True
    >>> issubclass(courses.Pupil, contacts.Person)
    True
    >>> issubclass(courses.Teacher, contacts.Person)
    True
    >>> issubclass(courses.Teacher, contacts.Partner)
    True

    >>> print(noblanklines(contacts.Partner.get_subclasses_graph()))
    .. graphviz::
       digraph foo {
        "Partner" -> "Organization"
        "Partner" -> "Person"
        "Person" -> "Participant"
        "Person" -> "Instructor"
      }
