.. _faggio.courses:

=======
Courses
=======


.. actors_overview:: 
    courses.Courses
    courses.Lines
    courses.Topics
    courses.Enrolments
    courses.Pupils
    courses.Teachers
    

Reference
=========

.. actor:: courses.Pupil
.. actor:: courses.Teacher
.. actor:: courses.Line

    A line (of :ref:`faggio.courses.Courses`) is a series which groups
    courses into a configurable list of categories. 
    The default database has  the following list of Course Lines:
  
    .. django2rst:: settings.SITE.login('robin').show(courses.Lines)
  
  
.. actor:: courses.Course
.. actor:: courses.Topic
.. actor:: courses.Enrolment
.. actor:: courses.Slot
.. actor:: courses.PupilType
.. actor:: courses.TeacherType
