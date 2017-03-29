#!/usr/bin/env python
from tetrislib import *
import numpy as np
from pprint import pprint

# tetrislib defines the variable board and the functions drawboard() and getinput()
BLOCK_DIMENSION = 4


class Block():
    def __init__(self, square_locations):
        self.block = np.zeros((BLOCK_DIMENSION, BLOCK_DIMENSION))
        self.position = (0, 0)
        for loc in square_locations:
            self.block[loc[0], loc[1]] = 1

    def rotate(self):
        self.block = np.rot90(self.block)


def main():
    # This example code draws a horizontal bar 4 squares long.
    # block = Block([(0, 0), (1, 0), (2, 0), (3, 0)])
    # pprint(block.block)
    # block.rotate()
    # pprint(block.block)
    # block.rotate()
    # pprint(block.block)
    # block.rotate()
    # pprint(block.block)



    row = 2
    board[row][5] = 1
    board[row][6] = 1
    board[row][7] = 1
    board[row][8] = 1

    drawboard()

    # This code waits for input until the user hits a keystroke. getinput() returns one of "left", "up", "right",
    # "down".
    print getinput()


if __name__ == '__main__':
    main()
