class Tile:
    def __init__(self, tile_type: str = None):
        self.rep: str = 'N'  # Actual representation in the grid
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
                self.contains: Item = None
            case "_":
                self.is_permeable: bool = True
                self.rep: str = '⬜'  # I didn't take this from the projects specs, since the link led nowhere
                self.contains: Item = None
        
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
    
    def get_item(self):
        return self.contains
        

class Item:  # This is for Axe and Flamethrower
    def __init__(self, item_type: str):
        self.item_type: str = item_type
        self.rep: str = 'N'
        self.text_rep: str = 'N'


class Laro(Tile):
    def __init__(self, tile_type: str):
        super().__init__(tile_type)
        self.tile_type: str = tile_type
        self.rep: str = '🧑'
        self.text_rep: str = 'L'
        self.coords: tuple = (0, 0)

        self.is_flammable: bool = False
        self.is_cuttable: bool = False
        self.is_water: bool = False
        self.is_pushable: bool = False
        self.is_permeable: bool = False

        self.powerup: Item = None  # Default value of powerup is nothing.
        self.powername: str = None
        self.powerstr: str = None

    def get_emoji(self):
        return self.rep
    
    def get_powerup(self):
        return self.powerup
    
    def get_powername(self):
        return self.powername
    
    def get_powerstr(self):
        return self.powerstr
    
    def new_powerup(self, powerup, name, emoji):
        self.powerup = powerup
        self.powername = name
        self.powerstr = emoji
        
    def move(self, move_seq: str):
        valid_input: dict[str, tuple[int, int]] = {'W': (-1, 0), 'A': (0, -1), 'S': (1, 0), 'D': (0, 1)}

        ...

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
    def get_name(self):
        return self.name
    
    def get_emoji(self):
        return self.rep


class Flamethrower(Item):
    def __init__(self, item_type: str):
        super().__init__(item_type)
        self.name: str = "Flamethrower"
        self.rep: str = '🔥'
        self.text_rep: str = item_type
    def get_name(self):
        return self.name
    
    def get_emoji(self):
        return self.rep
