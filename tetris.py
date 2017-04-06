#!/usr/bin/env python
from collections import namedtuple
from typing import Sequence

from blocks import BLOCKS
from tetrislib import *
import numpy as np
import random
import threading
from functools import partial

BLOCK_DIMENSION = 4
DEFAULT_BOARD_DIMENSIONS = {"x": 10, "y": 10}
DROP_DELAY = 1.5

Location = namedtuple("Location", 'row col')
Offset = namedtuple("Offset", 'row col')


class Block:
    """ Keeps track of offset positions, location and rotations of block """

    def __init__(self, offsets: Sequence[Offset], location: Location = Location(0, 0)):
        self._location = location
        self._offsets = offsets

    def rotate(self) -> 'Block':
        """ Returns a new block representing the 90 degree rotation of this block """
        new_offsets = [Offset(col, BLOCK_DIMENSION - 1 - row) for row, col in self._offsets]
        return Block(new_offsets, self._location)

    def move(self, offset: Offset) -> 'Block':
        """ Returns a new block representing a transposition of a given block by offset """
        new_location = Location(self._location.row + offset.row, self._location.col + offset.col)
        return Block(self._offsets, new_location)

    def get_locations(self):
        for offset in self._offsets:
            yield Location(self._location.row + offset.row, self._location.col + offset.col)


class Board:
    """ Handles state of the tetris board """

    def __init__(self, dimensions=None, board=None):
        self._dimensions = DEFAULT_BOARD_DIMENSIONS if dimensions is None else dimensions
        self._board = np.zeros((self._dimensions['x'], self._dimensions['y'])) if board is None else board

    def with_block(self, block) -> 'Board':
        """ Returns a new board containing the argument block """

        new_board = self._add_block(block)
        return Board(dimensions=self._dimensions, board=new_board)

    def _add_block(self, block: Block) -> np.ndarray:
        new_board = np.copy(self._board)
        for location in block.get_locations():
            new_board[location.row, location.col] += 1
        return new_board

    def can_place_block(self, block: Block) -> bool:
        """ Returns True if there is space to place the argument block. """
        for location in block.get_locations():
            for dim in range(2):
                if location[dim] >= self._board.shape[dim] or location[dim] < 0:
                    return False
            if self._board[location[0], location[1]] > 0:
                return False
        return True

    def clear(self) -> int:
        """ Clears full bottom rows and returns amount of rows cleared 
        Actually this would be nice to have return another board as well, to be consistent with the 
        rest of the api - but I don't have time to redesign it at the moment."""

        rows_cleared = 0
        ii = self._board.shape[0] - 1
        while ii >= 0:
            row_full = all(self._board[ii, :])
            if row_full:
                rows_cleared += 1
                ii -= 1
            else:
                break

        self._remove_bottom_n_rows(rows_cleared)
        return rows_cleared

    def _remove_bottom_n_rows(self, n):
        if n == 0:
            return
        self._board[-1 * n:, :] = 0
        self._board = np.roll(self._board, n, axis=0)


def next_block():
    rand = random.randint(0, len(BLOCKS) - 1)
    locations = [Location(*tup) for tup in BLOCKS[rand]]
    return Block(locations)


MOVES = {
    'right': (0, 1),
    'left': (0, -1),
    'down': (1, 0)
}


class Game:
    def __init__(self):
        self.board = Board()
        self.active_block = next_block()
        self.game_over = False
        self.points = 0
        self.timed_down = None
        self.terminal_io = None

    def run(self):
        with curses_ctx() as stdscr:
            self.terminal_io = TerminalIO(stdscr)
            self._display_state()
            self._reset_down_timer()

            # self.timed_drop = self.scheduler.enter(DROP_DELAY, 1, self.handle_move, argument=("down",))
            while not self.game_over:
                next_move = self.terminal_io.get_input()
                self.handle_move(next_move)

        print("Game over, you got " + str(self.points) + " points.")

    def handle_move(self, move):
        if move == "up":
            rotated = self.active_block.rotate()
            if self.board.can_place_block(rotated):
                self.active_block = rotated
        elif move in ["left", "right", "down"]:
            move_offset = translate_move(move)
            moved_block = self.active_block.move(move_offset)
            if self.board.can_place_block(moved_block):
                self._display_state()
                self.active_block = moved_block
            elif move == "down":
                self.board = self.board.with_block(self.active_block)
                self.points += self.board.clear()
                self.active_block = next_block()
                if not self.board.can_place_block(self.active_block):
                    self.game_over = True
            if move == "down" and not self.game_over:
                self._reset_down_timer()
        self._display_state()

    def _display_state(self):
        print("score:", self.points)
        active_board = self.board.with_block(self.active_block)
        self.terminal_io.draw_board(active_board._board)

    def _reset_down_timer(self):
        if self.timed_down is not None:
            self.timed_down.cancel()
        move_down = partial(self.handle_move, "down")
        self.timed_down = threading.Timer(DROP_DELAY, move_down)
        self.timed_down.start()


def translate_move(move_type: str) -> Offset:
    if move_type == "left":
        return Offset(0, -1)
    elif move_type == "right":
        return Offset(0, 1)
    elif move_type == "down":
        return Offset(1, 0)
    else:
        raise Exception("Bad move type")


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
