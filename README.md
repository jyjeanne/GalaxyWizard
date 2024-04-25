GalaxyWizard: an open-source tactical RPG made with python.

Copyright (C) 2024 Jeremy Jeanne <jyjeanne@gmail.com> and
contributors. 

INSTALLATION

GalaxyWizard is written in Python, so you'll need a Python interpreter
to get anything working. It also depends on several Python modules;
see the DEPENDENCIES section below if you have any problems.  If you
do have all the dependencies, you should be able to run the current
demo just by running the main GalaxyMage script with a Python
interpreter. From a shell, the following command should do the trick:

We use poetry to depency : 

poetry install

poeatry run 

$ python GalaxyWizard.py

Users of graphical file managers can probably double-click the
GalaxyWizard script to achieve the same effect.


DEPENDENCIES

You'll need a Python interpreter for your platform. See
http://www.python.org for more details. GalaxyWizard is officially
developed for Python version 3 .

In addition to the standard Python distribution, you'll also need the
following Python libraries:

* Numeric
 

* PyOpenGL
 

* PyGame
  

* Twisted

* pyinstaller
 

If you are using a Unix-like operating system, the easiest way to
install these dependencies is probably through your package management
system. On Debian GNU/Linux (or derivatives such as Ubuntu), these are
the names of the packages you'll need:

python python-numeric python-opengl python-pygame python-twisted

Using an old version of PyOpenGL might cause GalaxyWizard to crash, with
the following error message: "(pygame parachute) Segmentation
Fault". If you experience this error, please update to a more recent
version of PyOpenGL.

For Windows users, you can download the needed packages directly at
the following links (up-to-date as of 2005-Nov-26):


OPTIONAL PACKAGE: PSYCO

If you have the "psyco" just-in-time Python compiler, GalaxyWizard will
auto-detect it, and use it to speed up execution.  If you don't have
psyco, no problem -- GalaxyWizard will still work correctly.  It'll just
run a bit more slowly.

To install psyco in Linux, get a package with a name like
"python-psyco".

PLAYING THE GAME

See the file doc/controls.txt for a quick primer on the game
controls. Run GalaxyWizard with the -h option for help with command-line
options:

$ python GalaxyWizard.py -h


LICENSE

The GalaxyWizard source code is copyright (C) 2024 Jeremy Jeanne.

GalaxyWizard is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

GalaxyWizard is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with GalaxyWizard; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


The data files used by GalaxyWizard (all under the directory data/) are
copyright their individual authors. These files are redistributed with
their authors' permission, typically under a Creative Commons or GPL
license. To see the licensing terms for each of these files.