from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='secsgem',

    version='0.0.2',

    description='Python SECS/GEM implementation',
    long_description=long_description,

    url='https://github.com/bparzella/secsgem',

    author='Benjamin Parzella',
    author_email='bparzella@gmail.com',

    license='LGPL',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='development hsms secs gem',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
)