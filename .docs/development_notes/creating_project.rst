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

.. _installing_sphinx:

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

Cloning the Project to South Haven
==================================

I documented my process fairly carefully this time for future reference.

New Versions
------------

PyCharm needed to be updated to version 2018.2.1.

The PyCharm plugin ``.ignore`` also wanted to be updated so I did.

Then I went to ``python.org`` and downloaded Python 3.7. The options I selected were to "Install Launcher for all Users"
and "Add Python37 to PATH." I selected "Install Now" rather than the custom configuration. This installed Python 3.7 at:

``C:/Users/frjam_000/AppData/Local/Programs/Python/Python37``

Creating the Environment
------------------------

PyCharm started up in the last program I was working on, confirmation2018. To create the ``jprd`` environment using
Python 3.7 I performed the following steps.

#. Went to File->Settings->Project Interpreter->Gear->Add...
#. Left New Environment checked
#. Set the location to ``C:\Users\frjam_000\Envs\jprd``
#. Selected the base interpreter as ``C:/Users/frjam_000/AppData/Local/Programs/Python/Python37``
#. Clicked Ok.
#. Back in the main dialog I restored confirmation2018's setting to ``Python 3.6 (conf)(1)``

Installing PyQt5 and Sphinx
---------------------------

In PyCharm's terminal::

    workon jprd
    pip install pyqt5
    pip install sphinx

It gave me the usual warning it's been giving lately:

    ``You are using pip version 10.0.1, however version 18.0 is available...``

and I ignored it. It does look like there is a version 18.0, they are using a calendar versioning system now,
(see https://calver.org) but I haven't been able to get it to install on other machines and haven't tried on this one.
Maybe it's because version 18.0 and version 10.0.1 are really the same version. This isn't really  a problem, so I'll
deal with it later.

Cloning the Jeopardy Project
----------------------------

In PyCharm:

    VCS->Git->Clone...

I copy/pasted ``https://github/JMorris/Jeopardy`` into the URL edit box.
I changed the directory to:

``C:\Users\frjam_000\Documents\PyCharm Projects\JeopardyProject``

and clicked the Clone button.

I said "Yes" when it asked if I wanted to open that directory and opened it in a new window.

Configuration in PyCharm
------------------------

It works out to be best to go to File->Settings->Project Interpreter in order to add a new configuration. Once there I
clicked on the interpreter drop-down and selected "Show all..."

From there I clicked on the "+" button, checked "Existing Environment", clicked on the "..." button and navigated to
the ``python.exe`` file in the environment:

``C:\Users\frjam_000\Envs\jprd\Scripts\python.exe``

I clicked "Ok" and, back in the Settings dialog I clicked on Project Structure in order to select the ``src`` directory
to be for Sources.

When I clicked "Ok" again, and waited for two processes to complete, I clicked on the "Add Configuration..." button
to the left of the Run button in the toolbar. Clicked on its "+" button, named the configuration "Jeopardy" and
selected ``jeopardy.py`` in the Script Path box.

When I pressed the Run button to test the program it worked!

Setting up Sphinx
-----------------

I tried to do a ``sphinx-quickstart`` but it refused to let me since I already had a ``conf.py`` file available. All I
really had to do to prevent warning messages is to add an empty directory to the ``.docs`` folder called ``_static``. It
didn't warn me about it but, after reading the :ref:`above <installing_sphinx>` I added an empty ``_templates``
directory too.



