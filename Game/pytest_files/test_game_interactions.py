import sys
sys.path.append('..')
# Strangely, despite Pycharm freaking out when I use this, it still works whether I run it directly on pycharm or use cmd
from shroom_raider import Grid, game_loop
from unittest.mock import patch


def test_exit(capsys):
    with patch('builtins.input', side_effect=['!']) as mock_input:
        game_loop('../levels/test.txt')  # This uses our testing level
        captured = capsys.readouterr()
        output = captured.out.strip()  # This gets rid of the whitespace at the end
        lines = output.split('\n')
        # The very last line is either a prompt for more inputs, a win/lose statement, or a goodbye
        # statement if you exited the program
        last_line = lines[-1]
        assert last_line == 'Goodbye!'  # Confirm the last line shows you've exited the program


def test_movement_south(capsys):
    with patch('builtins.input', side_effect=['s', '!']):  # side_effect contains the test mock inputs
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        # The source code prints the grid once upon startup, and once more for each character in the input that isn't a '!'
        # captured.out captures all of these grids and stores them as a string, which is then split based off the newlines
        output = captured.out.strip()
        lines = output.split('\n')
        # Since there are three grids (once upon startup, two more from the mock input), the second grid
        # represents the grid after Laro makes his first move, which is relevant
        # The second grid ranges from lines[16] to lines[21]
        grid = lines[16:22]
        # Since Laro starts at (1, 1) and moved down, we expect him to be at (2, 1).
        expected_location_of_laro = grid[2][1]
        assert expected_location_of_laro == '🧑'


def test_movement_north(capsys):
    with patch('builtins.input', side_effect=['s', 'w', '!']):
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        # Since the mock input has two move chars, the third grid (found at 32 -> 37) will be used instead
        grid = lines[32:38]
        # Since Laro starts at (1, 1) and moved down, we expect him to be at (2, 1).
        # However, since he moved north, he would return to (1, 1)
        expected_location_of_laro = grid[1][1]
        assert expected_location_of_laro == '🧑'


def test_movement_east(capsys):
    with patch('builtins.input', side_effect=['d', '!']):
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        grid = lines[16:22]
        # Since Laro starts at (1, 1) and moved east he is expected to be at (1, 2)
        expected_location_of_laro = grid[1][2]
        assert expected_location_of_laro == '🧑'


def test_movement_west(capsys):
    with patch('builtins.input', side_effect=['d', 'a', '!']):
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        # Since the mock input has two move chars, the third grid (found at 32 -> 37) will be used instead
        grid = lines[32:38]
        # Since Laro starts at (1, 1) and moved east he is expected to be at (1, 2)
        # However, since he moves west, he is expected to be at (1, 1)
        expected_location_of_laro = grid[1][1]
        assert expected_location_of_laro == '🧑'


def test_axe_pickup(capsys):
    with patch('builtins.input', side_effect=['d']*7 + ['!']):  # Evaluate what happens when Laro gets an axe
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        # This requires 7 d-inputs, meaning we go to grid 8 to find the relevant grid
        grid = lines[112:118]
        # Since Laro starts at (1, 1) and moved east 8 times he is expected to be at (1, 8)
        # He is expected to reach (1, 8), and to have Axe as his powerup
        expected_location_of_laro = grid[1][8]
        expected_power_of_laro = lines[119]
        assert expected_location_of_laro == '🧑'
        assert 'Axe' in expected_power_of_laro


def test_axe_use(capsys):
    with patch('builtins.input', side_effect=['d']*8 + ['!']):  # Evaluate what happens when Laro moves right until hitting a tree, assuming he has an axe
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        # This requires 8 d-inputs, meaning we go to grid 9 to find the relevant grid
        grid = lines[128:134]
        # Since Laro starts at (1, 1) and moved east 8 times he is expected to be at (1, 9)
        # at (1, 9) there is a tree, but at (1, 8) there is also an axe
        # He is expected to chop the tree and reach (1, 9)
        expected_location_of_laro = grid[1][9]
        expected_power_of_laro = lines[135]
        assert expected_location_of_laro == '🧑'
        assert 'None' in expected_power_of_laro  # It is expected that the power has been used


def test_flamethrower_pickup(capsys):
    with patch('builtins.input', side_effect=['d']*7 + ['s', 'a', 'd', 'd', 'a', 's'] + ['!']):  # Evaluate what happens when Laro gets an axe
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        # This requires 13 move inputs, meaning we go to grid 14 to find the relevant grid
        grid = lines[208:214]
        expected_location_of_laro = grid[3][8]
        expected_power_of_laro = lines[215]
        assert expected_location_of_laro == '🧑'
        assert 'Flamethrower' in expected_power_of_laro


