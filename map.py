#!/usr/local/bin/python3
"""
map.py - runs the map and starts battles

Written by Morgan Potter

An addition to the code written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014 - modified with permission by Edwin Griffin.

ASCII art made by Phillip Kaulfuss, at ASCII Art Archive. https://www.asciiart.eu/people/occupations/ascii-art-artists
"""

# Imports necessary modules.
import random
import time
import battle

class Map:

    def __init__(self, size, app, player, enemies): # Takes the variables created in rpg.py and initializes them
        self.size = size
        self.app = app
        self.player = player
        self.enemies = enemies
        self.map = []
        self.powerup_modifier = 0
    def generate_map(self): # Generates the map using the size given in rpg.py
        """ Generates and returns the map grid with random enemies, and powerups. """
        try:
            grid = int(self.size)
            battles = random.randint(2, (self.size / 2)) # Randomly generates a number of enemies
            powerups = random.randint(1, (self.size / 2)) # Randomly generates a number of powerups
            grid = list(grid * '.' * grid)
            grid[0] = 'x' # Marks the players starting position
            for i in range(powerups):
                grid[random.randint(1, (len(grid) - 1))] = '#' # Randomly places the powerups on the grid
            for i in range(battles):
                grid[random.randint(1, (len(grid) - 1))] = 'o' # Randomly places the enemies on the map
            grid[random.randint(1, (len(grid) - 1))] = 'S' # Randomly places a merchant trader on the map
        except TypeError:
            restart = Map.generate_map()
        return grid # Retruns the grid as a list

    def valid_shop(self, shop_choice):
        ''' Checks to see if the player can buy the chosen shop item and if they have enough gold. '''
        player_race = self.player.__class__.__name__ # Makes a variable for the player race

        valid = False

        if self.player.gold >= 10: # Health and mana potions:
            if shop_choice == 1 and self.player.starting_health_potions > 0:
                valid = True
            if shop_choice == 2 and self.player.starting_mana_potions > 0:
                valid = True
        if shop_choice == 3 and self.player.starting_strength_potions > 0 and self.player.gold >= 15: # Strength potions
            valid = True
        if shop_choice == 4 and player_race == 'Orc' and self.player.gold >= 20: # Orc Battle Axe

            valid = True
        if self.player.level > 1: # Uruk battle axe and Attack Powerup
            if player_race == "Uruk" and shop_choice == 4 and self.player.gold >= 20:
                valid = True
            if shop_choice == 5 and self.player.gold >= 25:
                valid = True
        
        return valid




    def open_shop(self):
        ''' Opens shop and lists the item options depending on if the player starts with an item. Adds the items and returns True. Returns False if the player exits. '''
        try:
            player_race = self.player.__class__.__name__
            self.app.write("""
                    ,'" __`.,'"`.
            ,;,,'" _`Y'"`.\\
        //// ,'"'`Y'"`.\YY
        ffffff'    '   'Y||
        |||||l ,--   --.|||
        jjj|l`  ,-.  ,-.|ll
        ,-```  f  | f  ||-.
        l (|   l_0, l_0,| j 
        Y |       `.   |f 
        `-|,        )  l' 
        ||f ,-  `--'  _ Y
        jjj  `.       ,`|
        '''\   `-----'  j
            |.        ,' 
            | `-._.,-' 
        ____ |      l ____  """)
            time.sleep(1)
            self.app.write("Hello young adventurer.")
            time.sleep(1)
            self.app.write("Welcome to my store!")
            time.sleep(1)

            if self.player.gold < 10:
                self.app.write("Oh my! Looks like you don't have enough gold to buy anything. Come again later!")
                time.sleep(1)
                return False

            self.app.write("Please, take a look at my amazing selection of items:")
            time.sleep(1)
            if self.player.starting_health_potions > 0 and self.player.gold >= 10: # If the player starts with health potions
                self.app.write("1. Health Potion -> 10g")
            if self.player.starting_mana_potions > 0 and self.player.gold >= 10: # If the player starts with mana potions
                self.app.write("2. Mana Potion -> 10g")
            if self.player.starting_strength_potions > 0 and self.player.gold >= 15: # If the player starts with strength potions
                self.app.write("3. Strength Potion -> 15g")
            if player_race == "Orc" and self.player.gold >= 20: # If the player has an orc battle axe
                self.app.write("4. Orc Battle Axe -> 20g") 
            if player_race == "Uruk" and self.player.level > 1 and self.player.gold >= 20: # If the player has an Uruk battle axe
                self.app.write("4. Uruk Battle Axe -> 20g")
            if self.player.level > 1 and self.player.gold > 25: # If the player is level 2 or higher
                self.app.write("5. Attack Powerup -> 25g")
            self.app.write("0. Leave Merchant Trader")
            self.app.wait_variable(self.app.inputVariable)
            shop_choice = self.app.inputVariable.get()
            shop_choice = int(shop_choice)
      
            bought_item = False

            if shop_choice == 'quit': # If the player wishes to quit, quit
                self.app.quit()
            
            if shop_choice == 0: # If the player wishes to cancel the shop, exit
                self.app.write("Thanks for coming!")
                return False
            
            if self.valid_shop(shop_choice) == False: # Makes sure the player has made a valid choice
                raise ValueError

            if shop_choice == 1: # If the player wants to buy a health potion
                bought_item = True
                self.player.gold -= 10 # Subtract the gold
                self.player.health_potions += 1 # Add the health potion
                self.app.write("You bought a health potion")
                time.sleep(0.5)
                self.app.write("You have " + str(self.player.gold) + " gold left")
                time.sleep(0.5)

            if shop_choice == 2: # If the player wants to buy a mana potion
                bought_item = True
                self.player.gold -= 10 # Subtract the gold
                self.player.mana_potions += 1 # Add the mana potion
                self.app.write("You bought a mana potion")
                time.sleep(0.5)
                self.app.write("You have " + str(self.player.gold) + " gold left")
                time.sleep(0.5)

            if shop_choice == 3: # If the player wants to buy a strength potion
                bought_item = True
                self.player.gold -= 15 # Subtract the gold
                self.player.strength_potions += 1 # Add the strength potion
                self.app.write("You bought a strength potion")
                time.sleep(0.5)
                self.app.write("You have " + str(self.player.gold) + " gold left")
                time.sleep(0.5)

            if shop_choice == 4: # If the player wants to buy a battle axe
                bought_item = True
                self.player.gold -= 20 # Subtract the gold
                self.player.axe_durability = self.player.starting_axe_durability # Restore the axe durability
                self.app.write("You bought a battle axe")
                time.sleep(0.5)
                self.app.write("You have " + str(self.player.gold) + " gold left")
                time.sleep(0.5)

            if shop_choice == 5: # If the player wants to buy an attack powerup
                bought_item = True
                self.player.gold -= 25 # Subtract the gold
                self.powerup_modifier += 1.2 # Add to the powerup modifier
                self.app.write("You bought an attack powerup")
                time.sleep(0.5)
                self.app.write("You have " + str(self.player.gold) + " gold left")
                time.sleep(0.5)

        except ValueError: # If a value error is raised, restart the shop
            self.app.write("I'm afriad you can't buy that item.")
            time.sleep(0.5)
            bought_item == self.open_shop()

        return bought_item # Returns True if the player bought an item
    def move_enemies(self, grid):
        ''' Randomly moves the enemies on the map and returns the new grid '''
        for i in range(len(grid)):
            if grid[i] == 'o':
                enemy_x = i % self.size
                enemy_y = int((i - enemy_x) / self.size)
                direction = random.randint(1, 4)
                try: 

                    if enemy_y != 0 and direction == 1:
                        if grid[(enemy_y + 1) * self.size + enemy_x] == '.': # On a seperate line so that an index error wont occur every time if the enemy is in the bottom right.
                            grid[i] = '.'
                            grid[(enemy_y - 1) * self.size + enemy_x] = 'o'

                    if enemy_y != (self.size - 1) and direction == 2:
                        if grid[(enemy_y + 1) * self.size + enemy_x] == '.': # Not in one line so an index error wont occur every time.
                            grid[i] = '.'
                            grid[(enemy_y + 1) * self.size + enemy_x] = 'o'

                    if enemy_x != 0 and direction == 3:
                        if grid[i - 1] == '.':
                            grid[i] = '.'
                            grid[i - 1] = 'o'

                    if enemy_x != (self.size - 1) and direction == 4:
                        if grid[i + 1] == '.':
                            grid[i] = '.'
                            grid[i + 1] = 'o'
                except IndexError: # An index error occurs if the enemy is in the very bottom right corner. 
                    grid = self.move_enemies(grid)
        return grid

    def start_map(self, grid, battles, y, x):
        """ Starts the map movement process. Once an enemy is found, the battle sequence is started. Returns a plethera of variables to integrate with rpg.py. """
        o = 0
        line = ''
        move = ''
        try:
            for i in grid: # Prints the starting grid by cycling through each line and printing them individually.
                o = o + 1
                line = line + i
                if o >= self.size: 
                    o = 0
                    self.app.write(line)
                    line = ''
            grid[(y * self.size + x)] = '.' # Changes the previous player position to a '.'.(x and y are coordinates)
            while move != 'quit':           # y is the row number, x is the column number.
                self.app.write("Direction (n s e w): ") 
                self.app.write("")
                self.app.wait_variable(self.app.inputVariable)
                move = self.app.inputVariable.get() # Move is the direction the has input to move

                if move == 'quit': # If the player wishes to quit, then quit.
                    self.app.quit()

                # Creates the boundries for the player (x and y are coordinates 0, 0 being the top left)
                if move == 'n' and y == 0: 
                    self.app.write("Cannot travel outside the map!")
                    self.app.write("")
                elif move == 's' and y == (self.size - 1):
                    self.app.write("Cannot travel outside the map!")
                    self.app.write("")
                elif move == 'w' and x == 0:
                    self.app.write("Cannot travel outside the map!")
                    self.app.write("")
                elif move == 'e' and x == (self.size - 1):
                    self.app.write("Cannot travel outside the map!")
                    self.app.write("")
                else:
                    # If player is not travelling out of bounds, change the coordinates based on the player input
                    if move == 'e':
                        x = x + 1
                    elif move == 's':
                        y = y + 1
                    elif move == 'w':
                        x = x - 1
                    elif move == 'n':
                        y = y - 1  
                    else:
                        self.app.write("Please enter a valid input!") # If the input is not (nsew) tell the player to input correctly
                        time.sleep(1)
                    if grid[(y * self.size + x)] == '.': # If the player coordinates is blank space
                        grid[(y * self.size + x)] = 'x' # Changes the player coordinate to an x
                    elif grid[(y * self.size + x)] == 'o': # if the player landed on a enemy
                        
                        self.app.write("Enemies found!")
                        self.app.write("")
                        time.sleep(1)

                        encounter = battle.Battle(self.player, self.enemies, self.app, self.powerup_modifier) # Initializes the battle sequence, with the powerup modifier
                        battle_wins, battle_kills = encounter.play() # Starts the battle, returning battle_wins and battle_kills

                        if encounter.has_fled == True: # if the player flees the battle
                            grid[0] = 'x' # Sets a player marker at the start of the map (player flees back to the top of the map)
                            return grid, battles, battle_wins, battle_kills, 0, 0, encounter.player_lost, encounter.has_fled # returns the needed variables, setting x and y to 0 (top left of map)

                        if encounter.player_lost == False: # If the player has won the battle
                            grid[(y * self.size + x)] = 'x' # Set the enemy marker to an x, showing the player has won.
                            return grid, battles, battle_wins, battle_kills, y, x, encounter.player_lost, encounter.has_fled # returns the needed variables

                        else: # If the player has lost
                            return grid, battles, battle_wins, battle_kills, y, x, encounter.player_lost, encounter.has_fled # returns the needed variables (prompts player to play again in rpg.py)

                    elif grid[(y * self.size + x)] == '#': # If player lands on a powerup
                        self.powerup_modifier += 0.8 # Increase the players powerup modifier by 0.8
                        self.app.write("You gained a powerup!")
                        time.sleep(0.5)
                        self.app.write("Attack power has been boosted by 80%!")
                        time.sleep(0.5)
                        grid[(y * self.size + x)] = 'x' # Sets the player coordinate to an x

                    elif grid[(y * self.size + x)] == 'S':
                        self.app.write("You found the merchant trader!")
                        self.open_shop()
                        # Move the player back to where they accessed the trader from
                        if move == 'e':
                            x = x - 1
                        elif move == 's':
                            y = y - 1
                        elif move == 'w':
                            x = x + 1
                        elif move == 'n':
                            y = y + 1  
                        grid[(y * self.size + x)] = 'x'

                    if move != 'quit':
                        grid = self.move_enemies(grid)
                        for i in grid: # Prints the grid one line at a time
                            o = o + 1
                            line = line + i
                            if o >= self.size: 
                                o = 0
                                self.app.write(line)
                                line = ''
                        grid[(y * self.size + x)] = '.' # After the grid has been printed, the player marker is reverted to blank space             
        except ValueError: # If a ValueError is raised, the player is prompted to make a valid input and the map restarts.
            self.app.write("Please enter a valid input.")
            time.sleep(1)
            restart = self.start_map(grid, battles, y, x)