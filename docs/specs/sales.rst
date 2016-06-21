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
 03/03/2014            SLS         5         Groteclaes Gregory                  50,00                              -629,50
 08/04/2014            SLS         11        Dobbelstein-Demeulenaere Dorothée   20,00                              -234,40
 11/04/2014            SLS         7         Radermacher Guido                   50,00                              -468,50
 30/04/2014            SLS         10        Arens Annette                       68,00                              -794,92
 11/07/2014            SLS         20        Radermacher Guido                   50,00             50,00            -333,50
 31/07/2014            SLS         23        Arens Annette                       64,00             68,00            -551,68
 31/07/2014            SLS         24        Meier Marie-Louise                  116,00                             -924,52
 31/10/2014            SLS         33        Meier Marie-Louise                  96,00             116,00           -537,60
 08/12/2014            SLS         47        Martelaer Mark                      48,00                              -112,80
 11/12/2014            SLS         48        Bastiaensen Laurent                 100,00                             -404,00
 31/12/2014            SLS         44        Östges Otto                         48,00                              -178,56
 01/01/2015            SLS         59        Laschet Laura                       50,00                              -85,00
 08/01/2015            SLS         62        Jacobs Jacqueline                   48,00                              -82,56
 31/01/2015            SLS         55        Arens Annette                       112,00            132,00           -330,40
 11/02/2015            SLS         67        Bastiaensen Laurent                 50,00             100,00           -97,50
 08/03/2015            SLS         72        Faymonville Luc                     48,00                              -31,20
 30/05/2015            SLS         73        Radermacher Christian               48,00                              -48,96
 **Total (17 rows)**               **660**                                       **1 066,00**      **466,00**       **-5 845,60**
===================== =========== ========= =================================== ================= ================ ================
<BLANKLINE>

