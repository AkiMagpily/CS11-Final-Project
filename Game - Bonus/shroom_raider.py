from tiles import *
from typing import List
from termcolor import colored
import os
import sys
import shutil
import keyboard
import time

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


def delete_last_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def end_program():
    sys.exit()


def level_select():
    clear()
    level_count = 4
    print("Select a level:\n")
    print("[0] Tutorial")
    for l in range(1,level_count+1):
        print(f"[{l}] Level {l}")
    print("[E/e] Exit Program")
    
    key_pressed = keyboard.read_key()

    if key_pressed == "e" or key_pressed == "shift+e":
        clear()
        print('Program Ended... Thanks for playing!')
        end_program()

    if not key_pressed.isdecimal():
        print("That's not a correct level.")
        level_select()

    try:
        key_pressed = int(key_pressed)
        if key_pressed == 5:
            print('Discovered a secret level!')
            game_loop('../Game/levels/test.txt')
        elif key_pressed == 0:
            print("""Tutorial:\nYou can use WASD to move Laro around.\nCollect all mushrooms to win.\nAvoid falling in water\nRocks can be pushed around, push it into water and it turns into a paved tile.\nAn Axe lets you cut a single tree\nA flamethrower lets you burn consecutive trees.""")
            game_loop('../Game/levels/tutorial.txt')
        elif 0 < key_pressed <= level_count:
            game_loop(f'../Game/levels/level{key_pressed}.txt')
        else:
            print("That's not a correct level.")
            level_select()
    except:
        pass

