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
===================== =========== ========= ======================= ================= ================ ================
 Due date              Reference   No.       Partner                 Total incl. VAT   Balance before   Balance to pay
--------------------- ----------- --------- ----------------------- ----------------- ---------------- ----------------
 03/03/2014            SLS         5         Groteclaes Gregory      50,00                              -630,00
 01/05/2014            SLS         10        Östges Otto             64,00                              -500,48
 30/06/2014            SLS         11        Arens Annette           20,00                              -240,60
 31/08/2014            SLS         28        Dupont Jean             96,00                              -758,40
 11/09/2014            SLS         31        Radermacher Guido       50,00                              -300,00
 01/10/2014            SLS         32        Radermacher Hedi        590,00                             -4 165,40
 01/10/2014            SLS         38        Bastiaensen Laurent     50,00                              -232,50
 01/10/2014            SLS         39        Kaivers Karl            50,00                              -298,50
 01/12/2014            SLS         42        Groteclaes Gregory      50,00             50,00            -185,00
 01/12/2014            SLS         48        Lahm Lisa               48,00                              -184,80
 01/12/2014            SLS         54        Bastiaensen Laurent     50,00             50,00            -85,00
 31/12/2014            SLS         57        Östges Otto             50,00             64,00            -186,00
 30/01/2015            SLS         43        Demeulenaere Dorothée   48,00                              -240,96
 30/01/2015            SLS         58        Jacobs Jacqueline       48,00                              -178,56
 28/02/2015            SLS         72        Dupont Jean             48,00             96,00            -94,56
 01/04/2015            SLS         62        Demeulenaere Dorothée   48,00             48,00            -80,16
 30/05/2015            SLS         81        Arens Annette           48,00             20,00            -45,60
 **Total (17 rows)**               **711**                           **1 408,00**      **328,00**       **-8 406,52**
===================== =========== ========= ======================= ================= ================ ================
<BLANKLINE>
