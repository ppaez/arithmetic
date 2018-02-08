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
Tk, GTK and wxWidgets based sample editors that use the module
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


Requirements
~~~~~~~~~~~~

The *arithmetic* module uses only modules from the standard
Python library, no additional modules are required.

The sample
editors that are included require the Python bindings to the
graphical toolkit they use.  The following table shows which
package is required in each case:

==============  ===============   ===========
Editor          Package           Python
                                  bindings
==============  ===============   ===========
editor-tk.py    python-tk         Tkinter
--------------  ---------------   -----------
editor-gtk.py   python-gtk2       gtk
--------------  ---------------   -----------
editor-wx.py    python-wxgtk2.8   wx
==============  ===============   ===========

Package **python-tk** might need to be installed in GNU/Linux, it is automatically
installed with Python in Windows.
Packages **python-wxgtk2.8** (or *python-wxgtk2.6*) and **python-gtk2** are
normally installed in Ubuntu Linux.


Tutorials
~~~~~~~~~

There is no need to install the module in your system, if you
just want to try the module first.  Change into the source
directory before doing the following commands.  The simplest
demo is using a text file as input, the output is sent to the
standard output::

 ./arithmetic -f tutorial-1

A graphical demo of using the module in a text editor is made
using te sample editors. Open the *tutorial-1* and *tutorial-2* files
with one of the editor applications, for example in GNU/Linux, execute
the following commands in the source directory.  Using Tk::

 ./editor-tk.py tutorial-1
 ./editor-tk.py tutorial-2

Using GTK::

 ./editor-gtk.py tutorial-1
 ./editor-gtk.py tutorial-2


Using wxWidgets::

 ./editor-tk.py tutorial-1
 ./editor-tk.py tutorial-2

In Windows, explore the source directory and drag
each tutorial file over one of the *editor-\*.py* icons.

Installation
~~~~~~~~~~~~

To install the module, execute as root from the source directory::

 # python setup.py install

To install into your home directory (root user
is not required)::

 # python setup.py install --home=~

To install the Vim plugin::

 # vim-plugin/install.sh


Use in existing graphical applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using arithmetic in an existing, Python-based GUI application
involves adding a *calculate* function to the application
and bind a key combination to call that function.
These are the steps in more detail:

1. Identify the text buffer used.  This is usually an instance
of a text widget in the graphical toolkit and can be determined
by looking at the source code.  The name of the text widget
varies on each toolkit.  The table below shows the text
buffer class name for each toolkit.

2. Add a binding to the *calculate* routine.  This is done
differently on each toolkit.  In some you can bind directly
to F5 for example, other toolkits any key press is bound
and you have to check for F5.

3. Add a *calculate* routine that will receive an event or
a reference to the text buffer.  This routine instanciates
the Parser* class for the specific toolkit and calls the
parse method that does all the work.  It scans the buffer
line by line and writes back results if needed.

4. Add an import statement at the begining of the
source file where *calculate* is located, to import the
appropriate class for the toolkit.

================   ================ =======================
Toolkit              Widget         Class in arithmetic
================   ================ =======================
Tk                 tkinter.Text     ParserTk
----------------   ---------------- -----------------------
GTK                gtk.TextBuffer   ParserGTK
                   (displayed
                   inside a
                   gtk.TextView
                   widget)
----------------   ---------------- -----------------------
wxWindows          wx.TextCtrl      ParserWx
================   ================ =======================

Tk-based applications
---------------------

Look at editor-tk.py for full detail.
The key commmands that need to be added::

 from arithmetic import ParserTk

 TextWidget.bind( '<F5>', calculate )

 def calculate( event ):
     parser = ParserTk()
     parser.parse( event.widget )

GTK-based applications
----------------------

Look at editor-gtk.py for full detail.
Commmands that need to be added::

 from arithmetic import ParserGTK

 def on_window1_key_press_event(self, widget, event, \*args ):
     if event.keyval == gtk.keysyms.F5:
         buf = self.textview.get_buffer()
         self.calculate(buf)

 def calculate( buf ):
     parser = ParserGTK()
     parser.parse( buf )

wxWidgets-based applications
----------------------------

