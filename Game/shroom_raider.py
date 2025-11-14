from classes import *
import os
import sys

def delete_last_line():
    # deletes the last line in the terminal
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')


def clear():
    # clears the terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def game_loop(path, *new_move):
    """
    Main game logic
    Prints the game screen: Grid, Mushroom collected, Powerup on hand, Powerup on tile, Possible moves, reset stage, main menu
    calls game_loop() when stage is reset
    calls post_level() if Laro wins or loses
    if the move sequence has an "!" in between moves, it calls game_loop(path, new_move), where new_move are the moves after the "!"
    """
    game_map = Grid(path)
    global mushrooms_collected
    mushrooms_collected = 0
    global status
    status = "alive"  # Could be win (if laro acquires all mushrooms), lose (if laro falls underwater), or alive

    def get_laro_coords():
        # gets Laro's coords relative to the Grid
        i, j = len(game_map.emoji_grid), len(game_map.emoji_grid[0])
        for I in range(i):
            for J in range(j):
                if game_map.emoji_grid[I][J][-1] == '🧑':
                    return (I,J)
    
    def get_tile_powerup():
        # gets the powerup on the tile Laro is on
        start_coords = list(get_laro_coords())
        start_tile = game_map.emoji_grid[start_coords[0]][start_coords[1]]
        if '🔥' in start_tile:
            return "Flamethrower"
        elif '🪓' in start_tile:
            return "Axe"
        else:
            return "None"

    def get_mushroom_count():
        # get the total mushroom count in the level
        temp = 0
        for row in game_map.text_grid:
            for col in row:
                if col[-1] == "+":
                    temp += 1
        return temp

    def print_map():
        # prints the map
        for row in game_map.emoji_grid:
            for col in row:
                print(col[-1], end="")
        print("")

    def fire_traverse(coords: list[int, int], grid):
        # gets all the adjacent trees to a chosen tree, and deletes them all
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
        # processes each move made: UP, DOWN, LEFT, RIGHT, PICKUP, RESET
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

            if status == 'win' or status == 'lose':
                break

    laro_coords = get_laro_coords()
    mushroom_total = get_mushroom_count()

    if len(new_move) == 1:
        process_move(new_move[0])

    emcii = {'🌲': 'T', '🪨': 'R', '　': '.', '⬜': '_', '🧑': 'L', '🟦': '~', '🍄': '+', '🪓': 'x', '🔥': '*', '\n': '\n'}
    while True:
        if len(sys.argv) > 4:  # If the input in cmd is of the form: python -f <stage> -m <string>, this executes
            sys.argv = sys.argv[1:]
            move = str(sys.argv[3])
        else:
            clear()
            print_map()
            print(f"Mushrooms collected {mushrooms_collected}/{mushroom_total}")
            print(f'Current power up equipped: {game_map.laro.get_powername()}')
            print(f"Power up on tile: {get_tile_powerup()}")
            print("""Moves available: \n[W/w] Move Up \n[A/a] Move Left \n[S/s] Move Down \n[D/d] Move Right \n[P/p] Pickup item on current tile \n[!]   Reset the stage \n""")

            move = input("Input next moves: ").strip()
        if '!' in move:
            new = move.rpartition("!")
            game_loop(path, new[2])
            break
        else:
            process_move(move)

        if len(sys.argv) > 5:
            if status == "win":
                with open(sys.argv[-1], "w") as f:
                    f.write(f'CLEAR \n')
                    f.write(game_map.first_line)
                    for row in game_map.emoji_grid:
                        f.write(''.join(emcii[i[-1]] for i in row))
                break
            else:
                with open(sys.argv[-1], "w") as f:
                    f.write(f'NO CLEAR \n')
                    f.write(game_map.first_line)
                    for row in game_map.emoji_grid:
                        f.write(''.join(emcii[i[-1]] for i in row))
                break
        else:
            if status == "win":
                clear()
                print_map()
                print(f"Mushrooms collected {mushrooms_collected}/{mushroom_total}")
                print(f'Current power up equipped: {game_map.laro.get_powername()}')
                print(f"Power up on tile: {get_tile_powerup()}")
                print("You win!")
                break
            elif status == "lose":
                clear()
                print_map()
                print(f"Mushrooms collected {mushrooms_collected}/{mushroom_total}")
                print(f'Current power up equipped: {game_map.laro.get_powername()}')
                print(f"Power up on tile: {get_tile_powerup()}")
                print("You lose! :(")
                break


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        game_loop("../Game/levels/test.txt")
    elif len(sys.argv) > 2:
            game_loop(str(sys.argv[2]))
