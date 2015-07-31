from setuptools import setup, find_packages

import pyduino

requires = open('requirements.txt').read().strip().split('\n')

setup(
    name='pyduino',
    version=pyduino.__version__,
    packages=find_packages(),
    description='Allow to work with pins of a pcDuino.',
    long_description=open('README.md').read(),
    install_requires=requires,
    include_package_data=True,
    url='http://www.mon-club-elec.fr/pmwiki_reference_pyduino/pmwiki.php',
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: French',
        'Programming Language :: Python :: 2.7'
    ],
    licence='GPLv3'
)
