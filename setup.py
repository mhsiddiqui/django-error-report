import sys
from setuptools import setup, find_packages

setup(
    name="django-error-report",
    package_data={
        'error_report': [
            'README.md',
            'LICENSE.txt'
        ],
    },
    author="M Hassan Siddiqui",
    author_email="mhassan.eeng@gmail.com",
    description="View Django Error Report in Django Admin",
    url="https://github.com/mhsiddiqui/django-error-report",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages=[
        'error_report',
        'error_report.migrations',
    ],
    zip_safe=False,
    license="BSD License",
    install_requires=[
        'Django>=1.7'
    ],
    version='0.1.2',
)
