class Grid:
    def __init__(self, filepath: str):
        # IMPORTANT NOTE FROM BARKIA: We should create a separate list of lists that contains tile_objects
        # self.text_grid is simply the text representation
        # We might also consider a representation that doesn't use text but rather the actual icons
        # ANOTHER IMPORTANT NOTE FROM BARKIA: this is the filepath im currently using: 'levels/test.txt'
        # This is a relative filepath, which is not good to use. We should change it eventually 
        self.text_grid: list[str, ...] = []
        self.filepath: str = filepath
        self.make_grid(filepath)

    def make_grid(self, filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for row in lines:
                self.text_grid.append([])
                placeholder_list = []
                for char in row:
                    placeholder_list.append(char)
                self.text_grid[-1] = ''.join(placeholder_list).strip()

    def __repr__(self):
        return f'text representation of the grid: {self.text_grid}'




# Remove this stuff below when done with testing
test = Grid('levels/test.txt')
print(repr(test))