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

class Tile:
    def __init__(self, tile_type: str = None):
        self.rep: str = None  # Actual representation in the grid
        self.text_rep: str = tile_type  # What is being read from the text files

        self.is_flammable: bool = False  # Determines whether the tile can be affected by flamethrowers
        self.is_cuttable: bool = False  # Determines whether the tile can be affected by an axe
        self.is_water: bool = False  # Determines whether the tile is water
        self.is_pushable: bool = False  # Determines whether the tile is pushable
        self.is_permeable: bool = False  # Determines whether the tile can be passed through

        match tile_type:
            case "~":
                self.is_water: bool = True
                self.is_permeable: bool = True
                self.rep: str = '🟦'  # NOTE: this is blue when I paste in the terminal, but it isn't blue in my IDE (Pycharm)
            case "T":
                self.is_flammable: bool = True
                self.is_cuttable: bool = True
                self.rep: str = '🌲'
            case "R":
                self.pushable: bool = True
                self.rep: str = '🪨'
            case "+":
                self.is_permeable: bool = True
                self.rep: str = '🍄'
            case ".":
                self.is_permeable: bool = True
                self.rep: str = '　'
            case "_":
                self.is_permeable: bool = True
                self.rep: str = '⬜'  # I didn't take this from the projects specs, since the link led nowhere
        
    def get_emoji(self):
        return self.rep
    
    def get_flammable(self):
        return self.is_flammable
    
    def get_cuttable(self):
        return self.is_cuttable
    
    def get_water(self):
        return self.is_water
    
    def get_pushable(self):
        return self.is_pushable
    
    def get_permeable(self):
        return self.is_permeable
    
        

class Item:  # This is for Axe and Flamethrower
    def __init__(self, item_type: str):
        self.item_type: str = item_type
        self.rep: str = None
        self.text_rep: str = None
        self.name: str = None

    def get_name(self):
        return self.name

    def get_emoji(self):
        return self.rep

    def set_name(self, name: str):
        self.name = name

    def set_emoji(self, emoji: str):
        self.rep = emoji


class Laro(Tile):
    def __init__(self, tile_type: str):
        super().__init__(tile_type)
        self.tile_type: str = tile_type
        self.rep: str = '🧑'
        self.text_rep: str = 'L'
        self.coords: tuple = (0, 0)

        self.powerup: Item = None  # Default value of powerup is nothing.

    def get_emoji(self):
        return self.rep
    
    def get_powerup(self):
        return self.powerup
    
    def get_powername(self):
        return self.powerup.get_name() if not (self.powerup is None) else None
    
    def get_powerstr(self):
        return self.powerup.get_emoji() if not (self.powerup is None) else None
    
    def new_powerup(self, powerup, name, emoji):
        self.powerup = powerup
        self.powerup.set_name(name)
        self.powerup.set_emoji(emoji)

    def push(self):
        ...

    def use_powerup(self):
        used_powerup = self.powerup
        self.powerup = None
        return used_powerup


class Axe(Item):
    def __init__(self, item_type: str):
        super().__init__(item_type)
        self.name: str = "Axe"
        self.rep: str = '🪓'
        self.text_rep: str = item_type


class Flamethrower(Item):
    def __init__(self, item_type: str):
        super().__init__(item_type)
        self.name: str = "Flamethrower"
        self.rep: str = '🔥'
        self.text_rep: str = item_type
