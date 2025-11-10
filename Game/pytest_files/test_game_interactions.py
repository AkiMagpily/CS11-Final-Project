import sys
sys.path.append('..')
# Strangely, despite Pycharm freaking out when I use this, it still works whether I run it directly on pycharm or use cmd
from shroom_raider import *


def test_game_interactions():
    game_map = game_loop('../levels/test.txt')  # This uses our testing level
