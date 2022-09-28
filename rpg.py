#!/usr/local/bin/python3
"""
rpg.py - entry point for the RPG Game

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin

Assignment completed by Morgan Potter

Gollum ASCII art by Shanaka Dias from ASCII Art Archive. https://www.asciiart.eu/books/lord-of-the-rings
"""

# Importing modules and other game logic.
import time
import gui
import character
import map

# Creates a GUI terminal / app.
app = gui.simpleapp_tk(None)


# Names the game window 'RPG Battle'.
app.title('RPG Battle')

# Printing starting title screen.
app.write('''
 _    _      _                             _         
| |  | |    | |                           | |        
| |  | | ___| | ___  ___  _ __ ___   ___  | |_  ___  
| |/\| |/ _ \ |/ __|/ _ \| '_ ` _ \ / _ \ | __|/ _ \ 
\  /\  /  __/ | (__| (_) | | | | | |  __/ | |_| (_) |
 \/  \/ \___|_|\___|\___/|_| |_| |_|\___|  \__|\___/

____________ _____  ______       _   _   _      _ 
| ___ \ ___ \  __ \ | ___ \     | | | | | |    | |
| |_/ / |_/ / |  \/ | |_/ / __ _| |_| |_| | ___| |
|    /|  __/| | __  | ___ \/ _` | __| __| |/ _ \ |
| |\ \| |   | |_\ \ | |_/ / (_| | |_| |_| |  __/_|
\_| \_\_|    \____/ \____/ \__,_|\__|\__|_|\___(_)
''')
time.sleep(2)
app.write('''
           ___
         .';:;'.
        /_' _' /\   __
        ;a/ e= J/-'"  '.
        \ ~_   (  -'  ( ;_ ,.
         L~"'_.    -.  \ ./  )
         ,'-' '-._  _;  )'   (
       .' .'   _.'")  \  \(  |
      /  (  .-'   __\{`', \  |
     / .'  /  _.-'      ; /  |
    / /    '-._'-,     / / \ (
 __/ (_    ,;' .-'    / /  /_'-._
`"-'` ~`  ccc.'   __.','     \j\L
                 .='/|      
                   ' `

''')
app.write("You can exit the game at any time by typing in 'quit'")
#Creates a space between the next option.
app.write("")


#Selecting the game mode - good or evil.
def set_mode():
  """ Select the game mode """
  # This is an error checking version of reading player input
  # This will be explained in class - pay attention!!
  # Understanding try/except cases is important for
  # verifying player input
  try: # Loads code into different thread, allowing for error exeptions.
    app.write("Please select a side:")
    app.write("1. Good")
    app.write("2. Evil")
    app.write("")
    # Tells the GUI to wait for a player input. 
    app.wait_variable(app.inputVariable)
    #Creates variable for the player input (1, or 2).
    mode = app.inputVariable.get()
    
    # Checks if the player wishes to quit, and exits the program.
    if mode == 'quit':
      app.quit()
    # Checks if the input is within the options and if not, raises a ValueError.
    mode = int(mode)
    if mode not in range(1,3):
      raise ValueError
  
  # If a value error is detected, it re-runs the define statement.
  except ValueError:
    app.write("You must enter a valid choice")
    app.write("")
    mode = set_mode()
  
  # Returns game mode - int(1 or 2) to prompt character race.
  return mode


def set_race(mode):
  """ Set the player's race """
  if mode == 2: # Evil mode.
    app.write("Playing as the legally distinct Forces of Not Sauron.")
    app.write("")
  
    # Race selection - evil.
    try:
      app.write("Please select your race:")
      app.write("1. Goblin")
      app.write("2. Orc")
      app.write("3. Uruk")
      app.write("4. Wizard")
      app.write("")
      app.wait_variable(app.inputVariable) # Waits for a player input.
      race = app.inputVariable.get() # Creates race variable from player input.
      
      # If the player enters 'quit' the program ends.
      if race == 'quit':
        app.quit()
      
      # Checks if the value given is within range of options and if not, raises a ValueError.
      race = int(race)
      if race not in range(1,5):
        raise ValueError
    # If a ValueError is raised from inputting a non-existing option, it re-runs the define statement.
    except ValueError:
      app.write("You must enter a valid choice")
      app.write("")
      race = set_race(mode)

  else: # Good mode.
    app.write("Playing as the legally distinct Free Peoples of Just a Little Up from Middle Earth.") # Prints if the player has chosen 'good' whilst avoiding copyright infringement.
    app.write("")

    # Race selection - good.
    try:
      app.write("Please select your race:")
      app.write("1. Elf")
      app.write("2. Dwarf")
      app.write("3. Human")
      app.write("4. Hobbit")
      app.write("5. Wizard")
      app.write("6. Scout")
      app.write("")
      app.wait_variable(app.inputVariable) # Waits for a player input.
      race = app.inputVariable.get() # Creates a 'race' variable from player input.
      
      # Checks if the player wants to quit - and if so exits the program.
      if race == 'quit':
        app.quit()

      # Checks if the input is within range of possible answers and if not raises a ValueError.
      race = int(race)
      if race not in range(1,7):
        raise ValueError
    
    # If a ValueError is raised, it re-runs the define statement. 
    except ValueError:
      app.write("You must enter a valid choice")
      app.write("")
      race = set_race(mode)
  
  # Returns the player input as a int.
  return race
