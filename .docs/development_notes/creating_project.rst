Creating the Jeopardy Project
=============================

I wanted to use the latest version of Python (version 3.7) and PyQt5 along with the PyQt Designer program (which I may
not use anyway).

Installing Python 3.7
---------------------

Simply downloading the installation file and taking care to install "for anyone" and adding it to the path installed it
to ``c:/users/Jim/Program Files/Python37`` which is what I wanted.

Creating the JeopardyProject with PyCharm
-----------------------------------------

Closing the existing project brought me to a dialog which included the choice to create a new project. I did that and
gave it the name "JeopardyProject". I didn't notice, at first, but it automatically created a virtual environment named
"JeopardyProject" in my ``Envs`` directory. This is not what I wanted. There's a little grey arrow that expands the
virtual environment dialog where you can change the name. I used ``jprd``.

Installing PyQt5
----------------

``pip install pyqt5`` worked perfectly well for this but it complained that I was using an old version of pip. It took a
while to figure out how to pip install the new version. The command it suggested:

``python -m pip install --upgrade pip``

returned errors. I finally fixed it by using that command in a command prompt OUTSIDE the ``jprd`` virtual environment,
using that command WITHIN the virtual environment and then deleting the egg directory that contained the old version
that was still being used. If these instructions are vague it's because they are coming from a memory that is also
vague. I still hope it will prove useful.

Installing Sphinx
-----------------

``pip install sphinx`` worked perfectly as did ``sphinx-quickstart``. I'm trying to keep these notes in a separate
directory from the help system but I don't know how that will work out with the make program just yet.


