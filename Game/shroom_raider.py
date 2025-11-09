from tiles import *
from typing import List
class Grid:
    def __init__(self, filepath: str):
        # self.text grid is the text representation of the grid
        self.text_grid: List[str] = []
        # self.emoji_grid is the emoji representation of the grid
        self.emoji_grid: List[str] = []
        self.filepath: str = filepath

        # Initialize the different tile/item types
        self.empty: Tile = Tile(".")
        self.paved: Tile = Tile("_")
        self.water: Tile = Tile("~")
        self.rock: Tile = Tile("R")
        self.tree: Tile = Tile("T")
        self.mushroom: Tile = Tile("+")
        self.laro = Laro("player")
        self.axe = Axe("x")
        self.flamethrower = Flamethrower("*")

        self.ascii: dict = {".":self.empty,    # Note from Aki
                             "_":self.paved,    # This dict is here so we can immediately fetch the object
                             "~":self.water,    # and functions of the object by just using the ascii of it
                             "R":self.rock,     
                             "T":self.tree,
                             "+":self.mushroom,
                             "L":self.laro,
                             "x":self.axe,
                             "*":self.flamethrower,
                             "\n":"\n"} # Add or change if needed
        self.make_grid(filepath)


    def make_grid(self, filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
            lines = lines[1:]
            for row in lines:
                self.text_grid.append([])
                self.emoji_grid.append([])
                placeholder_list = []
                placeholder_list_emoji = []
                for char in row:
                    placeholder_list.append([char])
                    if char == "\n":
                        placeholder_list_emoji.append([self.ascii.get(char)])
                    elif char in ('L', 'x', '*', 'R', '+', 'T'):
                        # appends an empty tile, then places the char on top of it
                        placeholder_list_emoji.append(['　', self.ascii.get(char).get_emoji()])
                    else:
                        placeholder_list_emoji.append([self.ascii.get(char).get_emoji()])
                self.text_grid[-1] = placeholder_list
                self.emoji_grid[-1] = placeholder_list_emoji

    def __repr__(self):
        for i in self.emoji_grid:
            print(i)
        return f'this is a text representation of the grid:{self.text_grid}'


def game_loop(path):
    game_map = Grid(path)
    global mushrooms_collected
    mushrooms_collected = 0
    global status
    status = "alive"  # Could be win (if laro acquires all mushrooms), lose (if laro falls underwater), or alive

    def get_laro_coords():
        i, j = len(game_map.emoji_grid), len(game_map.emoji_grid[0])
        for I in range(i):
            for J in range(j):
                if game_map.emoji_grid[I][J][-1] == '🧑':
                    return (I,J)

    def get_mushroom_count():
        temp = 0
        for row in game_map.text_grid:
            for col in row:
                if col[-1] == "+":
                    temp += 1
        return temp
    
    #rewritten to use emoji_grid
    def print_map():
        for row in game_map.emoji_grid:
            for col in row:
                print(col[-1], end="")
        print("")

    def fire_traverse(coords: list[int, int], grid):
        r, c = coords[0], coords[1]
        rows, cols = len(grid), len(grid[0])
        if 0 <= r < rows and 0 <= c < cols:
            # Removes the tree
            try:
                if '🌲' in grid[r][c]:
                    grid[r][c].pop()
                    # Recursively travels to all adjacent tiles
                    fire_traverse([r - 1, c], grid)
                    fire_traverse([r + 1, c], grid)
                    fire_traverse([r, c - 1], grid)
                    fire_traverse([r, c + 1], grid)
            except:
                print(f'r: {r}, c: {c}, rows: {rows}, cols: {cols}')

    def process_move(move_seq: str):
        valid_input: dict[str, tuple[int, int]] = {'W': (-1, 0), 'A': (0, -1), 'S': (1, 0), 'D': (0, 1), 'P': (0, 0)}
        new_coords = list(get_laro_coords())
        rows, cols = len(game_map.text_grid), len(game_map.text_grid[0])
        mushrooms_max = get_mushroom_count()

        for char in move_seq:
            global status
            if not (char.isalpha()) or not (char.upper() in valid_input.keys()):  # Breaks if invalid input is encountered
                continue
            char = char.upper()
            r, c = valid_input[char][0], valid_input[char][1]

            if char == 'P' and '🔥' in game_map.emoji_grid[new_coords[0]][new_coords[1]]:
                game_map.emoji_grid[new_coords[0]][new_coords[1]].pop()
                game_map.emoji_grid[new_coords[0]][new_coords[1]].pop()
                game_map.emoji_grid[new_coords[0]][new_coords[1]].append('🪓')
                game_map.emoji_grid[new_coords[0]][new_coords[1]].append('🧑')
                game_map.laro.new_powerup(game_map.flamethrower, game_map.flamethrower.get_name(), game_map.flamethrower.get_emoji())
            elif char == 'P' and '🪓' in game_map.emoji_grid[new_coords[0]][new_coords[1]]:
                game_map.emoji_grid[new_coords[0]][new_coords[1]].pop()
                game_map.emoji_grid[new_coords[0]][new_coords[1]].pop()
                game_map.emoji_grid[new_coords[0]][new_coords[1]].append('🔥')
                game_map.emoji_grid[new_coords[0]][new_coords[1]].append('🧑')
                game_map.laro.new_powerup(game_map.axe, game_map.axe.get_name(), game_map.axe.get_emoji())

            # If the movement sends you out of the grid or into a tree then it breaks
            if not (0 <= new_coords[0] + r < rows and 0 <= new_coords[1] + c < cols - 1):
                continue
            elif '🌲' in game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c]:
                if isinstance(game_map.laro.get_powerup(), Axe):
                    game_map.laro.use_powerup()
                    game_map.emoji_grid[new_coords[0] + r][new_coords[1] + c].pop()
                elif isinstance(game_map.laro.get_powerup(), Flamethrower):
                    game_map.laro.use_powerup()
                    next_tile = [new_coords[0] + r, new_coords[1] + c]
                    fire_traverse(next_tile, game_map.emoji_grid)
                else:
                    continue
            elif '🪨' in game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c]:
                if  not (0 <= new_coords[0] + r + valid_input[char][0] < rows and 0 <= new_coords[1] + c + valid_input[char][1] < cols - 1):
                    continue
                elif '🌲' in game_map.emoji_grid[new_coords[0]+r+valid_input[char][0]][new_coords[1]+c+valid_input[char][1]]:
                    continue
                elif '🪨' in game_map.emoji_grid[new_coords[0]+r+valid_input[char][0]][new_coords[1]+c+valid_input[char][1]]:
                    continue
                elif '🍄' in game_map.emoji_grid[new_coords[0]+r+valid_input[char][0]][new_coords[1]+c+valid_input[char][1]]:
                    continue
                elif '🔥' in game_map.emoji_grid[new_coords[0]+r+valid_input[char][0]][new_coords[1]+c+valid_input[char][1]]:
                    continue
                elif '🪓' in game_map.emoji_grid[new_coords[0]+r+valid_input[char][0]][new_coords[1]+c+valid_input[char][1]]:
                    continue
                elif '🟦' in game_map.emoji_grid[new_coords[0]+r+valid_input[char][0]][new_coords[1]+c+valid_input[char][1]]:
                    game_map.emoji_grid[new_coords[0]+r+valid_input[char][0]][new_coords[1]+c+valid_input[char][1]].remove('🟦')
                    game_map.emoji_grid[new_coords[0]+r+valid_input[char][0]][new_coords[1]+c+valid_input[char][1]].append('⬜')
                    game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c].remove('🪨')
                else:
                    game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c].pop()
                    game_map.emoji_grid[new_coords[0]+r+valid_input[char][0]][new_coords[1]+c+valid_input[char][1]].append('🪨')
            elif '🔥' in game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c]:
                if game_map.laro.get_powerup() is None:
                    game_map.laro.new_powerup(game_map.flamethrower, game_map.flamethrower.get_name(), game_map.flamethrower.get_emoji())
                    game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c].pop()
            elif '🪓' in game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c]:
                if game_map.laro.get_powerup() is None:
                    game_map.laro.new_powerup(game_map.axe, game_map.axe.get_name(), game_map.axe.get_emoji())
                    game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c].pop()
            elif game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c][-1] == '🟦':
                status = 'lose'
            if '🍄' in game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c]:
                game_map.emoji_grid[new_coords[0] + r][new_coords[1] + c].pop()
                global mushrooms_collected
                mushrooms_collected += 1
                if mushrooms_collected == mushrooms_max:
                    status = 'win'
         
            game_map.emoji_grid[new_coords[0]][new_coords[1]].pop()  # Removes Laro from the stack of previous coords
            # Then, the coords are updated
            new_coords[0] += r
            new_coords[1] += c
            game_map.emoji_grid[new_coords[0]][new_coords[1]].append('🧑')


    laro_coords = get_laro_coords()
    mushroom_total = get_mushroom_count()

    while True:
        print_map()
        print(f"Mushrooms collected {mushrooms_collected}/{mushroom_total}")
        print(f'Current power up equipped: {game_map.laro.get_powername()}')
        print("""Moves available: \n[W/w] Move Up \n[A/a] Move Left \n[S/s] Move Down \n[D/d] Move Right \n[P/p] Pickup item on current tile \n[!]   Reset the stage \n""")

        move = input("Input next moves: ").strip()
        if '!' in move:
            print('Goodbye!')
            break
        else:
            process_move(move)

        if status == "win":
            print_map()
            print(f"Mushrooms collected {mushrooms_collected}/{mushroom_total}")
            print(f'Current power up equipped: {game_map.laro.get_powername()}')
            print("""Moves available: \n[W/w] Move Up \n[A/a] Move Left \n[S/s] Move Down \n[D/d] Move Right \n[P/p] Pickup item on current tile \n[!]   Reset the stage \n""")
            print("You win!")
            break
        elif status == "lose":
            print_map()
            print(f"Mushrooms collected {mushrooms_collected}/{mushroom_total}")
            print(f'Current power up equipped: {game_map.laro.get_powername()}')
            print("""Moves available: \n[W/w] Move Up \n[A/a] Move Left \n[S/s] Move Down \n[D/d] Move Right \n[P/p] Pickup item on current tile \n[!]   Reset the stage \n""")
            print("You lose! :(")
            break


# Remove this stuff below when done with testing
game_loop('../Game/levels/test.txt')
