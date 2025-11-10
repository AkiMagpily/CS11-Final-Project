import sys
sys.path.append('..')
# Strangely, despite Pycharm freaking out when I use this, it still works whether I run it directly on pycharm or use cmd
from shroom_raider import Grid


def test_grid_variables():
    # Test if filepath is correct
    grid = Grid('../levels/test.txt')  # This uses our testing level
    assert grid.filepath == '../levels/test.txt'

    # Test if text grid is correct
    testing_grid = open('../levels/test.txt', 'r').readlines()[1:]
    for r in range(len(testing_grid)):
        for c in range(len(testing_grid[r])):
            test_char = testing_grid[r][c]
            text_grid_char = grid.text_grid[r][c][-1]
            assert test_char == text_grid_char

    # Test if emoji grid is correct
    emoji_dict = {'.': '　',
                  '~': '🟦',
                  'T': '🌲',
                  'R': '🪨',
                  '+': '🍄',
                  '_': '⬜',
                  'L': '🧑',
                  'x': '🪓',
                  '*': '🔥',
                  '\n': '\n'}
    for r in range(len(testing_grid)):
        for c in range(len(testing_grid[r])):
            test_key = testing_grid[r][c]
            grid_tile = grid.ascii.get(grid.text_grid[r][c][-1])
            if test_key == '\n':
                assert emoji_dict[test_key] == grid_tile
            else:
                assert emoji_dict[test_key] == grid_tile.get_emoji()
