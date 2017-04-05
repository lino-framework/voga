.. _voga.specs.sales:

=============================
Sales management in Lino Voga
=============================

.. to test only this doc:

    $ python setup.py test -s tests.DocsTests.test_sales
    $ pytest -k test_sales

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *
    
See also :doc:`invoicing`.

Here are all our sales invoices:

>>> jnl = rt.models.ledger.Journal.get_by_ref('SLS')
>>> rt.show(sales.InvoicesByJournal, jnl)
===================== ============== ============ =================================== ================= ============== ================
 No.                   Voucher date   Due date     Partner                             Total incl. VAT   Subject line   Actions
--------------------- -------------- ------------ ----------------------------------- ----------------- -------------- ----------------
 83/2015               01/03/2015     30/04/2015   Brecht Bernd                        64,00                            **Registered**
 82/2015               01/03/2015     31/03/2015   Dupont Jean                         20,00                            **Registered**
 81/2015               01/03/2015     30/05/2015   Arens Annette                       48,00                            **Registered**
 80/2015               01/03/2015     31/03/2015   Radermacher Christian               48,00                            **Registered**
 79/2015               01/03/2015     30/04/2015   Engels Edgar                        48,00                            **Registered**
 78/2015               01/03/2015     01/03/2015   Bastiaensen Laurent                 50,00                            **Registered**
 77/2015               01/02/2015     28/02/2015   Radermacher Christian               64,00                            **Registered**
 76/2015               01/02/2015     03/03/2015   Östges Otto                         98,00                            **Registered**
 75/2015               01/02/2015     11/02/2015   Laschet Laura                       50,00                            **Registered**
 74/2015               01/02/2015     01/02/2015   Kaivers Karl                        50,00                            **Registered**
 73/2015               01/02/2015     01/02/2015   Bastiaensen Laurent                 50,00                            **Registered**
 72/2015               01/02/2015     28/02/2015   Dupont Jean                         48,00                            **Registered**
 71/2015               01/02/2015     01/02/2015   Meier Marie-Louise                  96,00                            **Registered**
 70/2015               01/02/2015     03/03/2015   Groteclaes Gregory                  114,00                           **Registered**
 69/2015               01/02/2015     11/02/2015   Radermacher Guido                   50,00                            **Registered**
 68/2015               01/01/2015     02/03/2015   Jacobs Jacqueline                   48,00                            **Registered**
 67/2015               01/01/2015     31/01/2015   Radermacher Christian               48,00                            **Registered**
 66/2015               01/01/2015     02/03/2015   Engels Edgar                        48,00                            **Registered**
 65/2015               01/01/2015     11/01/2015   Laschet Laura                       50,00                            **Registered**
 64/2015               01/01/2015     01/01/2015   Kaivers Karl                        50,00                            **Registered**
 63/2015               01/01/2015     01/01/2015   Bastiaensen Laurent                 100,00                           **Registered**
 62/2015               01/01/2015     01/04/2015   Demeulenaere Dorothée               48,00                            **Registered**
 61/2015               01/01/2015     01/04/2015   Arens Annette                       112,00                           **Registered**
 60/2015               01/01/2015     31/01/2015   Östges Otto                         114,00                           **Registered**
 59/2015               01/01/2015     31/01/2015   Groteclaes Gregory                  50,00                            **Registered**
 58/2014               01/12/2014     30/01/2015   Jacobs Jacqueline                   48,00                            **Registered**
 57/2014               01/12/2014     31/12/2014   Östges Otto                         50,00                            **Registered**
 56/2014               01/12/2014     11/12/2014   Laschet Laura                       50,00                            **Registered**
 55/2014               01/12/2014     01/12/2014   Kaivers Karl                        50,00                            **Registered**
 54/2014               01/12/2014     01/12/2014   Bastiaensen Laurent                 50,00                            **Registered**
 53/2014               01/12/2014     31/12/2014   Dupont Jean                         48,00                            **Registered**
 52/2014               01/12/2014     01/12/2014   Meier Marie-Louise                  96,00                            **Registered**
 51/2014               01/12/2014     11/12/2014   Radermacher Guido                   50,00                            **Registered**
 50/2014               01/11/2014     01/12/2014   Östges Otto                         48,00                            **Registered**
 49/2014               01/11/2014     30/01/2015   Arens Annette                       48,00                            **Registered**
 48/2014               01/11/2014     01/12/2014   Lahm Lisa                           48,00                            **Registered**
 47/2014               01/11/2014     30/11/2014   Radermacher Christian               48,00                            **Registered**
 46/2014               01/11/2014     01/12/2014   Emonts Daniel                       48,00                            **Registered**
 45/2014               01/11/2014     31/12/2014   Engels Edgar                        48,00                            **Registered**
 44/2014               01/11/2014     01/11/2014   Bastiaensen Laurent                 100,00                           **Registered**
 43/2014               01/11/2014     30/01/2015   Demeulenaere Dorothée               48,00                            **Registered**
 42/2014               01/11/2014     01/12/2014   Groteclaes Gregory                  50,00                            **Registered**
 41/2014               01/11/2014     11/11/2014   Radermacher Guido                   50,00                            **Registered**
 40/2014               01/10/2014     11/10/2014   Laschet Laura                       50,00                            **Registered**
 39/2014               01/10/2014     01/10/2014   Kaivers Karl                        50,00                            **Registered**
 38/2014               01/10/2014     01/10/2014   Bastiaensen Laurent                 50,00                            **Registered**
 37/2014               01/10/2014     31/10/2014   Dupont Jean                         48,00                            **Registered**
 36/2014               01/10/2014     01/10/2014   Meier Marie-Louise                  96,00                            **Registered**
 35/2014               01/10/2014     30/12/2014   Arens Annette                       64,00                            **Registered**
 34/2014               01/10/2014     31/10/2014   Östges Otto                         164,00                           **Registered**
 33/2014               01/10/2014     31/10/2014   Groteclaes Gregory                  50,00                            **Registered**
 32/2014               01/09/2014     01/10/2014   Radermacher Hedi                    590,00                           **Registered**
 31/2014               01/09/2014     11/09/2014   Radermacher Guido                   50,00                            **Registered**
 30/2014               01/08/2014     31/08/2014   Arens Annette                       295,00                           **Registered**
 29/2014               01/08/2014     30/10/2014   Demeulenaere Dorothée               96,00                            **Registered**
 28/2014               01/08/2014     31/08/2014   Dupont Jean                         96,00                            **Registered**
 27/2014               01/08/2014     01/08/2014   Meier Marie-Louise                  48,00                            **Registered**
 26/2014               01/08/2014     31/08/2014   Groteclaes Gregory                  50,00                            **Registered**
 25/2014               01/08/2014     11/08/2014   Radermacher Guido                   50,00                            **Registered**
 24/2014               01/07/2014     01/07/2014   Meier Marie-Louise                  48,00                            **Registered**
 23/2014               01/07/2014     29/09/2014   Arens Annette                       64,00                            **Registered**
 22/2014               01/07/2014     31/07/2014   Östges Otto                         64,00                            **Registered**
 21/2014               01/07/2014     31/07/2014   Groteclaes Gregory                  50,00                            **Registered**
 20/2014               01/07/2014     11/07/2014   Radermacher Guido                   50,00                            **Registered**
 19/2014               01/06/2014     01/07/2014   Groteclaes Gregory                  50,00                            **Registered**
 18/2014               01/05/2014     30/07/2014   Arens Annette                       64,00                            **Registered**
 17/2014               01/05/2014     31/05/2014   di Rupo Didier                      20,00                            **Registered**
 16/2014               01/05/2014     11/05/2014   Radermacher Guido                   50,00                            **Registered**
 15/2014               01/04/2014     31/05/2014   Jacobs Jacqueline                   20,00                            **Registered**
 14/2014               01/04/2014     31/05/2014   Engels Edgar                        40,00                            **Registered**
 13/2014               01/04/2014     08/04/2014   Vandenmeulenbos Marie-Louise        40,00                            **Registered**
 12/2014               01/04/2014     30/04/2014   Dobbelstein-Demeulenaere Dorothée   20,00                            **Registered**
 11/2014               01/04/2014     30/06/2014   Arens Annette                       20,00                            **Registered**
 10/2014               01/04/2014     01/05/2014   Östges Otto                         64,00                            **Registered**
 9/2014                01/04/2014     01/05/2014   Groteclaes Gregory                  50,00                            **Registered**
 8/2014                01/04/2014     11/04/2014   Radermacher Guido                   50,00                            **Registered**
 7/2014                01/03/2014     31/03/2014   Radermacher Christian               20,00                            **Registered**
 6/2014                01/03/2014     31/03/2014   Groteclaes Gregory                  50,00                            **Registered**
 5/2014                01/02/2014     03/03/2014   Groteclaes Gregory                  50,00                            **Registered**
 4/2014                01/02/2014     11/02/2014   Radermacher Guido                   50,00                            **Registered**
 3/2014                01/01/2014     11/01/2014   Radermacher Guido                   150,00                           **Registered**
 2/2014                01/01/2014     31/01/2014   Groteclaes Gregory                  100,00                           **Registered**
 1/2014                01/01/2014     31/01/2014   Radermacher Christian               64,00                            **Registered**
 **Total (83 rows)**                                                                   **5 639,00**
===================== ============== ============ =================================== ================= ============== ================
<BLANKLINE>

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


Printing invoices
=================

We take a sales invoice, clear the cache, ask Lino to print it and 
check whether we get the expected response.

>>> ses = settings.SITE.login("robin")
>>> dd.translation.activate('en')
>>> obj = sales.VatProductInvoice.objects.all()[0]
>>> obj.clear_cache()
>>> d = ses.run(obj.do_print)
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
appy.pod render .../sales/config/sales/VatProductInvoice/Default.odt -> .../media/cache/appypdf/sales.VatProductInvoice-91.pdf (language='en',params={'raiseOnError': True, 'ooPort': 8100, 'pythonWithUnoPath': ...}

>>> d['success']
True

>>> print(d['message'])
Your printable document (filename sales.VatProductInvoice-91.pdf) should now open in a new browser window. If it doesn't, please consult <a href="http://www.lino-framework.org/help/print.html" target="_blank">the documentation</a> or ask your system administrator.

Note that this test should fail if you run the test suite without a 
LibreOffice server running.


