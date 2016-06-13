.. _voga.specs.sales:

Sales
=====

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
 07/05/2014            SLS         21        Groteclaes Gregory      1 000,00                           1 000,00
 09/05/2014            SLS         17        Evers Eberhart          280,00                             -546,00
 11/05/2014            SLS         33        Emonts Erich            360,00                             360,00
 12/05/2014            SLS         26        Jonas Josef             230,00                             69,00
 22/05/2014            SLS         2         Radermacher Edgard      220,00                             220,00
 22/05/2014            SLS         5         Laschet Laura           250,00                             250,00
 29/05/2014            SLS         8         Jacobs Jacqueline       180,00                             180,00
 31/05/2014            SLS         4         Meier Marie-Louise      130,00                             130,00
 31/05/2014            SLS         29        Lambertz Guido          600,00                             600,00
 07/06/2014            SLS         30        Malmendier Marc         720,00                             720,00
 21/06/2014            SLS         7         Jonas Josef             200,00            69,00            200,00
 21/07/2014            SLS         1         Radermacher Hedi        150,00                             150,00
 21/07/2014            SLS         9         Hilgers Hildegard       200,00                             200,00
 20/08/2014            SLS         3         Radermacher Christian   250,00                             250,00
 20/08/2014            SLS         6         Kaivers Karl            170,00                             170,00
 **Total (15 rows)**               **201**                           **4 940,00**      **69,00**        **3 953,00**
===================== =========== ========= ======================= ================= ================ ================
<BLANKLINE>
