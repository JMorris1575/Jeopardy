from constants import *
from models import Item, Category, Game

import random

def print_game(game):
    print("\ngame.name = ", game.name)
    print("game.topic = ", game.topic)
    print("game.target_group = ", game.target_group)
    print("game.playable = ", game.playable)
    for segment in Segment:
        print("\n" + segment.name)
        for category in game.get_categories(segment):
            print(str(category))

#------------------------------------#
#                                    #
#            Item Tests              #
#                                    #
#------------------------------------#

# Test creation of a single Item
item = Item()
item.clue = 'This is a clue.'
print(item.clue)
item.response = "This is the response to clue."
print(item.response)

# Test creation of a single Item with the initializer
item = Item('This is another clue.', "This is another clue's response.")
print(item.clue)
print(item.response)

# Create an array of items and display them randomly
items = []
for i in range(5):
    item = Item('This is clue ' + str(i), 'This is response ' + str(i))
    items.append(item)
for i in range(10):
    print('Trial ' + str(i+1))
    item = random.choice(items)
    print('     Clue: ' + item.clue)
    print(' Response: ' + item.response)

for i in range(5):
    print('Item[' + str(i) + ']: ' + str(items[i]))


#------------------------------------#
#                                    #
#          Category Tests            #
#                                    #
#------------------------------------#

# check creation of a single category
print('\nSingle Category:')
category = Category()
category.title = 'Wishes & Dishes'
category.explanation = 'Foods you would like to eat'
print(str(category))
print('Explanation: ', category.explanation)

# check creation of a single category with the initializer
print('\nSingle Category with initializer:')
category = Category('Category 1', 'Explanation of Category 1')
print(str(category))

# check creation of a single category with 5 items
print('\nSingle Category with 5 items:')
category = Category('Category with Items', 'Five items to be exact.')
for i in range(5):
    category.add_item(Item('Item ' + str(i), 'Response to item ' + str(i)))
print(str(category))
for i in range(5):
    print('   Item ' + str(i) + ': ' + str(category.items[i]))


#------------------------------------#
#                                    #
#            Game Tests              #
#                                    #
#------------------------------------#

# check creation of game from scratch

print('\nBuilding a game from scratch:')
game = Game()
game.name = 'Catechism Questions'
game.topic = 'Catholic Faith'
game.target_group = 'Teens'
game.playable = False
print(str(game))

# check creation of game from the initializer

print('\nBuilding a game using the initializer:')
game = Game('Church History','Catholic Faith', 'Teens', False)
print(str(game))

# check creation of partial game with Jeopardy items filled in

print('\nBuilding a game with a complete set of Jeopardy items:')
game = Game('Physics', 'Science', 'Upper Elementary', False)
for i in range(6):
    segment = Segment.Jeopardy
    category = Category('Category ' + str(i), 'Explanation ' + str(i))
    for j in range(5):
        item = Item(segment.name + ' Clue ' + str(j), 'Response ' + str(j))
        category.add_item(item)
    game.add_category(segment, category)
print(str(game))
category = random.choice(game.get_categories(Segment.Jeopardy))
print(str(category.items[2]))

# check creation of complete game with all segments filled in

print('\nBuilding a game with a complete set of items from each segment')
game = Game('General Science', 'Science', 'Upper Elementary')
for segment in Segment:
    if segment.name != 'FinalJeopardy':
        for i in range(6):
            category = Category('Category ' + str(i), 'Explanation ' + str(i))
            for j in range(5):
                item = Item(segment.name + ' Clue ' + str(j), 'Response ' + str(j))
                category.add_item(item)
            game.add_category(segment, category)
    else:
        category = Category('Final Jeopardy Category', 'Final Jeopardy Category Explanation')
        item = Item('Final Jeopardy Clue', 'Final Jeopardy Response')
        category.add_item(item)
        game.add_category(segment, category)
print(str(game))
for segment in Segment:
    print('An item from ' + segment.name)
    category = random.choice(game.get_categories(segment))
    item = random.choice(category.items)
    print(str(category))
    print(str(item))

# Writing and Reading a gamefile

# Save the game to 'temp_saved_game.jqz'

print_game(game)
print("\nWriting game to file...")
game.write_game('temp_saved_game')
print('Destroying previous game...')
game = None
game = Game()
print_game(game)
print('Reading game from file...')
game = game.read_game('temp_saved_game')
print("\nThe resulting game:")
print_game(game)