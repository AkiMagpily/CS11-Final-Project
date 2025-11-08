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
                    placeholder_list.append(char)
                    if char == "\n":
                        placeholder_list_emoji.append(self.emojis.get(char))
                    else:
                        placeholder_list_emoji.append(self.emojis.get(char).get_emoji())
                self.text_grid[-1] = ''.join(placeholder_list).strip()
                self.emoji_grid[-1] = ''.join(placeholder_list_emoji).strip()

    def __repr__(self):
        return f'this is a text representation of the grid:{self.text_grid}'

    def show_grid(self):
        for row in self.emoji_grid:
            print(row)


def game_loop(path):
    def get_laro_coords():
        i, j = len(game_map.text_grid), len(game_map.text_grid[0])
        for I in range(i):
            for J in range(j):
                if game_map.text_grid[I][J] == "L":
                    return (I,J)

    def get_mushroom_count():
        temp = 0
        for row in game_map.text_grid:
            for col in row:
                if col == "+":
                    temp += 1
        return temp
    
    #rewrite this function to print the emojis instead
    def print_map():
        for row in game_map.text_grid:
            for col in row:
                print(col, end="")
            print("\n")
    
    def process_move():
        for m in move:
            n = m
            if n.isalpha():
                n = n.upper()
            # UNFINISHED, need the proper grid with Tile and Item objects

    laro_coords = get_laro_coords()
    game_map = Grid(path)
    mushroom_total = get_mushroom_count()
    mushrooms_collected = 0
    status = "alive" #could be win (if laro acquires all mushrooms), lose (if laro falls underwater), or alive

    while True:
        print_map()
        print(f"Mushrooms collected {mushrooms_collected}/{mushroom_total}")
        print("""Moves available:
              [W/w] Move Up
              [A/a] Move Left
              [S/s] Move Down
              [D/d] Move Right
              [P/p] Pickup item on current tile
              [!]   Reset the stage""")

        move = input("Input next moves: ")
        process_move()

        if status == "win":
            print("You win!")
            break
        elif status == "lose":
            print("You lose! :(")
            break


# Remove this stuff below when done with testing
test = Grid('../Game/levels/test.txt')
print(repr(test))
test.show_grid()