Look at editor-wx.py for full detail.
Commmands that need to be added::

 from arithmetic import ParserWx

 self.control.Bind( wx.EVT_KEY_DOWN, calculate)

 def calculate(event):
     if event.GetKeyCode() == wx.WXK_F5:
         control = event.GetEventObject()
         parser = ParserWx()
         parser.parse( control )
     event.Skip()


Adding the plugin to Zim
~~~~~~~~~~~~~~~~~~~~~~~~

If you have Zim installed in your system, copy the **calc.py** file
to */usr/local/lib/python2.6/dist-packages/zim/plugins*.  The 2.6 in
this path might vary depending of the Python version::

 su -c 'cp calc.py /usr/local/lib/python2.6/dist-packages/zim/plugins'

If you just want to try Zim and arithmetic without installing any of
them, download both sources to a folder, uncompress them, change into
the zim-0.xx directory, copy the *calc.py* file into the zim/plugins
path, and run this command::

 PYTHONPATH=../arithmetic ./zim.py

This will run Zim and tell the Python intepreter to find arithmetic in
that path instead of the default path for installed packages.  In Zim
use menu *Edit, Preferences*, then select the *Plugins* tab, look for
for the Arithmetic entry and click on it.  Check in the dependencies that
it says *arithmetic - OK*, then click on the checkbox in the *Enabled*
column to enable it.  Click on OK to close the Preferences window.  Use
menu *Tools* and verify that *Arithmetic  F5* is displayed.  You can now
write arithmetic expressions ending in a '=', then press <F5> to
obtain the results.

Applying the patch to PyRoom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have PyRoom installed in your system, do the following commands
in a shell::

  cd /usr/local/lib/python2.6/dist-packages/PyRoom
  su -c 'patch -p1 pyroom-0.4.1-arithmetic.patch'

If you want to try PyRoom and arithmetic without installing them,
download both sources into a folder. uncompress them, change into
the pyroom folder and run the following command::

 PYTHONPATH=../arithmetic ./pyroom

This runs PyRoom telling the Python interpreter to find arithmetic
in that path instead of the default path for installed packages.
Once in PyRoom, you may use *Control-T* to obtain the results from
calculations written in one of the buffers.

How it works
~~~~~~~~~~~~

The input is a text buffer which might contain one or more
interspersed arithmetic expressions.  This buffer is scanned
line by line from top to bottom, and each line is scanned left
to right.  For each equal sign that is found, the text to the
left and to the right sides of the equals sign is parsed to
determine if it is an expression, an identifier, or empty. Based
on both sides, one of these actions is carried out:

* Evaluate an expression on the left side, write the result
  on the right side. For example:  *2 + 3 =*
* Evaluate an expression on the right side, store the result
  on the name on the left side.  For example:  width = 45
* Store the formula for a function in the right side in the
  formula name on the left side.  For example:  *area = width x height*.
* Evaluate the value of a function on the left side, write the
  result on the right side.  Like *area =*.

Class *Parser* is the starting point. Its method *parse* accepts
a string representing a single or multiple line buffer, and
iterates through its lines. *parse* uses method *countLines* to
know how many lines are in the text buffer, then repeateadly
calls *readLine* to get a line and *parseLine* to scan it and
modify it if needed. *parse* returns the input string, modified
if any calculations where done.

*parseLine* finds the equal signs and their left and right sides
and determines what action to take.  Function *TypeAndValueOf*
is used to know what is on each side (name, expression, etc.)
*evaluate*, an expression parser, is used to get results of
expressions, which may include variable or function names.  It
uses *WriteResults* to modify a part of the line to write or
update the result of an expression.

*evaluate* uses class Lexer, a lexical analyzer, and accepts
'x' for multiplication and n%, converting it to n/100.

The *Parser* base class is used mostly for testing.
Classes *ParserTk, ParserGTK* and *ParserWx* are derived from Parser
and overwrite the *countLines, readLine* and *WriteResults*
methods to include toolkit-specific commands.  These are the ones
to be used for GUI applications.

The names and values of variables found by parseLine are stored
in the *variables* dictionary, the names and formulas of
functions are stored in the *functions* dictionary.  These
entries are read by evaluate when needed.  Both dictionaries
are initialized when the Parser* instance is created.


.. |date| date::
.. |time| date:: %H:%M

Document generated on |date| at |time| CST.
