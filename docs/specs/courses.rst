.. _voga.specs.courses:

=======================
Activities in Lino Voga
=======================

.. to test only this doc:

    $ python setup.py test -s tests.DocsTests.test_courses

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *

This document specifies how the :mod:`lino_xl.lib.courses` plugin is
being used in :ref:`voga`.


Implementation
==============

>>> dd.plugins.courses
lino_voga.projects.roger.lib.courses (extends_models=['Pupil', 'Enrolment', 'Line'])

>>> dd.plugins.courses.__class__.__bases__
(<class 'lino_voga.lib.courses.Plugin'>,)
    

Pupils and teachers
===================

Lino Voga adds specific models for teachers and pupils.
A teacher is a person with a `teacher_type`.
A pupil is a person with a `pupil_type`.

The :mod:`lino_xl.lib.courses` plugin has two settings
:attr:`teacher_model <lino_xl.lib.courses.Plugin.teacher_model>` and
:attr:`pupil_model <lino_xl.lib.courses.Plugin.pupil_model>`:


>>> dd.plugins.courses.teacher_model
<class 'lino_voga.lib.courses.models.Teacher'>

>>> dd.plugins.courses.pupil_model
<class 'lino_voga.projects.roger.lib.courses.models.Pupil'>

>>> ses = rt.login('robin')

>>> ses.show(rt.actors.courses.PupilTypes)
==== =========== ============= ================== ==================
 ID   Reference   Designation   Designation (de)   Designation (fr)
---- ----------- ------------- ------------------ ------------------
 1    M           Member        Mitglied           Member
 2    H           Helper        Helfer             Helper
 3    N           Non-member    Nicht-Mitglied     Non-member
==== =========== ============= ================== ==================
<BLANKLINE>

>>> ses.show(rt.actors.courses.TeacherTypes)
==== =========== ================== ======================= ======================
 ID   Reference   Designation        Designation (de)        Designation (fr)
---- ----------- ------------------ ----------------------- ----------------------
 1    S           Independant        Selbstständig           Indépendant
 2    EP          Voluntary (flat)   Ehrenamtlich pauschal   Volontaire (forfait)
 3    ER          Voluntary (real)   Ehrenamtlich real       Volontaire (réel)
 4    LBA         LEA                LBA                     ALE
==== =========== ================== ======================= ======================
<BLANKLINE>


See also :doc:`pupils`.


Enrolments
==========

>>> rt.show('courses.EnrolmentStates')
======= =========== ===========
 value   name        text
------- ----------- -----------
 10      requested   Requested
 11      trying      Trying
 20      confirmed   Confirmed
 30      cancelled   Cancelled
======= =========== ===========
<BLANKLINE>

>>> rt.show('courses.EnrolmentStates', language="de")
====== =========== ===========
 Wert   name        Text
------ ----------- -----------
 10     requested   Angefragt
 11     trying      Probe
 20     confirmed   Bestätigt
 30     cancelled   Storniert
====== =========== ===========
<BLANKLINE>



The fee of a course
===================

Per course and per enrolment we get a new field :attr:`fee`.

Number of places
================

The :attr:`max_places<lino_xl.lib.courses.models.Course.max_places>`
(:ddref:`courses.Course.max_places`) field of a *course* contains the
number of available places.

It is a simple integer value and expresses an *absolute* upper limit
which cannot be bypassed. Lino will refuse to confirm an enrolment if
this limit is reached. Here is a user statement about this:

    Also im Prinzip nehmen wir bei den Computerkursen maximal 10 Leute
    an. Da wir aber überall über 12 Geräte verfügen, können wir immer
    im Bedarfsfall um 2 Personen aufstocken. Also bei PC-Kursen setzen 
    wir das Maximum immer auf 12. Als Regel gilt dann, dass wir immer nur
    10 annehmen, aber falls unbedingt erforderlich auf 12 gehen
    können.

Every *enrolment* has a field
:attr:`places<lino_xl.lib.courses.models.Enrolment.places>`
(:ddref:`courses.Enrolment.places`) which expresses how many places
this enrolment takes. This is usually 1, but for certain types of
courses, e.g. bus travels, it can happen that one enrolment is for two
or more persons.


Waiting things
==============


The following is waiting for :ticket:`526` before it can work:

>>> # demo_get('robin', 'choices/courses/Courses/city', 'bla', 0)


CoursesByLine
=============

There are two Yoga courses:

>>> obj = courses.Line.objects.get(pk=10)
>>> obj
Line #10 ('Yoga')
        
