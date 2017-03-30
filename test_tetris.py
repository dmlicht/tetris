from pprint import pprint

import pytest
import numpy as np

from tetris import Block, Offset, Location, Board

LINE_BLOCK_INDICES = [
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0)
]


@pytest.fixture()
def line_block_offsets():
    return [Offset(*tup) for tup in LINE_BLOCK_INDICES]


@pytest.fixture()
def line_block_locations():
    return [Location(*tup) for tup in LINE_BLOCK_INDICES]


@pytest.fixture()
def line_block(line_block_offsets):
    return Block(line_block_offsets)


@pytest.fixture()
def board():
    return Board()


def test_pytest():
    assert True is True


def test_create_block(line_block, line_block_locations):
    actual_locations = list(line_block.get_locations())
    assert actual_locations == line_block_locations


def test_move_block(line_block):
    expected = [
        Location(0, 1),
        Location(1, 1),
        Location(2, 1),
        Location(3, 1)
    ]
    moved = line_block.move(Offset(0, 1))
    assert list(moved.get_locations()) == expected


def test_rotate_block(line_block):
    expected = [
        Location(0, 0),
        Location(0, 1),
        Location(0, 2),
        Location(0, 3)
    ]
    rotated = line_block.rotate()
    print(list(rotated.get_locations()))
    assert set(rotated.get_locations()) == set(expected)


def test_create_board():
    assert Board()


def test_board_with_block(board, line_block, line_block_locations):
    with_line_block = board.with_block(line_block)
    for location in line_block_locations:
        assert with_line_block._board[location.row, location.col] == 1
    assert with_line_block._board[5, 5] == 0


def test_can_place_block_fails_out_of_bounds(board, line_block):
    out_of_bounds_block = line_block.move(Offset(0, -1))
    assert board.can_place_block(out_of_bounds_block) == False


def test_can_place_block_fails_with_another_block(board, line_block):
    board = board.with_block(line_block)
    assert board.can_place_block(line_block) == False


def test_can_place_block_succeeds_without_conflict(board, line_block):
    assert board.can_place_block(line_block) == True


def test_clear_removes_full_bottom_rows(board):
    board._board[-2:, :] = 1  # fill up the bottom two rows
    board.clear()
    assert np.sum(board._board) == 0


def test_clear_returns_the_correct_number_of_points(board):
    board._board[-2:, :] = 1  # fill up the bottom two rows
    assert board.clear() == 2
