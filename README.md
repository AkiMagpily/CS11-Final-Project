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
The game starts out with the `level_select()` function, which lets the player select what level to play.  
Then `game_loop(path)` gets invoked, with `path` being the filepath of the level chosen by the player.  
Once in `game_loop(path)`, the game creates a `Grid` object

## Unit Tests:

hello barkia  

## Bonus Features:

- Fancier user interface. (the game is centered in the terminal)
- Ability to exit the game or program via a command.
- Colored terminal text using `termcolor`
- Automatic keyboard input

## Citations:
- w3schools