>>> rt.show(rt.actors.courses.CoursesByLine, obj)
================================ ============== ================== ============= ================
 Description                      When           Room               Times         Instructor
-------------------------------- -------------- ------------------ ------------- ----------------
 *024C Yoga* / *David da Vinci*   Every Monday   Conferences room   18:00-19:30   David da Vinci
 *025C Yoga* / *Hans Altenberg*   Every Friday   Conferences room   19:00-20:30   Hans Altenberg
================================ ============== ================== ============= ================
<BLANKLINE>


>>> ContentType = rt.modules.contenttypes.ContentType
>>> json_fields = 'count rows title success no_data_text param_values'
>>> kw = dict(fmt='json', limit=10, start=0)
>>> mt = ContentType.objects.get_for_model(courses.Line).pk
>>> demo_get('robin',
...          'api/courses/CoursesByLine', json_fields, 3, 
...          mt=mt, mk=obj.pk, **kw)


Status report
=============

The status report gives an overview of active courses.

(TODO: demo fixture should avoid negative free places)

>>> rt.show(rt.actors.courses.StatusReport)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
~~~~~~~~
Journeys
~~~~~~~~
<BLANKLINE>
====================================== ======================= ======= ================== =========== ============= ===========
 Description                            When                    Times   Available places   Confirmed   Free places   Requested
-------------------------------------- ----------------------- ------- ------------------ ----------- ------------- -----------
 *001 Greece 2014* / *Hans Altenberg*   14/08/2014-20/08/2014                              1                         0
 **Total (1 rows)**                                                     **0**              **1**       **0**         **0**
====================================== ======================= ======= ================== =========== ============= ===========
<BLANKLINE>
~~~~~~~~
Computer
~~~~~~~~
<BLANKLINE>
============================================================ ================= ============= ================== =========== ============= ===========
 Description                                                  When              Times         Available places   Confirmed   Free places   Requested
------------------------------------------------------------ ----------------- ------------- ------------------ ----------- ------------- -----------
 *003 comp (First Steps)* / *Daniel Emonts*                   Every Monday      13:30-15:00   3                  3           0             0
 *004 comp (First Steps)* / *Germaine Gernegroß*              Every Wednesday   17:30-19:00   3                  2           1             0
 *005 comp (First Steps)* / *Josef Jonas*                     Every Friday      13:30-15:00   3                  2           1             0
 *006C WWW (Internet for beginners)* / *Marc Malmendier*      Every Monday      13:30-15:00   4                  2           2             0
 *007C WWW (Internet for beginners)* / *Edgard Radermacher*   Every Wednesday   17:30-19:00   4                  3           1             0
 *008C WWW (Internet for beginners)* / *David da Vinci*       Every Friday      13:30-15:00   4                  0           4             1
 **Total (6 rows)**                                                                           **21**             **12**      **9**         **1**
============================================================ ================= ============= ================== =========== ============= ===========
<BLANKLINE>
~~~~~
Sport
~~~~~
<BLANKLINE>
========================================================= ================= ============= ================== =========== ============= ===========
 Description                                               When              Times         Available places   Confirmed   Free places   Requested
--------------------------------------------------------- ----------------- ------------- ------------------ ----------- ------------- -----------
 *009C BT (Belly dancing)* / *Hans Altenberg*              Every Wednesday   19:00-20:00   10                 2           8             1
 *010C FG (Functional gymnastics)* / *Charlotte Collard*   Every Monday      11:00-12:00   5                  3           2             0
 *011C FG (Functional gymnastics)* / *Daniel Emonts*       Every Monday      13:30-14:30   5                  2           3             0
 *012 Rücken (Swimming)* / *Germaine Gernegroß*            Every Monday      11:00-12:00   20                 3           17            0
 *013 Rücken (Swimming)* / *Josef Jonas*                   Every Monday      13:30-14:30   20                 3           17            0
 *014 Rücken (Swimming)* / *Marc Malmendier*               Every Tuesday     11:00-12:00   20                 3           17            0
 *015 Rücken (Swimming)* / *Edgard Radermacher*            Every Tuesday     13:30-14:30   20                 1           19            1
 *016 Rücken (Swimming)* / *David da Vinci*                Every Thursday    11:00-12:00   20                 4           16            0
 *017 Rücken (Swimming)* / *Hans Altenberg*                Every Thursday    13:30-14:30   20                 4           16            0
 *018 SV (Self-defence)* / *Charlotte Collard*             Every Friday      18:00-19:00   12                 1           11            2
 *019 SV (Self-defence)* / *Daniel Emonts*                 Every Friday      19:00-20:00   12                 3           9             0
 **Total (11 rows)**                                                                       **164**            **29**      **135**       **4**
