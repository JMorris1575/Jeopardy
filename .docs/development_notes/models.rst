========================================
Developing and Testing the Model Classes
========================================

Here's the plan:

#. Write the three model classes: GameModel, CategoryModel and Item Model.

    A. Each should have getters and setters as appropriate. (It's NOT appropriate in Python.)

    #. Methods should be developed as the need arises

        i. __str__ methods for each class

        #. an add_item(Item) method for the Category model - external program has no need to know how the items are added

        #. an add_category(Segment, Category) method for the Game model - same reason as above

        #. a get_categories(Segment) method - it seemed useful in the testing program so it may be useful later too

        #. I created a Segment enum class for the segments of the game: Jeopardy, Double Jeopardy and Final Jeopardy.

    #. The GameModel should be able to save itself to a .jqz file.

#. Build a separate program to populate and test every aspect of the models.

    A. All elements can have simple contents: Category A through F for example.

    #. The program should create, fill, check by getting what was filled in.

    #. Saving and loading can be checked last.

The Revised Models
==================

Originally copied from :doc:`design`, here are the final forms of the model classes:

.. csv-table:: **The Game Class**
    :header: Field, contents, comments
    :widths: 20, 20, 40

    name, string, optional-to give the game a name
    topic, string, optional-to give the game a category
    target-group, string, description of the group anticipated to play the game
    playable, boolean, true if the game is finished and ready for play
    jeopardy, list of categories, the clues and responses for the Jeopardy portion of the game
    double-jeopardy, list of categories, the clues and responses for the Double Jeopardy portion of the game
    final-jeopardy, category, the clue and response for the Final Jeopardy portion of the game

|

.. csv-table:: **The Category Class**
    :header: Field, contents, comments
    :widths: 20, 20, 40

    title, string, category title to appear on board
    explanation, string, optional explanation for that category
    items, list of ItemModels, contain the clues and responses for that category in order from least to most valuable

|

.. csv-table:: **The Item Class**
    :header: Field, Contents, Comments
    :widths: 20, 20, 40

    clue, string, the clue to appear on the board when its square is clicked
    response, string, the correct response to the clue appearing when no one gets it right

Comments
========

I made some changes in the models as I was putting them together. These changes should be reflected above.

The writing and reading of files was easy enough - the pickle module does all the work. My only difficulty was to
figure out how the ``read_game()`` method of the ``Game()`` class could read the information from the file and put it
into itself. It turned out that the operative line IN the method was:

``self = pickle.load(pathname)``

as well as returning the instance:

``return self``

To use it one needs to create a game and then use an assignment statement back to itself:

game = Game()
game = game.read_game(<pathname>)

I will probably be using this a lot since, as I envision it now, the program will keep a list of games that are ready
to be played. This may require a frequent reading of all the games available to see which ones are ready.

Next Step
=========

Now I think it's time to start working on the user interface. It will be a main window program and so here is a
tentative plan:

#. Create the main window
#. Add all of the menu items
#. Stub in all of the menu functions
#. Get the exit menu item working
#. Add the central window and all of its widgets.
#. Get the Open... menu item working - after which the opened game displays itself in the main window in some form
#. Get the Save and Save As... menu items working
#. Too tired to think of the rest of it at the moment...

