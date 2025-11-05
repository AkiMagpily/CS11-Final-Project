class Tile:
    def __init__(self, tile_type: str = None):
        self.tile_type: str = tile_type
        self.rep: str = 'N'  # Actual representation in the grid
        self.text_rep: str = 'N'  # What is being read from the text files

        self.is_flammable: bool = False  # Determines whether the tile can be affected by flamethrowers
        self.is_cuttable: bool = False  # Determines whether the tile can be affected by an axe
        self.is_water: bool = False  # Determines whether the tile is water
        self.is_pushable: bool = False  # Determines whether the tile is pushable
        self.is_permeable: bool = False  # Determines whether the tile can be passed through


class Laro(Tile):
    def __init__(self, tile_type: str):
        super().__init__(tile_type)
        self.tile_type: str = tile_type
        self.rep: str = '🧑'
        self.text_rep: str = 'L'

        self.is_flammable: bool = False
        self.is_cuttable: bool = False
        self.is_water: bool = False
        self.is_pushable: bool = False
        self.is_permeable: bool = False

        self.powerup: str = ''  # Default value of powerup is nothing. Used empty string for it


class Empty(Tile):
    def __init__(self, tile_type: str):
        super().__init__(tile_type)
        self.tile_type: str = tile_type
        self.rep: str = ' '  # I think for empty tiles, we use whitespace? Not sure
        self.text_rep: str = '.'

        self.is_flammable: bool = False
        self.is_cuttable: bool = False
        self.is_water: bool = False
        self.is_pushable: bool = False
        self.is_permeable: bool = True


class Tree(Tile):
    def __init__(self, tile_type: str):
        super().__init__(tile_type)
        self.tile_type: str = tile_type
        self.rep: str = '🌲'
        self.text_rep: str = 'T'

        self.is_flammable: bool = True
        self.is_cuttable: bool = True
        self.is_water: bool = False
        self.is_pushable: bool = False
        self.is_permeable: bool = False


class Mushroom(Tile):
    def __init__(self, tile_type: str):
        super().__init__(tile_type)
        self.tile_type: str = tile_type
        self.rep: str = '🍄'
        self.text_rep: str = '+'

        self.is_flammable: bool = False
        self.is_cuttable: bool = False
        self.is_water: bool = False
        self.is_pushable: bool = False
        self.is_permeable: bool = True


class Rock(Tile):
    def __init__(self, tile_type: str):
        super().__init__(tile_type)
        self.tile_type: str = tile_type
        self.rep: str = '🪨'
        self.text_rep: str = 'R'

        self.is_flammable: bool = False
        self.is_cuttable: bool = False
        self.is_water: bool = False
        self.is_pushable: bool = True
        self.is_permeable: bool = False


class Water(Tile):
    def __init__(self, tile_type: str):
        super().__init__(tile_type)
        self.tile_type: str = tile_type
        self.rep: str = '🟦'  # NOTE: this is blue when I paste in the terminal, but it isn't blue in my IDE (Pycharm)
        self.text_rep: str = '~'

        self.is_flammable: bool = False
        self.is_cuttable: bool = False
        self.is_water: bool = True
        self.is_pushable: bool = False
        self.is_permeable: bool = True


class Paved(Tile):
    def __init__(self, tile_type: str):
        super().__init__(tile_type)
        self.tile_type: str = tile_type
        self.rep: str = '⬜'  # I didn't take this from the projects specs, since the link led nowhere
        self.text_rep: str = '_'

        self.is_flammable: bool = False
        self.is_cuttable: bool = False
        self.is_water: bool = False
        self.is_pushable: bool = False
        self.is_permeable: bool = True