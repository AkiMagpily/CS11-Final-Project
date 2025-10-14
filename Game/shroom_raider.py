class Grid:
    def __init__(self, rows: int, columns: int):
        self.rows: int = rows
        self.columns: int = columns
        self.grid: list[list[str, ...], ...] = [['' for _ in range(self.columns)] for i in range(self.rows)]


class Tile:
    def __init__(self, tile_type: str):
        self.tile_type: str = tile_type


class Laro:
    def __init__(self, powerup: str = None):
        self.powerup = powerup


class Powerup:
    def __init__(self, name: str = None):
        self.name = name


