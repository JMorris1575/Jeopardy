from constants import *

import pickle
import os
import sys

class Item():

    def __init__(self, clue='', response=''):
        self.clue = clue
        self.response = response

    def __str__(self):
        return "    Clue: " + self.clue + "\nResponse: " + self.response


class Category():

    def __init__(self, title='', explanation=''):
        self.title = title
        self.explanation = explanation
        self.items = []     # will hold the clue/response item(s) for this category

    def __str__(self):
        return self.title + ': ' + str(len(self.items)) + ' items.'

    def add_item(self, item):
        self.items.append(item)


class Game():

    def __init__(self, name='', topic='', target_group='', playable=False):
        self.name = name
        self.topic = topic
        self.target_group = target_group
        self.playable = playable
        self.jeopardy = []
        self.double_jeopardy = []
        self.final_jeopardy = []

    def __str__(self):
        if self.playable:
            appendage = ' - ready to be played'
        else:
            appendage = ' - not yet playable'
        if self.name != '':
            msg = self.name + appendage
        else:
            msg = 'unnamed Jeopardy game' + appendage
        return msg

    def add_category(self, segment, category):
        if segment == Segment.Jeopardy:
            self.jeopardy.append(category)
        elif segment == Segment.DoubleJeopardy:
            self.double_jeopardy.append(category)
        else:
            self.final_jeopardy.append(category)

    def get_categories(self, segment):
        if segment == Segment.Jeopardy:
            return self.jeopardy
        elif segment == Segment.DoubleJeopardy:
            return self.double_jeopardy
        else:
            return self.final_jeopardy

    def write_game(self, pathname):
        """
        Writes this game to disk at the location pathname.
        """
        f = None
        f = open(pathname, 'wb')
        try:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            print("{0}: saveProgramInfo error: {1}".format(
                os.path.basename(sys.argv[0]), err))
        finally:
            if f is not None:
                f.close()

    def read_game(self, pathname):
        """
        Reads this game from the file indicated by pathname
        :param pathname: the pathname of the file to read
        :return: None
        """
        f = None
        f = open(pathname, 'rb')
        self = pickle.load(f)
        if f is not None:
            f.close()
        return self
