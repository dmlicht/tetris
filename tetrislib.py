#!/usr/bin/env python
import curses
from contextlib import contextmanager


@contextmanager
def curses_ctx():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    yield stdscr
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


class TerminalIO():
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def draw_board(self, board):
        self.stdscr.clear()
        n_rows, n_cols = board.shape
        board_border = "".join(["*" for _ in range(0, n_cols + 2)]) + '\n'
        self.stdscr.addstr(board_border)
        for y in range(0, n_rows):
            line = "|"
            for x in range(0, n_cols):
                line += ("#" if board[y][x] == 1 else " ")
            line += "|\n"
            self.stdscr.addstr(line)
        self.stdscr.addstr(board_border)
        self.stdscr.refresh()

    def get_input(self):
        key_pressed = self.stdscr.getkey()
        arrow_character_codes = {
            'KEY_LEFT': 'left',
            'KEY_RIGHT': 'right',
            'KEY_UP': 'up',
            'KEY_DOWN': 'down'
        }
        return arrow_character_codes[key_pressed]
