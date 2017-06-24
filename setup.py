from os.path import join, dirname
from setuptools import setup

package_name = "shoogie"
base_dir = dirname(__file__)

def read(filename):
    f = open(join(base_dir, filename))
    return f.read()

def get_version(package_name, default='0.1'):
    try:
        f = open(join(base_dir, package_name, '__init__.py'))
    except IOError:
        try:
            f = open(join(base_dir, package_name + '.py'))
        except IOError:
            return default
    scope = {}
    exec f in scope
    return scope.get('__version__', default)

setup(
    name = "django-shoogie",
    version = get_version(package_name),
    description = "Log server errors to database",
    long_description = read("README.rst"),
    author = "Aryeh Leib Taurog",
    author_email = "python@aryehleib.com",
    license = 'MIT',
    url = "http://bitbucket.org/altaurog/django-shoogie",
    packages = [package_name],
    install_requires = ["django>=1.3"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Logging",
        "Topic :: Database",
        "Framework :: Django",
    ],
)
