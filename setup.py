#!/usr/bin/env python

import os
from setuptools import setup
from django_extra_referrals import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-extra-referrals',
    version=__version__,
    description='Django referral with multilevel fee system',
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer='Rizki Sasri Dwitama',
    maintainer_email='sasri.project@gmail.com',
    license="MIT",
    url='https://github.com/sasriawesome/django_extra_referrals',
    packages=[
        'django_extra_referrals',
        'django_extra_referrals.migrations',
        'django_extra_referrals.utils',
    ],
    install_requires=[
        "django>=2.2",
        "django-numerators>=0.0.1",
        "django-polymorphic>=2.1.2",
        "django-mptt>=0.11.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    tes_suite="tests.run_tests.run_tests"
)
