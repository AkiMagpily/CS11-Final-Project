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


def game_loop(path):
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
        ...
    
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
test = Grid('levels/test.txt')
print(repr(test))