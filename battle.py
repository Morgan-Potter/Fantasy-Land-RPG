#!/usr/local/bin/python3
"""
Battle.py - The battle class manages the events of the battle

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin

Assignment completed by Morgan Potter
"""

# Import required python modules.
import sys
import time
import random



class Battle:

  def __init__(self, player, enemies, app, powerup_modifier):
    """
    Instantiates a battle object between the players and enemies specified,
    sending output to the given gui instance
    """
    self.player = player
    self.enemies = enemies
    self.app = app
    self.turn = 1
    self.wins = 0
    self.kills = 0
    self.player_won = False
    self.player_lost = False
    self.has_fled = False
    self.powerup_modifier = powerup_modifier

  def play(self):
    """
    Begins and controls the battle
    returns tuple of (win [1 or 0], no. kills)
    """
    
    while not self.player_won and not self.player_lost: # While the player has not won and has not lost.
      
      self.app.write("Turn "+str(self.turn))
      self.app.write("")
      time.sleep(1)
      
      # This is where the bulk of the battle takes place
      self.do_player_actions()
      self.do_enemy_actions()
      self.find_item()
      
      # advance turn counter
      self.turn += 1
      
    return (self.wins, self.kills) # Returns the battle kills and wins

  def find_item(self):
    """
    Rolls for an item after every turn. Returns true if an item is found.
    """
    item = 0
    roll = random.randint(1, 15) # rolls for a chance of getting an item

    if roll == 15:
    
      bundle = random.randint(1, 2) # Rolls for 1 or 2 items.

      while True: # Loops until the random item is applicable to the player
        item = random.randint(1, 4) # Randomly changes the item number of 1-4 (all possible items)
        if self.player.valid_item(item): # Checks if the item is applicable to the player

          if item == 1: # If the item is a health potion

            if bundle == 1: # If you are granted 1 potion
              self.app.write("A wizard granted you a healing potion!")
              self.app.write("")
              time.sleep(1)
              self.player.health_potions =+ 1 # Increase the potion count by one
              return True
            if bundle == 2: # If you are granted 2 potions
              self.app.write("A wizard granted you a bundle of healing potions!")
              self.app.write("")
              time.sleep(1)
              self.player.health_potions += 2 # Increase the potion count by one
              return True

          if item == 2: # If it is a mana potion.
            if bundle == 1:
              self.app.write("A wizard granted you a mana potion!")
              self.app.write("")
              time.sleep(1)
              self.player.mana_potions =+ 1
              return True
            if bundle == 2:
              self.app.write("A wizard granted you a bundle of mana potions!")
              self.app.write("")
              time.sleep(1)
              self.player.mana_potions += 2
              return True

          if item == 3: # If it is a strength potion.
            if bundle == 1:
              self.app.write("A wizard granted you a strength potion!")
              self.app.write("")
              time.sleep(1)
              self.player.strength_potions =+ 1
              return True
            if bundle == 2:
              self.app.write("A wizard granted you a bundle of strength potions!")
              self.app.write("")
              time.sleep(1)
              self.player.strength_potions += 2
              return True

          if item == 4: # If it is a battle axe
            self.app.write("The elden Orc wizard granted you a battle axe!")
            self.player.axe_durability = self.player.starting_axe_durability # Change the battle axe durability to the starting durability
            return True
    else:
      return False # If the roll fails, return False

  def get_action(self): 
    """ Gets the player's chosen action for their turn """
    try:
      self.app.write(self.player.name + "'s Turn:")
      self.app.write("1. Attack Enemies")
      self.app.write("2. Cast Magic")
      self.app.write("3. Open Inventory")
      self.app.write("4. Flee")
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      player_action = self.app.inputVariable.get()

      if player_action == 'quit': # If the player chooses to quit - exit the app
        self.app.quit()

      player_action = int(player_action)
      if player_action not in range(1,5): # If the input is not 1-4.
        raise ValueError

    except ValueError: # Restarts the define statement if a ValueError occurs
      self.app.write("You must enter a valid choice")
      self.app.write("")
      player_action = self.get_action()
    
    return player_action # Returns player_action as an int.
  
  def fleeing_roll(self): 
    """ Returns True if a player has succesfully fled, and false if not. """
    race = self.player.__class__.__name__ # Creates a variable for the player race.

    # There are varying levels of difficulty to flee depending on what character you have chosen.
    if race == "Wizard":
      flee = random.randint(0, 6)
    elif race == "Goblin" or "Orc" or "Human" or "Elf":
      flee = random.randint(0, 3)
    elif race == "Uruk" or "Dwarf": # Urukai and Dwarves are slow, so it is harder for them to flee
      flee = random.randint(0, 5)
    elif race == "Scout" or "Hobbit":
      flee = random.randint(0, 2)
    else:
      flee = random.randint(0, 4) # If the character was not listed, a average speed is give. 

    if flee in range(0, 2): # If the randomly generated input is 0 or 1, return True
      self.player_won = True
      return True
    else:
      return False # Returns false if the integer is not 0 or 1.
  def select_item(self):
    """ Returns item the player has selected as an int.  """
    player_race = self.player.__class__.__name__
    try:
      # Shows items in the players inventory if they are available to the player. If the player race is not an orc, the orc battle axe will not be shown.
      self.app.write("Select your item:")
      if self.player.health_potions > 0: # If the player is carrying any health potions. 
        self.app.write("1. Health Potion (restores 250hp)")
      if self.player.mana_potions > 0: # If the player is carrying any mana potions.
        self.app.write("2. Mana Potion (restores 50mp)")
      if self.player.strength_potions > 0: # If the player is carrying any strength potions
        self.app.write("3. Strength Potion (next attack does triple damage)")
      if player_race == "Orc": # If the player race is an orc and if they have axe durability.
        if self.player.axe_durability > 0:
          self.app.write("4. Orc Battle Axe (decapitates enemy, 5 durability)")
      if player_race == "Uruk" and self.player.level > 1: # If the player race is Urukai and their level is bigger or equal to 2.
        if self.player.axe_durability > 0:
          self.app.write("4. Uruk Battle Axe (decapitates enemy, 3 durability)")
      self.app.write("0. Cancel Inventory")
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      item_choice = self.app.inputVariable.get() # Item_choice becomes the players input


      if item_choice == 'quit': # If the player wishes to quit -> quit. 
        self.app.quit
      item_choice = int(item_choice)

      valid_item = self.player.valid_item(item_choice) # Checks if the item is valid in case of a miss-input (we wouldn't want hobbits to be able to use a orc battle axe).

      if valid_item != True: # If the item is not a valid choice, raise a ValueError
        raise ValueError

      if item_choice not in range(0, 5): # If the input is not an option, raise a ValueError.
        raise ValueError

      if item_choice == 0: # If the item choice is 0 (cancel inventory), return false
        return False

    except ValueError: # If a ValueError is raised, post an error message and re-run the define statement.
      self.app.write("Please enter a valid choice")
      item_choice = self.select_item()
    return item_choice # Returns the players choice of item

  def select_spell(self):
    """ Selects the spell the player would like to cast """
    player_race = self.player.__class__.__name__

    try:
      # Only shows options to the player if they are capable of using that spell.
      self.app.write("Select your spell:")
      if player_race == "Scout" and self.player.mana >= 5:
        self.app.write("1. Scattergun (5 mp)")
      if player_race == "Wizard" and self.player.mana >= 10:
        self.app.write("1. Fireball (10 mp)")
      if self.player.mana >= 20:
        self.app.write("2. Shield (20 mp)")
      if player_race == "Wizard":
        self.app.write("3. Mana Drain (no mp cost)")
      self.app.write("0. Cancel Spell")
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      spell_choice = self.app.inputVariable.get() # player input becomes spell_choice

      if spell_choice == 'quit': # If the player wishes to quit, exit the app
        self.app.quit()

      spell_choice = int(spell_choice) 

      if spell_choice == 0: # If the spell choice is 0 (cancel spell), return false (not used).
        return False

      valid_spell = self.player.valid_spell(spell_choice)

      if not valid_spell: # If the spell is not applicable to the current character, raise a ValueError
        raise ValueError

    except ValueError: # If a Value Error is raised, restart the define statement
      self.app.write("You must enter a valid choice")
      self.app.write("")
      spell_choice = self.select_spell()
    
    return spell_choice # Returns the players spell choice as an int.

  def choose_target(self):
    """ Selects the target of the player's action """
    try:
      self.app.write("Choose your target:")
      # use j to give a number option
      j = 0
      while j < len(self.enemies): # Loops until there is no enemies left
        if self.enemies[j].health > 0: # If the enemy is not dead
          self.app.write(str(j) + ". " + self.enemies[j].name) # Writes the enemy number and the enemies name. e.g. "1. Azig".
        j += 1 # Adds a counter for every enemy (number option)

      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      target = self.app.inputVariable.get() # Target becomes the player input

      if target == 'quit': # If the player wishes to quit, exit the app instance.
        self.app.quit()

      target = int(target)
      if not (target < len(self.enemies) and target >= 0) or self.enemies[target].health <= 0: # If the input is not an enemy (not bigger than the last enemy or smaller than the first (0)), or if the chosen enemy is dead; raise a value error.
        raise ValueError

    except ValueError: # If a value error occurs, restart the define statement.
      self.app.write("You must enter a valid choice")
      self.app.write("")
      target = self.choose_target()

    return target # Return the chosen target as an int.

  def choose_stance(self):
    """ Obtains the players stance, and returns a, d, or b """
    try:
      self.app.write("Choose your stance:")
      self.app.write("a - Aggressive")
      self.app.write("d - Defensive")
      self.app.write("b - Balanced")
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      stance_choice = self.app.inputVariable.get() # The player input becomes stance_choice

      if stance_choice == 'quit': # If the player wishes to quit, exit the app.
        self.app.quit()

      if stance_choice not in ['a','d','b'] or stance_choice == '': # If the player input is not a, d, or b, or stance_choice is nothing - raise a value error.
        raise ValueError

    except ValueError: # If a value error is raised, restart the define statement
      self.app.write("You must enter a valid choice")
      self.app.write("")
      stance_choice = self.choose_stance()
    
    return stance_choice # Returns the player chosen stance.

  def do_player_actions(self):
    """ Performs the player's actions """
  
    turn_over = False # Initialises turn_over
  
    while not self.player_won and not turn_over: # While the player has not won and the players turn is not complete.

      self.player.print_status() # Prints key player information - health, mana, experience, shield, and items.

      stance_choice = self.choose_stance() # Obtains the players stance choice, (a, b, or d)

      self.player.set_stance(stance_choice) # Sets attack modifiers based on stance choice in character.py.
      
      player_action = self.get_action() # Gets the player action as an int.

      has_attacked = False


      if player_action == 4: # If the player wishes to flee
        self.has_fled = self.fleeing_roll() # Returns if the player has fled succesfully as true or false.

        if self.has_fled == True: # If the player flees succesfully, inform the player
          self.app.write("You fled the battle.")
          self.app.write("")
          time.sleep(1)

        else: # If the player fails to flee, take the players turn.
          self.app.write("You were too slow.")
          self.app.write("")
          time.sleep(1)
          has_attacked = True # Takes the players attacking turn.


      elif player_action == 3: # If the player wishes to use their inventory
        item_choice = self.select_item() # Prompts the player to open their inventory

        if item_choice != False: # If the player does not wish to cancel their inventory
          has_attacked = True # Take the players turn

          if item_choice == 1: # If the player wants to use a health potion -> use a health potion
            self.player.use_health_potion()

          elif item_choice == 2: # If the player wants to use a mana potion -> use a mana potion
            self.player.use_mana_potion()

          elif item_choice == 3: # If the player wants to use a strength potion -> use a strength potion
            self.player.use_strength_potion()

          elif item_choice == 4: # If the player wants to use a battle axe
            target = self.choose_target() # Choose the target
            self.player.use_battle_axe(self.enemies[target], self.powerup_modifier) # Use the battle axe

    
      elif player_action == 2: # IF the player wants to use a spell
        spell_choice = self.select_spell()

        if spell_choice != 0: # If the player does not want to cancel the spell. 
          has_attacked = True
          if spell_choice == 1 or spell_choice == 3: # If the player wishes to use a fireball, scattergun or mana drain spell.
            target = self.choose_target() # Choose the target
            if self.player.cast_spell(spell_choice, self.enemies[target]): # Runs the spell, If the player kills someone with the spell, add a kill to the counter.
              self.kills += 1
          else:
            self.player.cast_spell(spell_choice) # If the spell does not require a target (sheild), cast it.

         
      else: # If the player action is the attack the enemy
        target = self.choose_target() # Choose the target
        has_attacked = True
        turn_outcome = self.player.attack_enemy(self.enemies[target], self.powerup_modifier) # Attack the chosen enemy, return if the player kills the enemy

        if turn_outcome != "counter": # If the enemy does not kill the player with a counter attack
          if turn_outcome: # If the player kills an enemy
            self.kills += 1
        else: # If the enemy kills the player with a counter attack
          self.player_lost = True # The player has lost

    
      turn_over = True # The turn is over.
      if not has_attacked: # If the player has not attacked, the turn is not over
        turn_over = False

      else: # If the player has attacked     
        self.player_won = True
        for enemy in self.enemies:
          if enemy.health > 0: # If all the enemies are not dead
            self.player_won = False # The player has not won.
            break

        if self.player_won == True: # If all the enemies are dead
          self.app.write("Your enemies have been vanquished!!")
          self.app.write("")
          time.sleep(1)
          self.wins += 1 # Add a win to the counter.

  def do_enemy_actions(self):
    """ Performs the enemies' actions """

    turn_over = False
    
    if not self.player_won: # If the player has killed all the enemies
      self.app.write("Enemies' Turn:")
      self.app.write("")
      time.sleep(1)
    
      for enemy in self.enemies: # Goes through all the enemies
        if enemy.health > 0 and not self.player_lost: # If an enemy is alive, and the player has not lost, begin the enemies turn.

          if not self.player_lost: # (coding error)
            self.player_lost = enemy.move(self.player) # Self.player_lost becomes True if the enemy kills the player, and false if the player lives.

      if self.player_lost == True: # If the enemy kills the player
        self.app.write("You have been killed by your enemies.")
        self.app.write("")
        time.sleep(1)

      elif self.player_lost == "counter": # If the player kills the enemy with a counter attack
        self.player_lost = False # The player has not lost the game