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
 03/03/2014            SLS         5         Groteclaes Gregory      50,00                              -612,50
 30/04/2014            SLS         11        Arens Annette           20,00                              -200,60
 31/05/2014            SLS         10        Östges Otto             64,00                              -693,76
 08/08/2014            SLS         28        Martelaer Mark          96,00                              -763,20
 31/10/2014            SLS         33        Arens Annette           64,00             20,00            -310,40
 30/11/2014            SLS         47        Arens Annette           48,00             84,00            -224,16
 01/12/2014            SLS         40        Groteclaes Gregory      50,00             50,00            -232,50
 08/12/2014            SLS         51        Martelaer Mark          48,00             96,00            -130,56
 11/12/2014            SLS         52        Bastiaensen Laurent     50,00                              -201,00
 31/12/2014            SLS         48        Östges Otto             48,00             64,00            -178,56
 01/01/2015            SLS         60        Demeulenaere Dorothée   48,00                              -93,60
 28/02/2015            SLS         69        Meier Marie-Louise      96,00                              -195,84
 03/03/2015            SLS         68        Groteclaes Gregory      114,00            100,00           -153,90
 08/03/2015            SLS         80        Martelaer Mark          20,00             144,00           -14,00
 31/03/2015            SLS         81        Brecht Bernd            64,00                              -65,28
 02/04/2015            SLS         74        Östges Otto             98,00             112,00           -191,10
 **Total (16 rows)**               **757**                           **978,00**        **670,00**       **-4 260,96**
===================== =========== ========= ======================= ================= ================ ================
<BLANKLINE>

