=======================
Building the Controller
=======================

My notes here are likely to be a little haphazard since I will be building some of the parts of the application
controller, the parts I know how to do, as I develop the user interface and save other parts for when my practicing
with the program suggests that I need something.

Keeping Track of the Program Mode
---------------------------------

As it stands now, I have completed at least the first draft of the main window's menu bar and the next thing on my mind
is to set up a system to disable/enable different menu entries according to the different states the program will be in.
Here is my original idea of the different modes:

A. Program just loaded, no game open - neutral mode
#. Game open for creation or editing - neutral mode
#. Game being played - playing mode

After working on the program for a while I decided on a different set of modes:

A. No game loaded - Empty mode
#. Game loaded but neither editing nor playing - Neutral mode
#. Game loaded and being edited - Editing mode
#. Game loaded and being played - Playing mode

Here is a table showing which menu items are to be enabled in each mode:

+---------------------+---------+---------+---------+---------+
| Menu Item           | Empty   | Neutral | Editing | Playing |
+=====================+=========+=========+=========+=========+
| file_open           | X       | X       | X       |         |
+---------------------+---------+---------+---------+---------+
| file_create         | X       | X       | X       |         |
+---------------------+---------+---------+---------+---------+
| file_close          |         | X       | X       |         |
+---------------------+---------+---------+---------+---------+
| file_save           |         | X       | X       |         |
+---------------------+---------+---------+---------+---------+
| file_save_as        |         | X       | X       |         |
+---------------------+---------+---------+---------+---------+
| file_print          |         | X       | X       |         |
+---------------------+---------+---------+---------+---------+
| file_exit           | X       | X       | X       | X       |
+---------------------+---------+---------+---------+---------+
| edit_modifyMenu     |         | X       | X       |         |
+---------------------+---------+---------+---------+---------+
| edit_cut            |         |         | X       |         |
+---------------------+---------+---------+---------+---------+
| edit_copy           |         |         | X       |         |
+---------------------+---------+---------+---------+---------+
| edit_paste          |         |         | X*      |         |
+---------------------+---------+---------+---------+---------+
| game_names          | X       | X       |         | X       |
+---------------------+---------+---------+---------+---------+
| game_practice       | X       | X       |         | X       |
+---------------------+---------+---------+---------+---------+
| game_playMenu       | X       | X*      |         | X       |
+---------------------+---------+---------+---------+---------+
| game_correct_scores |         |         |         | X       |
+---------------------+---------+---------+---------+---------+
| game_end            |         |         |         | X       |
+---------------------+---------+---------+---------+---------+
| game_settings       | X^      | X^      | X^      | X^      |
+---------------------+---------+---------+---------+---------+
| help_using_program  | X       | X       | X       | X       |
+---------------------+---------+---------+---------+---------+
| help_rules          | X       | X       | X       | X       |
+---------------------+---------+---------+---------+---------+
| help_about          | X       | X       | X       | X       |
+---------------------+---------+---------+---------+---------+

* only available if the game loaded is marked as playable.

** should only be available in ProgramMode.Editing when there is text on the clipboard.

^ whether this is available in all modes depends on if I decide it is set for the program or for the game

But a question has been raised in my mind. How is the program to know, when the user loads a game, whether the user
wants to edit the game or play the game? One possibility is to presume editing is desired until the user clicks the
"Play Jeopardy!" entry. I could use the edit-modify menu entry to allow for editing during a played game. It would have
to check to see if a game was in progress and suspend it, somehow stopping its timers, as well as activating the items
in edit mode, until the user clicks game-play again (now labelled something like "Return to the Game").

After working on the program for a while I decided that it might be better to have

That all suggests a new method in the Jeopardy class: setProgramMode(state=neutral, editing or playing) and a new enum
to go with it::

    class ProgramMode(Enum):
        Neutral = 1
        Editing = 2
        Playing = 3

Since a couple of the menu entries should only be enabled if a playable game is present I rigged up the ``file_open``
method to read in my ``temp_saved_game`` in the ``src`` directory in order to test whether that happens or not.

Creating self.game_pathname
---------------------------

That did work but while working on it another thought came to my mind about the ``file_open`` method. It will somehow
(either from a file dialog box or from a custom made game selection box of my own) be given a pathname to open. I
suspect it will be good to save that pathname for later saving. I created a ``self.game_pathname`` just in case.

Playing the Game(s)
-------------------

The leader will have to be able to select which game to play: Jeopardy, Double Jeopardy or Final Jeopardy during the
game. That suggests that, under the Game menu there should be a "Play" entry with sub-menus for each of the three
options. Now... how do I do sub-menus?

According to the documentation at http://doc.qt.io/qt-5/qmenu.html#details I should be able to use Menu.addMenu() to add
a sub-menu. Let me try that...

That worked quite well and, in the process of implementing it I realized I would have to do the same thing for editing.
A game can only be edited or played, of course, if it has been loaded in memory so both the ``file_open`` and
``file_create`` methods will have to set a ``self.game_loaded`` variable to ``True``. It will start out ``False``
and return to false in the ``file_close`` method. (It seems that ``file_close`` should also set the program back to
``ProgramMode.Neutral``. I will implement all of that now.

(Continue this later)

A Massive Refactor
==================

I was floundering around trying to figure out how mousePressEvents from the DisplayUnits could get back up to the
Board. But I found I have been drifting away from the MVC model. Currently the DisplayUnits effectively have to know
whether they are category units or clue units. That would seem to be the job of the controller. Meanwhile, the Board
class is a QGraphicsItem but it is never added to the scene and I'm not sure what purpose it is supposed to serve. It
seems to be another controller.

I'm going to try this:

#. Create a StageSet class that inherits from QGraphicsScene to contain all of the elements of the game

#. Call the QGraphicsScene stageSet. It will contain the board, scoreboards, lights, timers, etc.

#. Make the DisplayUnits dumber. Let the controller set their fonts, text, positions, types and what they display.

#. Give the DisplayUnits a reference to the controller so they can tell the controller the events of their lives.



