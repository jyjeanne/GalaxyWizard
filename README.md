#### GalaxyWizard: an open-source tactical RPG made with python.

contributors :
 - Jeremy Jeanne <jyjeanne@gmail.com> and

#### INSTALLATION

**GalaxyWizard** is written in Python, so you'll need a **Python version 3** interpreter
to get anything working and install **poetry**, see https://python-poetry.org. It also depends on several Python modules;
see the DEPENDENCIES section below if you have any problems.  If you
do have all the dependencies, you should be able to run the current
demo just by running the main into main.py GalaxyMage script with a Python
interpreter. From a shell, the following command should do the trick:

We use poetry to manage dependencies : 

 - To install the dependencies run command : **poetry install** 

 - To run locally use command : **poetry run python src/main.py**

 - For building the executable, use:

 - Windows: **poetry run pyinstaller --onefile --windowed src/main.py** 

 - Linux: **poetry run pyinstaller --onefile src/main.py**

Users of graphical file managers can probably double-click the
GalaxyWizard.exe  to achieve the same effect.

#### DEPENDENCIES

You'll need a Python interpreter for your platform. See
http://www.python.org for more details. GalaxyWizard is officially
developed for Python version 3.

In addition to the standard Python distribution, you'll also need the
following Python libraries:

* Numeric

* PyOpenGL

* PyGame

* Twisted

* pyinstaller


#### PLAYING THE GAME

See the file doc/controls.txt for a quick primer on the game
controls. Run GalaxyWizard with the -h option for help with command-line
options:

**$ python src/main.py -h**


#### LICENSE

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

The data files used by GalaxyWizard (all under the directory src/assets) are
copyright their individual authors. These files are redistributed with
their authors' permission, typically under a Creative Commons or GPL
license. To see the licensing terms for each of these files.