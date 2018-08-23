from constants import *

import pickle
import os
import sys

class Cell():

    def __init__(self, type, col, row):
        self.type = type
        self.col = col
        self.row = row
        self.text_A = {}
        self.text_B = {}

    def __str__(self):
        return self.type + " cell at (" + str(self.col) + ', ' + str(self.row) + ')'

    def setContents(self, segment, text_A, text_B):
        self.text_A[segment.name] = text_A
        self.text_B[segment.name] = text_B

    def getTextA(self, segment):
        return self.text_A[segment.name]

    def getTextB(self, segment):
        return self.text_B[segment.name]


class Game():

    def __init__(self, name='', topic='', target_group='', playable=False):
        self.name = name
        self.topic = topic
        self.target_group = target_group
        self.playable = playable
        self.board = []                         # the container for all the rows and columns
        for col in range(6):
            self.board.append([Cell("Category", col, 0)])               # the container for each column
            for row in range(5):
                self.board[col].append(Cell("Clue", col, row+1))      # the container for each cell in the column

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

    def setCell(self, col, row, cell):
        self.board[col][row] = cell
        if self.isPlayable():
            self.playable = True
        else:
            self.playable = False

    def isPlayable(self):
        """
        Checks the playability of the game based on each cell having text_A contents for all segments
        :return: True if all cells have contents for text_A, False otherwise
        """
        for col in range(6):
            for row in range(6):
                for segment in Segment:
                    try:
                        test = self.board[col][row].getTextA(segment)
                    except KeyError:
                        playable = False
                        return False
        return True

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
