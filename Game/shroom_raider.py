from tiles import *
from typing import List
class Grid:
    def __init__(self, filepath: str):
        # IMPORTANT NOTE FROM BARKIA: We should create a separate list of lists that contains tile_objects
        # self.text_grid is simply the text representation
        # We might also consider a representation that doesn't use text but rather the actual icons
        # ANOTHER IMPORTANT NOTE FROM BARKIA: this is the filepath im currently using: 'levels/test.txt'
        # This is a relative filepath, which is not good to use. We should change it eventually 
        self.text_grid: List[str] = []
        self.emoji_grid: List[str] = []
        self.filepath: str = filepath
        self.empty: Tile = Tile(".")
        self.paved: Tile = Tile("_")
        self.water: Tile = Tile("~")
        self.rock: Tile = Tile("R")
        self.tree: Tile = Tile("T")
        self.mushroom: Tile = Tile("+")
        self.laro = Laro("player")
        self.axe = Axe("x")
        self.flamethrower = Flamethrower("*")
        self.emojis: dict = {".":self.empty,    # Note from Aki
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
            for row in lines:
                self.text_grid.append([])
                self.emoji_grid.append([])
                placeholder_list = []
                placeholder_list_emoji = []
                for char in row:
                    placeholder_list.append([char])
                    if char == "\n":
                        placeholder_list_emoji.append([self.emojis.get(char)])
                    else:
                        placeholder_list_emoji.append([self.emojis.get(char).get_emoji()])
                self.text_grid[-1] = placeholder_list
                self.emoji_grid[-1] = placeholder_list_emoji

    def __repr__(self):
        for i in self.emoji_grid:
            print(i)
        return f'this is a text representation of the grid:{self.text_grid}'


def game_loop(path):
    game_map = Grid(path)
    player = game_map.laro
    mushrooms_collected = 0
    status = "alive" #could be win (if laro acquires all mushrooms), lose (if laro falls underwater), or alive

    def get_laro_coords():
        i, j = len(game_map.text_grid), len(game_map.text_grid[0])
        for I in range(i):
            for J in range(j):
                if game_map.text_grid[I][J][-1] == "L":
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
    
    def process_move(move_seq: str):
        valid_input: dict[str, tuple[int, int]] = {'W': (-1, 0), 'A': (0, -1), 'S': (1, 0), 'D': (0, 1)}
        new_coords = list(get_laro_coords())
        for char in move_seq:
            if not (char.isalpha()) or not (char.upper() in valid_input.keys()):  # Breaks if invalid input is encountered
                break
            char = char.upper()
            new_coords[0] += valid_input[char][0]
            new_coords[1] += valid_input[char][1]

            game_map.emoji_grid[new_coords[0]][new_coords[1]].append('🧑')

    laro_coords = get_laro_coords()
    mushroom_total = get_mushroom_count()

    while True:
        print_map()
        print(f"Mushrooms collected {mushrooms_collected}/{mushroom_total}")
        print("""Moves available: \n[W/w] Move Up \n[A/a] Move Left \n[S/s] Move Down \n[D/d] Move Right \n[P/p] Pickup item on current tile \n[!]   Reset the stage \n""")

        move = input("Input next moves: ").strip()
        if move == '!':
            print('Goodbye!')
            break
        else:
            process_move(move)

        if status == "win":
            print("You win!")
            break
        elif status == "lose":
            print("You lose! :(")
            break


# Remove this stuff below when done with testing
game_loop('../Game/levels/test.txt')