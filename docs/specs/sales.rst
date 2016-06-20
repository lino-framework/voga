.. _voga.specs.sales:

=============================
Sales management in Lino Voga
=============================

.. to test only this doc:

    $ python setup.py test -s tests.DocsTests.test_sales

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *
    
See also :doc:`invoicing`. 

The :class:`lino_cosi.lib.sales.models.DueInvoices` table shows a list
of due invoices.

>>> rt.show(sales.DueInvoices)
===================== =========== ========= =================================== ================= ================ ================
 Due date              Reference   No.       Partner                             Total incl. VAT   Balance before   Balance to pay
--------------------- ----------- --------- ----------------------------------- ----------------- ---------------- ----------------
 03/03/2014            SLS         5         Groteclaes Gregory                  50,00                              -662,50
 08/04/2014            SLS         11        Dobbelstein-Demeulenaere Dorothée   20,00                              -240,40
 11/04/2014            SLS         7         Radermacher Guido                   50,00                              -439,50
 30/04/2014            SLS         10        Arens Annette                       68,00                              -797,64
 11/07/2014            SLS         20        Radermacher Guido                   50,00             50,00            -332,50
 31/07/2014            SLS         23        Arens Annette                       64,00             68,00            -558,08
 31/07/2014            SLS         24        Meier Marie-Louise                  116,00                             -918,72
 31/10/2014            SLS         33        Meier Marie-Louise                  96,00             116,00           -528,00
 01/12/2014            SLS         49        Laschet Laura                       50,00                              -202,00
 11/01/2015            SLS         56        Bastiaensen Laurent                 100,00                             -295,00
 08/02/2015            SLS         65        Martelaer Mark                      48,00                              -94,56
 28/02/2015            SLS         64        Meier Marie-Louise                  96,00             212,00           -67,20
 01/03/2015            SLS         48        Kaivers Karl                        50,00                              -171,00
 **Total (13 rows)**               **415**                                       **858,00**        **446,00**       **-5 307,10**
===================== =========== ========= =================================== ================= ================ ================
<BLANKLINE>

