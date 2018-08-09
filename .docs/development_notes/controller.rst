=======================
Building the Controller
=======================

My notes here are likely to be a little haphazard since I will be building some of the parts of the application
controller, the parts I know how to do, as I develop the user interface and save other parts for when my practicing
with the program suggests that I need something.

As it stands now, I have completed at least the first draft of the main window's menu bar and the next thing on my mind
is to set up a system to disable/enable different menu entries according to the different states the program will be in.
Here is my idea of the different modes:

A. Program just loaded, no game open - neutral mode
#. Game open for creation or editing - edit mode
#. Game being played - playing mode

Here is a table showing which menu items are to be enabled in each mode:

+---------------------+---------+---------+---------+
| Menu Item           | Neutral |   Edit  | Playing |
+=====================+=========+=========+=========+
| file-open           | X       | X       | X       |
+---------------------+---------+---------+---------+
| file-create         | X       | X       | X       |
+---------------------+---------+---------+---------+
| file-close          |         | X       | X       |
+---------------------+---------+---------+---------+
| file-save           |         | X       |         |
+---------------------+---------+---------+---------+
| file-save_as        |         | X       |         |
+---------------------+---------+---------+---------+
| file-print          |         | X       | X       |
+---------------------+---------+---------+---------+
| file-exit           | X       | X       | X       |
+---------------------+---------+---------+---------+
| edit-modify         |         | X       | X       |
+---------------------+---------+---------+---------+
| edit-cut            |         | X       |         |
+---------------------+---------+---------+---------+
| edit-copy           |         | X       |         |
+---------------------+---------+---------+---------+
| edit-paste          |         | X       |         |
+---------------------+---------+---------+---------+
| game-names          | X       | X       | X       |
+---------------------+---------+---------+---------+
| game-practice       | X       | X       | X       |
+---------------------+---------+---------+---------+
| game-play           | X       | X*      | X*      |
+---------------------+---------+---------+---------+
| game-correct_scores |         | X*      | X*      |
+---------------------+---------+---------+---------+
| help-using_program  | X       | X       | X       |
+---------------------+---------+---------+---------+
| help-rules          | X       | X       | X       |
+---------------------+---------+---------+---------+
| help-about          | X       | X       | X       |
+---------------------+---------+---------+---------+

* These menu items are only available if the game loaded is marked as playable.

But a question has been raised in my mind. How is the program to know, when the user loads a game, whether the user
wants to edit the game or play the game? One possibility is to presume editing is desired until the user clicks the
"Play Jeopardy!" entry. I could use the edit-modify menu entry to allow for editing during a played game. It would have
to check to see if a game was in progress and suspend it, somehow stopping its timers, as well as activating the items
in edit mode, until the user clicks game-play again (now labelled something like "Return to the Game").

That all suggests a new method in the Jeopardy class: setProgramState(state=neutral, editing or playing) and a new enum
to go with it::

    class ProgramState(Enum):
        Neutral = 1
        Editing = 2
        Playing = 3

Since a couple of the menu entries should only be enabled if a playable game is present I rigged up the ``file_open``
method to read in my ``temp_saved_game`` in the ``src`` directory in order to test whether that happens or not.

That did work but while working on it another thought came to my mind about the ``file_open`` method. It will somehow
(either from a file dialog box or from a custom made game selection box of my own) be given a pathname to open. I
suspect it will be good to save that pathname for later saving. I created a ``self.game_pathname`` just in case.