def set_map():
  ''' Returns the size of the map '''
  app.write("Map size 4-30 (must be an even number): ")
  app.write("")    
  app.wait_variable(app.inputVariable)
  size = app.inputVariable.get()  

  try:
    size = int(size)
    if size not in range(4, 31): # Checks if the input is within the given range of 4-30
      app.write("Map size not in range 4-30.")
      app.write("")
      raise TypeError
    if size % 2 != 0: # Raises a TypeError if the input is not an even number
      app.write("Not an even number.")
      app.write("")
      raise TypeError
  except TypeError:
    restart = set_map() # Restarts the map if a TypeError is raised.
  return size # Returns the size of the map as an int


def set_name():
  """ Set the player's name """
  try:
    app.write("Please enter your Character Name:")
    app.write("")
    app.wait_variable(app.inputVariable) # Waits for player input.
    char_name = app.inputVariable.get() # Creates variable "char_name" as player input.

    # If the player types 'quit', the program ends.
    if char_name == 'quit':
      app.quit()

      # Raises value error if input is nothing.
    if char_name == '':
      raise ValueError
    
    # If a ValueError is raised, the define statement is re-run.
  except ValueError:
    app.write("")
    app.write("Your name cannot be blank")
    char_name = set_name()

  return char_name # Returns player made name.

# Assigns a character created in character.py.


def create_player(mode, race, char_name):
  """ Create the player's character """
  # Evil
  if mode == 2: # Checks if the player has selected the evil game mode.
    if race == 1:
      player = character.Goblin(char_name, app) # Assigns player variable to class created in character.py - corresponding to the race and game mode previously selected.
    elif race == 2:
      player = character.Orc(char_name, app)
    elif race == 3:
      player = character.Uruk(char_name, app)
    elif race == 4:
      player = character.Wizard(char_name, app)
  # Good
  else: # If the player has not selected the evil mode, they have selected the good mode.
    if race == 1:
      player = character.Elf(char_name, app)
    elif race == 2:
      player = character.Dwarf(char_name, app)
    elif race == 3:
      player = character.Human(char_name, app)
    elif race == 4:
      player = character.Hobbit(char_name, app)
    elif race == 5:
      player = character.Wizard(char_name, app)
    elif race == 6:
      player = character.Scout(char_name, app)
  return player # Returns the player variable. I.e. the player selected character.


def set_difficulty():
  """ Set the difficulty of the game """
  try:
    app.write("Please select a difficulty level:")
    app.write("e - Easy")
    app.write("m - Medium")
    app.write("h - Hard")
    app.write("l - Legendary")
    app.write("i = Impossible")
    app.write("")
    app.wait_variable(app.inputVariable) # Waits for player input.
    difficulty = app.inputVariable.get() # Creates the variable 'difficulty' from player input.
    # Checks if the player wishes to quit the game, if so the program exits.
    if difficulty == 'quit':
      app.quit()
    # Checks if the input is valid, if not it raises a ValueError
    if difficulty not in ['e','m','h','l', 'i'] or difficulty == '':
      raise ValueError
    # If a ValueError is raised, the define statement runs again.
  except ValueError:
    app.write("You must enter a valid choice")
    app.write("")
    difficulty = set_difficulty()

  return difficulty # Returns the player chosen difficulty setting.


def create_enemies(mode, difficulty):
  """ Create the enemies """
  if mode == 2: # If player has selected evil mode - good enemies.
    # Defines a list of good enemies (with totally original names), changing depending on difficulty setting. 
    if difficulty == 'm': # Medium difficulty.
      enemies = [character.Hobbit("Peregron", app), character.Hobbit("Meriaduc", app), character.Scout("Jared.2015", app)]
    elif difficulty == 'h': # Hard difficulty.
      enemies = [character.Scout("__xXxSl4y3rxXx__", app), character.Elf("Legolos", app), character.Human("Boromor", app)]
    elif difficulty == 'l': # Legendary difficulty.
      enemies = [character.Dwarf("Tharin", app), character.Elf("Thranduol", app), character.Wizard("Gandolf", app)]
    elif difficulty == 'e': # Easy difficulty.
      enemies = [character.Hobbit("Frodi", app), character.Hobbit("Som", app)]
    else:
      enemies = [character.Wizard("Gandolf", app), character.Wizard("Radagost", app), character.Wizard("Alator", app), character.Human("Aragarn", app)]

  else: # If player has selected good mode - evil enemies
    # Defines a list of evil enemies (where's azulk and bolg?), which change based on difficulty setting. 
    if difficulty == 'm': # Medium difficulty.
      enemies = [character.Goblin("Azig", app), character.Goblin("Gorkol", app), character.Orc("Sharko", app)]
    elif difficulty == 'h': # Hard difficulty.
      enemies = [character.Orc("Shagrit", app), character.Goblin("Gorbog", app), character.Orc("Lugduf", app)]
    elif difficulty == 'l': # Legendary difficulty.
      enemies = [character.Orc("Grishnikh", app), character.Uruk("Lortz", app), character.Wizard("Sarumon", app)]
    elif difficulty == 'e': # Easy difficulty.
      enemies = [character.Goblin("Azig", app), character.Goblin("Gorkol", app)]
    else:
      enemies = [character.Wizard("Sarumon", app), character.Wizard("Souron", app), character.Uruk("Azalk", app), character.Uruk("Bulg", app)]

  return enemies # Returns enemies based on difficulty and game mode.


