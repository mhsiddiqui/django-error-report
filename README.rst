
django-error-report
===================

View all Django Error detail in Django Admin.

Error-report save Django error traceback and details which would be the
same beautiful exception page that Django displays when debugging is
enabled and saves it to the database so you can view it later.

It’s simple alternative to django-sentry which is a paid option to see
error detail.

You can create issues for feature you want in django-error-report in
future.

Features
========


* A simple user interface for browsing error records in the database.

Requirements
============


* Python 2.7, 3.6
* Django > 1.7

Installation
============


#. 
   To install, simply run:

   .. code-block::

      pip install django-error-report

#. 
   Add ``error_report`` to your ``INSTALLED_APPS`` setting.

#. 
   Add below in your ``urls.py`` file

   .. code-block::

      url(r'^error/', include('error_report.urls'))

#. 
   Add ``error_report.middleware.ExceptionProcessor`` in your middlewares

#. Run ``manage.py migrate`` to create the database tables.

Configuration
=============

Required settings for Django-error-report should be added in settings.py
file like this

.. code-block::

   ERROR_DETAIL_SETTINGS = {
       "CONFIGURATION_OPTION": VALUE
   }


Available configuration options are below - ERROR_DETAIL_ENABLE:


#. 
   ERROR_DETAIL_ENABLE: Should Log error detail or not (True/False)

#. 
   ERROR_DETAIL_HEIGHT: Height of Iframe in admin (in pixels)
