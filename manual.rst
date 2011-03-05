..    project.rst
..
..    Copyright (c) 2010, 2011 Patricio Paez <pp@pp.com.mx>
..
..    This program is free software; you can redistribute it and/or modify
..    it under the terms of the GNU General Public License as published by
..    the Free Software Foundation; either version 2 of the License, or
..    (at your option) any later version.
..
..    This program is distributed in the hope that it will be useful,
..    but WITHOUT ANY WARRANTY; without even the implied warranty of
..    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
..    GNU General Public License for more details.
..
..    You should have received a copy of the GNU General Public License
..    along with this program.  If not, see <http://www.gnu.org/licenses/>

arithmetic
================================================

*arithmetic* is a Python module that allows mixing arithmetic
operations and text.
Sample Tk, GTK and wxWidgets based sample editors that use the module
are provided as a starting point.  A plugin for Zim and a patch for PyRoom
editors.
Tutorial documents are included, they will quickly show
all the features of arithmetic.
It is licensed under the Gnu GPL license version 2 or later.


The project is available at http://pp.com.mx/python/arithmetic

.. Contents::
   :depth: 1


Download
~~~~~~~~

Download the latest arithmetic-<version>.tar.gz file::

 $ wget http://pp.com.mx/python/arithmetic/arithmetic-<version>.tar.gz

Extract the contents::

 $ tar xf arithmetic-<version>.tar.gz 

Enter the folder arithmetic-<version> that was created::

 $ cd arithmetic-<version>


Tutorials
~~~~~~~~~

Open the *tutorial-1* and *tutorial-2* files with editor-tk.py,
the editor application included with the module.
There is no need to install the module, editor-tk.py runs
as is from the source directory.  In GNU/Linux, execute
the following commands in the source directory::

 ./editor-tk.py tutorial-1
 ./editor-tk.py tutorial-2


In Windows, explore the source directory and drag
each tutorial file over the *editor-tk.py* icon.


Requirements
~~~~~~~~~~~~

Tkinter is required to run the editor-tk.py sample editor. you might need to install
package python-tk in GNU/Linux. Tkinter is automatically installed in Windows.


Installation
~~~~~~~~~~~~

To install the module, execute as root from the source directory:: 
 
 # python setup.py install



.. |date| date::
.. |time| date:: %H:%M

Document generated on |date| at |time| CST.