def game_loop(path, *new_move):
    def post_level():
        key_pressed = keyboard.read_key()
        if key_pressed == "shift+1":
            game_loop(path)
        elif key_pressed == "l" or key_pressed == "shift+l":
            level_select()
        elif key_pressed == "e" or key_pressed == "shift+e":
            clear()
            print('Program Ended... Thanks for playing!')
            end_program()
        else:
            delete_last_line()
            print("Incorrect Input")
            post_level()

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

    def print_map():
        term_width = shutil.get_terminal_size().columns
        for row in game_map.emoji_grid:
            print_row = []
            for col in row:
                if col[-1] != "\n":
                    print_row.append(col[-1])
            print(''.join(print_row).center(term_width-12))
        print("".center(term_width))

    def fire_traverse(coords: list[int, int], grid):
        r, c = coords[0], coords[1]
        rows, cols = len(grid), len(grid[0])
        if 0 <= r < rows and 0 <= c < cols-1:
            # Removes the tree
            if '🌲' in grid[r][c]:
                grid[r][c].pop()  # Removes the tree on the current tile
                # Recursively travels to all adjacent tiles
                fire_traverse([r - 1, c], grid)
                fire_traverse([r + 1, c], grid)
                fire_traverse([r, c - 1], grid)
                fire_traverse([r, c + 1], grid)

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

            # If the movement sends you out of the grid, it is not processed
            if not (0 <= new_coords[0] + r < rows and 0 <= new_coords[1] + c < cols - 1):
                continue   
            curr_tile = game_map.emoji_grid[new_coords[0]][new_coords[1]]
            first_tile = game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c]
                                                              
            if char == 'P' and '🔥' in curr_tile and game_map.laro.get_powerup() != game_map.flamethrower:
                curr_tile.pop()  # Gets rid of the powerup emoji in the current tile

                if game_map.laro.get_powerup() is None:  # Pickup powerup then move Laro
                    curr_tile.pop()
                    curr_tile.append('🧑')
                elif isinstance(game_map.laro.get_powerup(), Axe):  # Swap powerup then move Laro
                    curr_tile.pop()
                    curr_tile.append('🪓')
                    curr_tile.append('🧑')
                game_map.laro.new_powerup(game_map.flamethrower, game_map.flamethrower.get_name(), game_map.flamethrower.get_emoji())
            elif char == 'P' and '🪓' in curr_tile and game_map.laro.get_powerup() != game_map.axe:
                curr_tile.pop()  # Gets rid of the powerup emoji in the current tile

                if game_map.laro.get_powerup() is None:  # Pickup powerup then move Laro
                    curr_tile.pop()
                    curr_tile.append('🧑')
                elif isinstance(game_map.laro.get_powerup(), Flamethrower):  # Swap powerup then move Laro
                    curr_tile.pop()
                    curr_tile.append('🔥')
                    curr_tile.append('🧑')
                game_map.laro.new_powerup(game_map.axe, game_map.axe.get_name(), game_map.axe.get_emoji())

            if '🌲' in first_tile:  # Tree interactions
                if isinstance(game_map.laro.get_powerup(), Axe):  # Axe interaction
                    game_map.laro.use_powerup()
                    game_map.emoji_grid[new_coords[0] + r][new_coords[1] + c].pop()
                elif isinstance(game_map.laro.get_powerup(), Flamethrower):  # Flamethrower interaction
                    game_map.laro.use_powerup()
                    next_tile = [new_coords[0] + r, new_coords[1] + c]
                    fire_traverse(next_tile, game_map.emoji_grid)
                else:  # Regular collision (the move input is ignored)
                    continue
            elif '🪨' in first_tile:  # Rock interactions
                # The next_tile is the one in front of the rock, not the one in front of Laro
                next_tile = game_map.emoji_grid[new_coords[0]+(r*2)][new_coords[1]+(c*2)]
                if  not (0 <= new_coords[0] + (r*2) < rows and 0 <= new_coords[1] + (c*2) < cols - 1):
                    continue
                elif tuple(x for x in ('🌲','🪨','🍄','🔥','🪓') if x in next_tile):
                    continue
                elif '🟦' in next_tile:  # Remove both water and rock tile. Add a paved tile
                    next_tile.remove('🟦')
                    next_tile.append('⬜')
                    first_tile.remove('🪨')
                else:  # Default interaction: the rock is pushed
                    first_tile.pop()
                    next_tile.append('🪨')
            elif first_tile[-1] == '🟦':  # When directly walking into water, Laro drowns
                status = 'lose'
            if '🍄' in first_tile:  # When walking into a mushroom tile, Laro automatically picks it up
                first_tile.pop()
                global mushrooms_collected
                mushrooms_collected += 1
                if mushrooms_collected == mushrooms_max:
                    status = 'win'
            game_map.emoji_grid[new_coords[0]+r][new_coords[1]+c] = first_tile
         
            curr_tile.pop()  # Removes Laro from the stack of previous coords
            # Then, the coords are updated to simulate movement
            game_map.emoji_grid[new_coords[0]][new_coords[1]] = curr_tile
            new_coords[0] += r
            new_coords[1] += c
            game_map.emoji_grid[new_coords[0]][new_coords[1]].append('🧑')

    laro_coords = get_laro_coords()
    mushroom_total = get_mushroom_count()

    if len(new_move) == 1:
        process_move(new_move[0])

    emcii = {'🌲': 'T', '🪨': 'R', '　': '.', '⬜': '_', '🧑': 'L', '🟦': '~', '🍄': '+', '🪓': 'x', '🔥': '*', '\n': '\n'}
    static_prints = ["Moves available:",
                     "[W/w] Move Up        ",
                     "[A/a] Move Left      ",
                     "[S/s] Move Down      ",
                     "[D/d] Move Right     ",
                     "[P/p] Pickup item    ",
                     "[!]   Reset the stage",
                     "[E/e] Exit Game      "]
    while True:
        term_width = shutil.get_terminal_size().columns
        if len(sys.argv) > 4:  # If the input in cmd is of the form: python -f <stage> -m <string>, this executes
            sys.argv = sys.argv[1:]
            move = str(sys.argv[3])
            process_move(move)
        else:
            clear()
            print_map()
            print(f"Mushrooms collected {mushrooms_collected}/{mushroom_total}".center(term_width))
            print(f'Current power up equipped: {game_map.laro.get_powername()}'.center(term_width))
            for i in static_prints:
                print(i.center(term_width))
            key_pressed = keyboard.read_key()
            time.sleep(0.15)
        
        if key_pressed == "e" or key_pressed == "shift+e":
            level_select()
            break
        else:
            if "shift" in key_pressed:
                process_move(key_pressed[-1])
            else:
                process_move(key_pressed)


        prints = [f"Mushrooms collected {mushrooms_collected}/{mushroom_total}",
                  f'Current power up equipped: {game_map.laro.get_powername()}']
        post_prints = prints[:2]
        static_post_prints = ["Moves available:",
                              "[!]   Reset the stage",
                              "[L/l] Level Select",
                              "[E/e] Exit Program"]
        if len(sys.argv) > 5:
            if status == "win":
                with open(sys.argv[-1], "w") as f:
                    f.write(f'CLEAR \n')
                    for row in game_map.emoji_grid:
                        f.write(''.join(emcii[i[-1]] for i in row))
                    for i in prints:
                        f.write("\n" + i)
                    for i in static_prints:
                        f.write("\n" + i)
                    f.write(f'You win!')
                break
            elif status == "lose":
                with open(sys.argv[-1], "w") as f:
                    f.write(f'NO CLEAR \n')
                    for row in game_map.emoji_grid:
                        f.write(''.join(emcii[i[-1]] for i in row))
                    for i in prints:
                        f.write("\n" + i)
                    for i in static_prints:
                        f.write("\n" + i)
                    f.write(f'You lose! :(')
                break
        else:
            if status != "alive":
                clear()
                print_map()
                for i in post_prints:
                    print(i.center(term_width))
                for i in static_post_prints:
                    print(i.center(term_width))
                if status == "win":
                    print("You win!".center(term_width))
                elif status == "lose":
                    print("You lose! :(".center(term_width))
                post_level()
                break

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        level_select()
    elif len(sys.argv) > 2:
            game_loop(str(sys.argv[2]))
