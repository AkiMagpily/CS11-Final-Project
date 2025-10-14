class Grid:
    def __init__(self, rows: int, columns: int):
        self.rows: int = rows
        self.columns: int = columns


class Tile:
    def __init__(self, tile_type: str):
        self.tile_type: str = tile_type


class Laro:
    def __init__(self, powerup: str = None):
        self.powerup = powerup



