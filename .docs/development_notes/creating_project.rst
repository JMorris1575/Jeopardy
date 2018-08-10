=============================
Creating the Jeopardy Project
=============================

I wanted to use the latest version of Python (version 3.7) and PyQt5 along with the PyQt Designer program (which I may
not use anyway).

Original Creation
=================

I started this project on my Windows 7 laptop while on vacation. Here is how it worked out on that machine.

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

Creating the Project in Kalamazoo
=================================

I used the Version Control System (VCS) through PyCharm to set up, commit and push the project files to github. I
originally forgot to include the files in ``.docs/development_notes`` but they were easy to add later.

Here is what happened when I started working on the project on my Kalamazoo Windows 10 computer.

Cloning the Project
-------------------

From within PyCharm I selected ``VCS->Git->Clone...`` and named the project Jeopardy. Then I had to install Python 3.7
and prepare the virtual environment.

Installing Python 3.7
---------------------

On the Windows 10 machine, selecting the option to install "for anyone" ended up installing it in:
``C:\Users\frjam\AppData\Local\Programs\Python\Python37`` which is not what I expected but it seems to work. Also I
elected to have it added to the PATH.

Installing PyQt5
----------------

Doing ``pip install pyqt5`` worked as expected but there were problems later. :ref:`See below.<pycharm_problems>`

I got the warning, again, about using an outdated versin of pip (version 10) and recommendation to install pip version
18 but, again, following the instructions led to errors. It must be some kind of mistake, though. Would they jump up to
version 18 already?

Installing Sphinx
-----------------

This also worked as expected but, since I hadn't done a ``sphinx-quickstart`` I didn't have a ``_static`` directory and
it warned me about that when I did a ``make html``

The second time around, :ref:`(See below)<pycharm_problems>`, I did the ``sphinx-quickstart`` but apparently from the
``Jeopardy`` directory and not the ``.docs`` directory. It put three empty directories: ``_build, _static,`` and
``_templates`` into the ``Jeopardy`` directory and ``make html`` complained about it. I moved them and all seems well.

.. _pycharm_problems:

PyCharm Problems
----------------

Once I got it all hooked up, that is, got the PyCharm configuration all done up properly, the program worked but all of
the references to PyQt5 classes where highlighted with wavy red underlines. It wasn't able to find them. Eventually I
was able to fix it by deleting the entire ``C:\Users\frjam\Documents\PyCharmProjects\Jeopardy`` folder and cloning it
again.

This time I ended up cloning it as PyCharm opened since it couldn't find the files it was expecting. I opted not to open
the resulting folder right away and, when I tried to open it next noticed it was not marked as a PyCharm project. When
it noticed I was trying to open a directory with files in it, it asked if I wanted to use them in the project. I did.

I don't know why or how but it all seems to be working now: the program works, and the ugly red highlights are gone.

