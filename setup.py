# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import pyduino

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)

        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

requires = open('requirements.txt').read().strip().split('\n')
test_requires = requires + open('requirements-dev.txt').read().strip().split('\n')

setup(
    name = "pyduino",
    version = pyduino.__version__,
    author = "pyDuino Team dev"
    author_email = "support@mon-club-elec.fr"
    packages = find_packages(),
    description = "Allow to work with pins of a pcDuino.",
    long_description = open('README.md').read(),
    install_requires = requires,
    include_package_data = True,
    url = "https://github.com/Poztit/pyDuino",
    classifiers = [
        "Programming Language :: Python",
        "Natural Language :: French",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    licence = "GPLv3",
    cmdclass = {"test": PyTest},
    tests_require = test_requires
)
