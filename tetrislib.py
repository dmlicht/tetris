#!/usr/bin/env python
import os
import sys
import tty
from subprocess import Popen, PIPE


# The board is represented as an array of arrays, with 10 rows and 10 columns.
# BOARD_SIZE = {"x": 10, "y": 10}
# board = np.zeros(BOARD_SIZE.values())


def draw_board(board):
    """ Draws the contents of the board with a border around it. """
    n_rows, n_cols = board.shape
    board_border = "".join(["*" for _ in range(0, n_cols + 2)])
    print(board_border)
    for y in range(0, n_rows):
        line = "|"
        for x in range(0, n_cols):
            line += ("#" if board[y][x] == 1 else " ")
        line += "|"
        print(line)
    print(board_border)


# Waits for a single character of input and returns the string "left", "down", "right", "up", or None.
def get_input():
    original_terminal_state = None

    try:
        original_terminal_state = Popen("stty -g", stdout=PIPE, shell=True).communicate()[0]
        # Put the terminal in raw mode so we can capture one keypress at a time instead of waiting for enter.
        os.system("stty raw -echo")

        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

        # The arrow keys are read from stdin as an escaped sequence of 3 bytes.
        escape_sequence = "\x1b"
        ctrl_c = "\003"
        if ch == escape_sequence:
            # The next two bytes will indicate which arrow keyw as pressed.
            character = sys.stdin.read(2)
            arrow_character_codes = dict(D="left", B="down", C="right", A="up")
            return arrow_character_codes.get(character[1], None)
        elif ch == ctrl_c:
            sys.exit()
    finally:
        ## TODO: this is a hack
        os.system("stty sane")

    return None
