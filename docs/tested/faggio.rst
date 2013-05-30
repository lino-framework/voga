.. _faggio.tested.faggio:

Faggio
=======

.. include:: /include/tested.rst

The following statement imports a set of often-used global names::

>>> from lino.runtime import *

We can now refer to every installed app via it's `app_label`.
For example here is how we can verify here that the demo database 
has 23 pupils and 7 teachers:

>>> school.Pupil.objects.count()
23
>>> school.Teacher.objects.count()
7

