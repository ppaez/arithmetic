has_setuptools = False
try:
	from setuptools import setup, Extension
	has_setuptools = True
except ImportError:
	from distutils.core import setup, Extension

import sys,os,string,time

version = '0.4'

kwargs = dict()
if has_setuptools:
	kwargs = dict(
			include_package_data = True,
			install_requires = ['setuptools'],
			zip_safe = False)

setup(
	#-- Package description
	name = 'arithmetic',
	version = version,
	description = 'Arithmetic module',
	author = 'Patricio Paez',
	author_email = 'pp@pp.com.mx',
	url = 'http://pp.com.mx/python/arithmetic/',
	license = 'GNU GPL v2 or later',
	py_modules = [ 'arithmetic' ],
	data_files = [ ( 'share/arithmetic-' + version, [ 'COPYING',
		'CHANGELOG', 'README', 'tutorial-1', 'tutorial-2' ] ) ],
	scripts = [ 'libreta.py', 'arithmetic' ],
	platforms = ['any'],
	long_description='''arithmetic is a Python module that allows mixing arithmetic
operations and text.  It resembles the calculator program bc.

A sample Tk-based editor that uses the module is provided as
a starting point.

Tutorial documents are included, they will quickly show
all the features of arithmetic.''',
	classifiers=[ "Development Status :: 3 - Alpha",
		"Topic :: Text Processing" ],
)
