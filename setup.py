"""Setup for django-error-report-2 package."""
from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="django-error-report-2",
    package_data={
        'error_report': [
            'README.md',
            'LICENSE.txt'
        ],
    },
    author="M Hassan Siddiqui",
    author_email="mhassan.eeng@gmail.com",
    description="View Django Error Report in Django Admin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matmair/django-error-report-2",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages=find_packages(exclude=['build', 'dist', 'django_error_report.egg-info']),
    zip_safe=False,
    license="BSD License",
    install_requires=[
        'Django>=1.7'
    ],
    version='0.4.2',
)
