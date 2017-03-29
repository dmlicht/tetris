from pprint import pprint

import pytest

import tetris

LINE_BLOCK_INDICES = [
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0)
]


@pytest.fixture()
def line_block():
    return tetris.Block(LINE_BLOCK_INDICES)


def test_pytest():
    assert True is True


def test_create_block():
    block = tetris.Block([(0, 0), (0, 1)])
    assert block.block[0, 0] == 1
    assert block.block[0, 1] == 1
    assert block.block[0, 2] == 0


def test_rotate_block(line_block):
    for row_ii, col_ii in LINE_BLOCK_INDICES:
        assert line_block.block[row_ii, col_ii] == 1

    expected_rotation_indices = [
        (3, 0),
        (3, 1),
        (3, 2),
        (3, 3)
    ]

    line_block.rotate()
    pprint(line_block)

    for row_ii, col_ii in expected_rotation_indices:
        assert line_block.block[row_ii, col_ii] == 1
    assert line_block.block[0, 0] == 0
