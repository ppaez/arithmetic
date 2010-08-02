has_setuptools = False
try:
	from setuptools import setup, Extension
	has_setuptools = True
except ImportError:
	from distutils.core import setup, Extension

import sys,os,string,time

version = '0.1'

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
	py_modules = [ 'arithmetic' ],
        data_files = [ ( '', [ 'COPYING', 'CHANGELOG' ] ) ],
        scripts = [ 'libreta.py' ],
)