def map_complete(grid):
  """ Checks if there is any enemies left on the map """
  remaining_enemies = 0
  for i in grid: # Loops through every tile on the grid (list)
    if i == 'o': # If an enemy is found
      remaining_enemies = remaining_enemies + 1 # Adds a enemy to the counter
  if remaining_enemies == 0:
    return True # Returns true if there is no enemies left - hence the map is complete.
  else:
    return False


def quit_game():
  """ Quits the game """
  try:
    app.write("Play Again? (y/n)")
    app.write("")
    app.wait_variable(app.inputVariable) # Waits for a player input.
    quit_choice = app.inputVariable.get() # Defines variable 'quit_choice' as the player input.
    # If the player input is to 'quit', the program exits.
    if quit_choice == 'quit':
      app.quit()
    # Checks if player input is not 'y' or 'n', or is '' and if so, raises a value error.
    if quit_choice not in 'yn' or quit_choice == '':
      raise ValueError
    # If a ValueError is raised, the define statement is re-run.
  except ValueError:
    app.write("You must enter a valid choice")
    app.write("")
    quit_choice = quit_game() # Re-runs the current define statement.

  return quit_choice # Returns if the player wants to keep playing or not, 'y' or 'n'.

def print_results(): # Prints the result once the player is done playing.
  """ Prints the results of the battle - battles, wins, kills, success rate, avg kills per battle, and player level """
  app.write("Battle over!")
  app.write("No. Battles: {0}".format(str(battles)))
  app.write("No. Wins: {0}".format(wins))
  app.write("No. Kills: {0}".format(kills))
  app.write("Success Rate (%): {0:.2f}%".format(float(wins*100/battles)))
  app.write("Avg. kills per battle: {0:.2f}".format(float(kills)/battles))
  app.write(player.name + "level: " + str(player.level))
  app.write("")

# Defines results as 0 for later use.
battles = 0
wins = 0
kills = 0
y = 0
x = 0


# Defines the constant variables - mode, race and name.
mode = set_mode()
race = set_race(mode)
char_name = set_name()
player = create_player(mode, race, char_name) # Creates a player based on the mode, race, and name.
app.write(player) # Gives a description of the character
app.write("")
player_lost = False # Sets player_lost to false to stop a un-innitialized error from occuring.
while True: # Loops the game


  difficulty = set_difficulty() # asks the player for difficulty
  enemies = create_enemies(mode, difficulty) # creates the enemyies based on the difficulty and mode
  size = set_map() # Obtains the size of the map
  map_sequence = map.Map(size, app, player, enemies) # Initializes the map sequence
  grid = map_sequence.generate_map() # Generates the map grid

  while map_complete(grid) != True and player_lost != True: # Loops over the map sequence until all enemies on the map are vanquished
    grid, battles, battle_wins, battle_kills, y, x, player_lost, has_fled = map_sequence.start_map(grid, battles, y, x) # This completes when a battle on the map is completed
    battles += 1
    wins += battle_wins 
    kills += battle_kills
    if player_lost == False and has_fled == False: # Checks if the player has won (hasn't fled, and hasn't lost)
      app.write("You gained 50 experience points for winning!")
      time.sleep(0.5)
      app.write("You gained 20 gold for winning!")
      time.sleep(0.5)
      player.experience += 50 # Adds 50 experience to the player for winning
      player.gold += 20 # Adds 20 gold to the player for winning
      player.check_player_level() # Checks if the player has leveled up
      for enemy in enemies:
        enemy.reset() # Resets all enemies
    print_results() # Prints the results of the battle

  
  # Prompts the player to quit the game, and creates the variable 'quit' based on the result of the define statement 'quit_game' above.
  quit = quit_game()

  # Checks if the player has chosen to quit, and if so, exits the program.
  if quit == "n":
    app.write("Thank you for playing RPG Battle.")
    time.sleep(2) # Gives the player 2 seconds to read the message above.
    app.quit()

  else:
    # Playing again - resets the map, enemies, players, and player_lost.
    x = 0
    y = 0
    grid = 0
    player_lost = False
    map_sequence = None
    player.reset()
    for enemy in enemies:
      enemy.reset()
    