def test_flamethrower_use(capsys):
    with patch('builtins.input', side_effect=['d']*7 + ['s', 'a', 'd', 'd', 'a', 's', 'd'] + ['!']):  # Evaluate what happens when Laro gets an axe
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        # This requires 14 move inputs, meaning we go to grid 15 to find the relevant grid
        grid = lines[224:230]
        expected_location_of_laro = grid[3][9]
        expected_power_of_laro = lines[231]
        assert expected_location_of_laro == '🧑'
        assert 'None' in expected_power_of_laro  # It is expected that the power has been used


def test_collission_tree(capsys):
    with patch('builtins.input', side_effect=['w', '!']):  # Evaluate what happens when Laro directly walks into a tree
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        grid = lines[16:22]
        # Since Laro starts at (1, 1) and moved up, but was blocked by a tree, he is expected not to have moved
        expected_location_of_laro = grid[1][1]
        assert expected_location_of_laro == '🧑'


def test_water(capsys):
    with patch('builtins.input', side_effect=['s', 's', '!']):  # Evaluate what happens when Laro directly walks into water
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        grid = lines[16:22]
        # Since Laro is expected to die, then the last line of 'lines' is expected to be a loss message
        expected_location_of_laro = grid[1][1]
        last_line = lines[-1]
        assert last_line == "You lose! :("


def test_collision_rock(capsys):
    with patch('builtins.input', side_effect=['d', 'd', 's', '!']):  # Evaluate what happens when Laro walks into a rock
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        grid = lines[48:54]
        # Since Laro's last movement before pushing the rock was downwards, we expect the rock to be
        # right below him
        expected_location_of_laro = grid[2][3]
        expected_location_of_rock = grid[3][3]
        assert expected_location_of_laro == '🧑'
        assert expected_location_of_rock == '🪨'


def test_collision_rock_and_mushroom(capsys):  # Evaluate what happens when Laro pushes a rock into a mushroom
    with patch('builtins.input', side_effect=['d', 'd', 'd', 's', 'a', '!']):
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        grid = lines[80:86]
        # Since Laro is pushing the rock into the mushroom, we expect there to be no movement
        expected_location_of_laro = grid[2][4]
        expected_location_of_rock = grid[2][3]
        expected_location_of_mushroom = grid[2][2]
        assert expected_location_of_laro == '🧑'
        assert expected_location_of_rock == '🪨'
        assert expected_location_of_mushroom == '🍄'


def test_collision_rock_and_axe(capsys):  # Evaluate what happens when Laro pushes a rock into an axe
    with patch('builtins.input', side_effect=['d', 'd', 's', 'a', 's', 'd', '!']):
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        grid = lines[96:102]
        # Since Laro is pushing the rock into the axe, we expect there to be no movement
        expected_location_of_laro = grid[3][2]
        expected_location_of_rock = grid[3][3]
        expected_location_of_axe = grid[3][4]
        assert expected_location_of_laro == '🧑'
        assert expected_location_of_rock == '🪨'
        assert expected_location_of_axe == '🪓'


def test_collision_rock_and_flamethrower(capsys):  # Evaluate what happens when Laro pushes a rock into a flamethrower
    with patch('builtins.input', side_effect=['d', 'd', 's', 's', 'a', 's', 'd', '!']):
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        grid = lines[112:118]
        # Since Laro is pushing the rock into the flamethrower, we expect there to be no movement
        expected_location_of_laro = grid[4][2]
        expected_location_of_rock = grid[4][3]
        expected_location_of_fire = grid[4][4]
        assert expected_location_of_laro == '🧑'
        assert expected_location_of_rock == '🪨'
        assert expected_location_of_fire == '🔥'


def test_collision_rock_and_water(capsys):  # Evaluate what happens when Laro pushes a rock into water
    with patch('builtins.input', side_effect=['d', 's', 'w', 'd', 'd', 's', 'a', 'a', 'w', 'a', 's', '!']):
        game_loop('../levels/test.txt')
        captured = capsys.readouterr()
        output = captured.out.strip()
        lines = output.split('\n')
        grid = lines[176:182]
        # Since Laro is pushing the rock into the water, we expect that right below him lies a paved tile
        expected_location_of_laro = grid[2][1]
        expected_location_of_paved = grid[3][1]
        assert expected_location_of_laro == '🧑'
        assert expected_location_of_paved == '⬜'