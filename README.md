# CS11-Final-Project

This is the main source code of the CS11 Final Group Project consisting of the members:  
Christopher Akira S.A. Magpily  
John Brandon C. Julian  
Syed Barkia N. Hashemi Nik  

## User Manual:

### To run the game:

1. Navigate to the folder that contains shroom_raider.py
2. Click the address bar and copy the filepath
3. (Windows) Click the Windows button and search for Command Prompt
4. Type in `cd <the filepath that you copied>`
5. Type in `python3 shroom_raider.py`
6. If you get an error saying you don't have python installed, type `python3` instead. This will redirect you to a page where you can install python. Once done, return to step 5

Once you run the game, you start out at the Level Select screen.  
Just type in the number of the level you want to play and press enter*.  
Once you're in the level, you have the following controls:  

`W/w` Move Up  
`A/a` Move Left  
`S/s` Move Down  
`D/d` Move Right  
`P/p` Pickup item on current tile  
`!`   Reset the stage  

The goal of the game is to collect all the mushrooms in the map.  
Be careful of water because Laro is not a great swimmer!  
There are powerups scattered across the maps which can help Laro collect the mushrooms.  

Once you win(or die) you can reset the stage by entering `!` or go back to the Level Select by entering `L/l`

*If you play the bonus version of the game, you don't have to enter your moves in. Simply press the controls you want to use.  
You also need to run the following commands if you want to play the bonus version of the game:
- `python3 -m pip install termcolor`
- `python3 -m pip install keyboard`

## Code Details:

For code organization:  
`shroom_raider.py` contains our main functions and the `Grid` class, then we have `tiles.py` which contains the `Tile` class and the `Laro`, `Axe`, and `Flamethrower` subclasses.  

For code implementation:
The game starts out with the `level_select()` function, which lets the player select what level to play.*  
Then `game_loop(path)` gets invoked, with `path` being the filepath of the level chosen by the player.  
Once in `game_loop(path)`, the game creates a `Grid` object.  

The `Grid` object has a List of Lists of Lists of Strings. The first List for the entirety of the Grid, the Lists inside that for each row, and the Lists inside those for each square.  
Each innermost List may contain any number of Strings consisting of emojis. The Strings represent the objects within that coorinate.
Once the `Grid` is created, the total number of mushrooms to collect is also determined. This is done by iterating through the entire `Grid` and counting the number of mushroom emojis.  

The game now enters a `while True` loop which only `break`s when Laro wins or dies.  
While in the `while True` loop, the game takes the input of the player, and passes it to the `process_move(move_seq)` function.  
`process_move(move_seq)` has a `for char in move_seq` loop to account for multiple moves being passed at once.

The `process_move(move_seq)` function then checks for the coordinates of Laro, then, depending on which direction the next move is, it looks at the contents of the next two tiles in that direction of Laro and determines if the move is valid. (e.g. if the next time is empty, Laro can move there; if the next tile is a rock and the tile after that is water, the rock moves into the water and turns into a paved tile.)

If the move is valid, the emojis in the relevant tiles are then removed and appended depending on the move. (e.g. if the next tile contains rock and the next next tile contains water, Laro is removed from the current tile, the rock is removed from the next tile, Laro is appended to the next tile, the water is removed from the next next tile, and a paved tile is appended into the next next tile)

If the move is `P`, the game first checks if Laro has no current powerup. Then, if he has no powerup, he pickup the powerup on the ground.

If Laro moves into a Tree while holding a powerup, either only the Tree he moved to is removed or every Tree adjacent to that Tree is also removed depending on Laro's current powerup. Then, Laro's current powerup is set to `None`

Once Laro collects all mushrooms or falls into water, the `while True` loop is broken and `post_level()` is called.

If the move is `!`, `game_loop(path)` is simply called again.

In `post_level()` the player can either reset the stage, or go back to the Level Select screen.

In the bonus version of the game, pressing `E/e` anywhere exits the game using `sys.exit()`

*`level_select` only exists in the bonus version

## Unit Tests:

hello barkia  

## Bonus Features:

- Fancier user interface. (the game is centered in the terminal, ascii art)
- Added a Level Select screen
- Added post level actions
- Ability to exit the game or program via a command.
- Colored terminal text using `termcolor`
- Automatic keyboard input

## Citations:
- w3schools