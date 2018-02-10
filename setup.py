has_setuptools = False
try:
	from setuptools import setup, Extension
	has_setuptools = True
except ImportError:
	from distutils.core import setup, Extension

import sys,os,string,time

version = '0.6.1'

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
	data_files = [('share/arithmetic-' + version,
                       [ 'COPYING',
		         'CHANGELOG', 'README',
                         'tutorial-1', 'tutorial-2',
                         'pyroom-0.4.1-arithmetic.patch', 'calc.py',
                         'manual.rst', 'manual.html']),
                       ('share/arithmetic-' + version + '/vim-plugin',
                         ['vim-plugin/arithmetic.vim',
                         'vim-plugin/wrapper.py',
                         'vim-plugin/install.sh',
                         'vim-plugin/tutorial.txt',
                         'vim-plugin/arithmetic.txt']),
        ],
	scripts = [ 'editor-tk.py', 'arithmetic', 'editor-gtk.py',
                    'editor.ui', 'editor-wx.py' ],
	platforms = ['any'],
	long_description='''arithmetic is a Python module that allows mixing arithmetic
operations and text.  It resembles the calculator program bc.

Tk, GTK and wxWidgets based sample editors that use the module
are provided as a starting point.  A plugin for Vim, a plugin ford Zim,
and a patch for the PyRoom editors are included.

Tutorial documents are included, they will quickly show
all the features of arithmetic.''',
	classifiers=[ "Development Status :: 3 - Alpha",
		      "Topic :: Text Processing",
                      "Programming Language :: Python :: 2",
                      "Programming Language :: Python :: 3"
        ],
)