========================================================= ================= ============= ================== =========== ============= ===========
<BLANKLINE>
~~~~~~~~~~
Meditation
~~~~~~~~~~
<BLANKLINE>
============================================================== ============== ============= ================== =========== ============= ===========
 Description                                                    When           Times         Available places   Confirmed   Free places   Requested
-------------------------------------------------------------- -------------- ------------- ------------------ ----------- ------------- -----------
 *020C GLQ (GuoLin-Qigong)* / *Germaine Gernegroß*              Every Monday   18:00-19:30                      3                         0
 *021C GLQ (GuoLin-Qigong)* / *Josef Jonas*                     Every Friday   19:00-20:30                      1                         0
 *022C MED (Finding your inner peace)* / *Marc Malmendier*      Every Monday   18:00-19:30   30                 0           30            2
 *023C MED (Finding your inner peace)* / *Edgard Radermacher*   Every Friday   19:00-20:30   30                 2           28            0
 *024C Yoga* / *David da Vinci*                                 Every Monday   18:00-19:30   20                 2           18            0
 *025C Yoga* / *Hans Altenberg*                                 Every Friday   19:00-20:30   20                 2           18            0
 **Total (6 rows)**                                                                          **100**            **10**      **94**        **2**
============================================================== ============== ============= ================== =========== ============= ===========
<BLANKLINE>
~~~~~~~
Externe
~~~~~~~
<BLANKLINE>
No data to display



Free places
===========

Note the *free places* field which is not always trivial.  Basicially
it contains `max_places - number of confirmed enrolments`.  But it
also looks at the `end_date` of these enrolments.

List of courses which have a confirmed ended enrolment:

>>> qs = courses.Enrolment.objects.filter(end_date__lt=dd.today(),
...     state=courses.EnrolmentStates.confirmed)
>>> for obj in qs:
...     print("{} {}".format(obj.course.id, obj.course.max_places))
4 3
10 5
20 None
8 4
3 3
23 30
2 None
19 12
22 30
25 20
1 None
7 4
11 5
21 None
6 4

In course #25 there are 8 confirmed enrolments, but only 5 of them are
actually taking a place because the 3 other ones are already ended.


>>> obj = courses.Course.objects.get(pk=11)
>>> print(obj.max_places)
5
>>> print(obj.get_free_places())
3
>>> rt.show(rt.actors.courses.EnrolmentsByCourse, obj, column_names="pupil start_date end_date places")
=========================== ============ ============ =============
 Participant                 Start date   End date     Places used
--------------------------- ------------ ------------ -------------
 Laurent Bastiaensen (MES)                             1
 Laura Laschet (ME)                                    1
 Otto Östges (ME)                         08/11/2014   1
 **Total (3 rows)**                                    **3**
=========================== ============ ============ =============
<BLANKLINE>

Above situation is because we are working on 20150522:

>>> print(dd.today())
2015-05-22

The same request on earlier dates yields different results:

On 20140101 nobody has left yet, 5+3 places are taken and therefore
20-8=12 places are free:

>>> print(obj.get_free_places(i2d(20141107)))
2

On 20141108 is Otto's last day, so his place is not yet free:

>>> print(obj.get_free_places(i2d(20141108)))
2

On 20141109 is is:

>>> print(obj.get_free_places(i2d(20141109)))
3



Filtering pupils
================

>>> print(rt.actors.courses.Pupils.params_layout.main)
course partner_list #aged_from #aged_to gender show_members show_lfv show_ckk show_raviva

There are 36 pupils (21 men and 15 women) in our database:

>>> json_fields = 'count rows title success no_data_text param_values'
>>> kwargs = dict(fmt='json', limit=10, start=0)
>>> demo_get('robin', 'api/courses/Pupils', json_fields, 36, **kwargs)

>>> kwargs.update(pv=['', '', 'M', '', '', '', ''])
>>> demo_get('robin', 'api/courses/Pupils', json_fields, 21, **kwargs)

>>> kwargs.update(pv=['', '', 'F', '', '', '', ''])
>>> demo_get('robin', 'api/courses/Pupils', json_fields, 15, **kwargs)


>>> json_fields = 'navinfo disable_delete data id title'
>>> kwargs = dict(fmt='json', an='detail')
>>> demo_get('robin', 'api/courses/Lines/2', json_fields, **kwargs)



.. _voga.presence_sheet:

Presence sheet
==============

The **presence sheet** of a course is a printable document where
course instructors can manually record the presences of the
participants for every event.
