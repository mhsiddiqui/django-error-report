from os import path
from setuptools import setup, find_packages
from codecs import open


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


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
    long_description=long_description,
    url="https://github.com/mhsiddiqui/django-error-report",
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
    version='0.2.0',
)
