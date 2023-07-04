              
django-error-report-2
===================
Maintained fork of [django-error-report](https://github.com/mhsiddiqui/django-error-report). Original author  [mhsiddiqui](https://github.com/mhsiddiqui/)

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

-  A simple user interface for browsing error records in the database.

Requirements
============

-  Python 2.7, 3.6
-  Django > 1.7

Installation
============

1. To install, simply run:

       pip install django-error-report

2. Add ``error_report`` to your ``INSTALLED_APPS`` setting.
3. Add below in your ``urls.py`` file

       url(r'^error/', include('error_report.urls'))

4. Add ``error_report.middleware.ExceptionProcessor`` in your middlewares
5. Run ``manage.py migrate`` to create the database tables.

Configuration
=============

Required settings for Django-error-report should be added in settings.py
file like this


    ERROR_DETAIL_SETTINGS = {
        "CONFIGURATION_OPTION": VALUE
    }

Available configuration options are below - ERROR\_DETAIL\_ENABLE:

1.  ERROR\_DETAIL\_ENABLE: Should Log error detail or not (True/False)

2.  ERROR\_DETAIL\_HEIGHT: Height of Iframe in admin (in pixels)
