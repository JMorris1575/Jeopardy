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

Editing Jeopardy Games - A Narrative Run-Through
================================================

Jim has finally finished the part of the Jeopardy program that allows for creating and editing games. He fires up the
program and clicks on File->Create... and a dialog appears with a form for filling out the game information:

#. Name

#. Topic

#. Target Group

#. Default Settings:

    A. Time allowed for players to respond

    #. Scoring Method (Dollars or Points)

    #. Base Amount (Lowest value square (all others based on it)

Having a name is mandatory as it will be transformed into a filename, and the resulting filename must be unique for the
set of game files on the local system. (If I have time I can make "catalogs" of games, subfolders within the main
program's game folder.)

The rest of the items are optional but helpful for the listing of games that will be given when File->Open... is
clicked.

The default Default Settings I have in mind right now are 5 seconds for the time allowed for players to respond and
Dollars for the scorekeeping method. (That one doesn't really matter since we're NOT giving away money!) The default
Base Amount will be 200.

Once he fills that out the board shifts into edit mode as indicated by the dark grey, rather than black, background. The
board is ready for Jeopardy categories and clues as indicated by an image of the Jeopardy cover card to the left of the
main board. Jim enters categories and clues into the game in one of the following two ways:

|

+--------------------------------------------------------------------------------------------------------------------+
| **The Easy Way**                                                                                                   |
+====================================================================================================================+
| When Jim clicks on a category square a dialog opens where he can enter the category and an optional explanation    |
| for that category. When Jim clicks on a clue square a dialog opens which allows him to enter the clue and its      |
| correct response. In either case, as text is entered into the edit boxes it also appears on a "screen" as it would |
| appear during the game.                                                                                            |
+--------------------------------------------------------------------------------------------------------------------+

|

+--------------------------------------------------------------------------------------------------------------------+
| **The Dream Way**                                                                                                  |
+====================================================================================================================+
| When Jim clicks on a category square that square enters into edit mode and Jim types the category name into the    |
| square. If he wants to enter an explanation for that category he can double-click the square. When Jim clicks on a |
| clue square it allows him to enter the clue and the correct response in the same way.                              |
+--------------------------------------------------------------------------------------------------------------------+

|

Jim can correct his entries simply by clicking on a box again and either the filled-out dialog for that box, or the box
itself will appear according to whether I do it the easy way or can figure out how to do it the dream way.

Jim can click on Edit->Modify to enter or edit categories and clues for Double Jeopardy and Final Jeopardy.

After each entry the game is checked for completeness. If it is complete it is marked as playable and will appear in
the File->Open... dialog box.

Implementing the Editing Process
================================

I will start out with the "Easy Way" described above and, to keep the "views" and the "controller" separate, will create
a new file: ``dialogs.py`` to contain all of the dialog boxes I build.

Here is a quick plan for implementation, kind of Test-Driven-Development like:

#. Write a call to check whether a game in memory has changed in file_create

#. Write the routine to chec whether a game in memory has changed

#. Once saving things as appropriate create a new Game() and enter the info dialog box.

#. Create the info dialog box.

#. Wire up file_save_as to save a file.

#. Wire up file_save to check if file_save_as is more appropriate and then save the file.

That should be enough for now.

Deciding the Next Step
======================

I've got the program working to the point that I can enter and save puzzles, though it only opens and saves the same
temporary file: ``../Games/temp_game.jqz``. I can rename it later when I decide how I want the File->Open... process to
work.

My question now is what to do next. There are several options:

#. Improve the simple input dialog boxes I have now.
#. Design and build the scoreboards and wire them to work.
#. Decide on how I want the File->Open... process to work and make it so.
#. Work on the game playing portion of the program -- at least in the version that doesn't require the switches.
#. Work on the timing lights.
#. Make better graphics for the cover cards and make a graphic for the Daily Double card.
#. Study how to implement a Help system.
#. Work on a keyboard navigation system for the board to replace the mouse if so desired while editing or playing.
#. Work on listing and allowing the user to change the game settings.
#. Study how the leader notes can be printed and make it happen.
#. Work on a splash screen and it's display at the beginning of the program.
#. Work on Help->About -- perhaps using the splash screen with an OK button.
#. Work on right-clicking to display the secondary text of a DisplayUnit.
#. Work on expanding a DisplayUnit when clicked during a game.
#. Work on simulating a TV camera view by scaling and moving the scene or changing the viewport somehow.

Working on the Game Playing Portion of the Program
==================================================

Working on the game playing portion of the program will take care of many of the other items in the list above so I will
do that. Based on how the game is played here is a possible order in which to tackle each item:

#. Sequence of events to reveal categories
#. Reveal a requested clue
#. Activate the buttons, if available, and start the group response timer
#. If the group response timer times out, pause for a bit and then reveal the correct response
#. If a player responds
    A. start the individual response timer
    #. if the individual response timer times out before they have given an answer subtract the points
    #. if the player responds and is right
        i. show the correct response
        #. add the score for that question to that player's score
        #. give that player "control of the board"
    #. If a player responds and is wrong
        i. subtract the score for that question from that player's score
        #. deactivate their button
        #. activate the other two buttons
        #. start the group response timer again
#. Completed clues are left blank

