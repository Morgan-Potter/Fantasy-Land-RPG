#!/usr/local/bin/python3
"""
Character.py - Class definition for RPG Characters

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin

Assignment completed by Morgan Potter
"""

# Import required Python modules.
import time
import random
from tkinter.constants import W

######
### Define the attributes and methods available to all characters in the Character
### Superclass. All characters will be able to access these abilities.
### Note: All classes should inherit the 'object' class.
######

class Character:
  """ Defines the attributes and methods of the base Character class """
  
  def __init__(self, char_name, app):
    """ Parent constructor - called before child constructors """
    self.attack_mod = 1.0
    self.defense_mod = 1.0
    self.name = char_name
    self.shield = 0
    self.max_shield = 50
    self.app = app
    self.strength_potion_mod = 0

  def __str__(self):
    """ string representation of character """
    return str("You are " + self.name + " the " + self.__class__.__name__) # Returns a breif description of the character.

  def move(self, player):
    """
    Defines any actions that will be attempted before individual
    character AI kicks in - applies to all children
    """
    move_complete = False

    if self.health < 50 and self.health_potions > 0: # If the enemy has a health potion and it's health is lower than 50

      self.set_stance('d') # Set a defensive stance
      
      self.use_health_potion() # Use a health potion

      move_complete = True # Complete the enemies move


    elif self.mana == 0 and self.mana_potions > 0: # If the enemy has no mana, and has a mana potion

      self.set_stance('d') # Set a defensive stance
      
      self.use_mana_potion() # Use a mana potion

      move_complete = True # Completes the move


    return move_complete # Returns True if the enemy has completed their move, and false if not.

    

#### Character Attacking Actions ####

  def set_stance(self, stance_choice):
    """ sets the fighting stance based on given parameter """

    if stance_choice == "a": # Agressive stance
      self.attack_mod = 1.3 # Sets the attack modifier based on the stance choice.
      self.defense_mod = 0.6 # Sets the defence modifier based on the stance choice.
      self.app.write(self.name + " chose aggressive stance.")

    elif stance_choice == "d": # Defensive stance
      self.attack_mod = 0.6
      self.defense_mod = 1.3
      self.app.write(self.name + " chose defensive stance.")

    else: # Balanced stance
      self.attack_mod = 1.0
      self.defense_mod = 1.0
      self.app.write(self.name + " chose balanced stance.")
    self.app.write("")

  def attack_enemy(self, target, powerup_modifier):
    ''' Attacks the targeted enemy. Accepts a Character object as the parameter (enemy
    to be targeted). Returns True if target killed, False if still alive.'''

    roll = random.randint(1, 20) # Rolls for attack damage
    hit = int(roll * (self.attack_mod + powerup_modifier + self.strength_potion_mod + self.level) * self.attack) # Damage calculation
    self.strength_potion_mod = 0 # Resets the strength potion modifier
    self.app.write(self.name + " attacks " + target.name + ".")
    time.sleep(1)

    crit_roll = random.randint(1, 10) # Rolls for a critcal hit
    if crit_roll == 10: # Has a 1/10 chance of occuring
      hit = hit*2 # The damage is doubled
      self.app.write(self.name + " scores a critical hit! Double damage inflicted!!")
      time.sleep(1)
    
    counter_roll = random.randint(1, 10) # Rolls for a counter attack
    if counter_roll == 10: # Has a 1/10 chance of occuring
      self.app.write(target.name + " countered the attack!")
      counter = self.defend_attack(hit) # Calculates if the target kills the attacker
    else: # If the counter fails
      kill = target.defend_attack(hit) # Calculate if the attacker kills the target
      counter = None # Counter does not occur

    time.sleep(1)
    if counter: # If the attacker is killed by a counter attack
      self.app.write(target.name + " has killed " + self.name + ".")
      time.sleep(0.5)
      self.app.write(target.name + " gained 20 experience!")
      time.sleep(0.5)
      self.app.write(target.name + " gained 10 gold!")
      self.app.write("")      
      target.experience += 20 # The enemy gains 20 experience
      target.gold += 10 # The enemy gains 10 gold
      target.check_player_level() # The enemies level is checked
      time.sleep(1)
      return "counter" 

    elif counter == False: # If counter == false (the enemy has countered but not killed) -> return false.
      return False

    elif kill: # If the enemy has been killed
      self.app.write(self.name + " has killed " + target.name + ".")
      time.sleep(0.5)
      self.app.write(self.name + " gained 20 experience!")
      time.sleep(0.5)
      self.app.write(self.name + " ganed 20 gold!")
      self.app.write("")      
      self.experience += 20 # The attacker gains 20 experience
      self.gold += 10 # The attacker gains 10 gold
      self.check_player_level() # The attackers level is checked
      time.sleep(1)
      return True

    elif kill == False: # If the enemy has not countered, and the enemy is not dead, return False.
      return False

  def defend_attack(self, att_damage):
    ''' Defends an attack from the enemy. Accepts the "hit" score of the attacking enemy as
    a parameter. Returns True is character dies, False if still alive.'''
    
    # defend roll
    roll = random.randint(1, 20)
    block = int(roll * (self.defense_mod + self.level) * self.defense) # Defense calculation
        
    # Roll for block - must roll a 10 (10% chance)
    block_roll = random.randint(1, 10)
    if block_roll == 10:
      self.app.write(self.name + " successfully blocks the attack!")
      block = att_damage
      time.sleep(1)

    # Calculate damage from attack
    damage = att_damage - block
    if damage < 0:
      damage = 0

    # If character has a shield, shield is depleted, not health
    if self.shield > 0:
      # Shield absorbs all damage if shield is greater than damage
      if damage <= self.shield:
        self.app.write(self.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(1)
        self.shield = self.shield - damage
        damage = 0
      # Otherwise some damage will be sustained and shield will be depleted
      elif damage != 0:
        self.app.write(self.name + "'s shield absorbs " + str(self.shield) + " damage.")
        time.sleep(1)
        damage = damage - self.shield
        self.shield = 0
      
    # Reduce health
    self.app.write(self.name + " suffers " + str(damage) + " damage!")
    self.health = self.health - damage
    time.sleep(1)
      
    # Check to see if dead or not
    if self.health <= 0:
      self.health = 0
      self.app.write(self.name + " is dead!")
      self.app.write("")
      time.sleep(1)
      return True # Returns true if the enemy is dead
    else:
      self.app.write(self.name + " has " + str(self.health) + " hit points left")
      self.app.write("")
      time.sleep(1)
      return False # Returns false if the enemy is alive

#### Character Magic Actions ####

  def valid_spell(self, choice):
    ''' Checks to see if the spell being cast is a valid spell i.e. can be cast by
    that race and the character has enough mana '''

    valid = False

    # Determine this character's race
    # This is a built-in property we can use to work out the
    # class name of the object (i.e. their race)
    race = self.__class__.__name__
    
    if choice == 1:
      if race == "Wizard" and self.mana >= 10:
        valid = True
      if race == "Scout" and self.mana >= 5:
        valid = True
    elif choice == 2 and self.mana >= 20:
      valid = True
    elif choice == 3:
      if race == "Wizard":
        valid = True

        
    return valid # Returns true if the spell can be cast by the race and if mana is high enough.

  def cast_spell(self, choice, target=False):
    ''' Casts the spell chosen by the character. Requires 2 parameters - the spell
    being cast and the target of the spell. '''
    # Creates a varaible for the player race
    race = self.__class__.__name__
    kill = False;

    # Casts a spell based on choice and player race.
    if choice == 1 and race == "Scout":
      kill = self.fire_scattergun(target)
    elif choice == 1 and race == "Wizard":
      kill = self.cast_fireball(target)
    elif choice == 2:
      self.cast_shield()
    elif choice == 3:
      self.cast_mana_drain(target)
    else:
      self.app.write("Invalid spell choice. Spell failed!")
      self.app.write("")

    return kill # Returns True if a spell kills the enemy, and false if not.

  def fire_scattergun(self, target):
    """ Uses the scattergun spell, returns true if the enemy is killed, and false if not """
    self.mana -= 5 # Subtracts the players mana
    self.app.write(self.name + " fires scattergun at " + target.name + "!")
    time.sleep(1)
      
    roll = random.randint(4, 9) # Rolls for damage
    defense_roll = random.randint(3, 5) # Rolls for defense
    damage = int(roll * self.magic) - int(defense_roll * target.resistance) # Damage calculation, including subtraction of defense calculation.
    if damage < 0:
      damage = 0
      
    # If the target has a shield, subtract the damage from the shield isntead of health.
    if target.shield > 0: 
      if damage <= target.shield:
        self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(1)
        target.shield = target.shield - damage # Reduces the targets shield
        damage = 0
      elif damage != 0: # If the targets shield is destroyed.
        self.app.write(target.name + "'s shield absorbs " + str(target.shield) + " damage.")
        time.sleep(1)
        damage = damage - target.shield # Damage is reduced by how much the shield the target has left.
        target.shield = 0 # The targets shield is destoryed
                        
    self.app.write(target.name + " takes " + str(damage) + " damage.")
    self.app.write("")
    time.sleep(1)
    target.health = target.health - damage # Reduces the targets health
      
    if target.health <= 0: # If the target is dead
      target.health = 0
      self.app.write(target.name + " is dead!")
      time.sleep(0.5)
      self.app.write(self.name + " gained 20 experience!")
      time.sleep(0.5)
      self.app.write(self.name + " gained 10 gold!")
      self.app.write("")      
      self.experience += 20 # Increase the attackers experience
      self.gold += 10 # Attacker gains 10 gold
      self.check_player_level() # Check the attackers experience
      time.sleep(1)
      return True 

    else: # If the target is alive
      self.app.write(target.name + " has " + str(target.health) + " hit points left")
      self.app.write("")
      time.sleep(1)
      return False


  def cast_fireball(self, target):
    """ Uses the fireball spell. Returns true if the target is killed, and false if not """
    self.mana -= 10 # Removes the players mana
    self.app.write(self.name + " casts Fireball on " + target.name + "!")
    time.sleep(1)
      
    roll = random.randint(1, 10) # Rolls for attack
    defense_roll = random.randint(1, 10) # Rolls for defense
    damage = int(roll * self.magic) - int(defense_roll * target.resistance) # Damage calculation, including defense.
    if damage < 0:
      damage = 0
      
    if target.shield > 0: # Subtracts the damage from the targets shield if they have one.
      if damage <= target.shield: # If the damage does not destroy the shield.
        self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(1)
        target.shield = target.shield - damage # Subtract damage from the targets shield
        damage = 0
      elif damage != 0: # If the targets shield is destroyed and damage is more than 0.
        self.app.write(target.name + "'s shield absorbs " + str(target.shield) + " damage.")
        time.sleep(1)
        damage = damage - target.shield # Subtract the shield from the damage calculation
        target.shield = 0 # Destroy the shield
                        
    self.app.write(target.name + " takes " + str(damage) + " damage.")
    self.app.write("")
    time.sleep(1)
    target.health = target.health - damage # Subtract damage from the enemies health.
      
    if target.health <= 0: # If the target is dead
      target.health = 0
      self.app.write(target.name + " is dead!")
      time.sleep(0.5)
      self.app.write(self.name + " gained 20 experience!")
      time.sleep(0.5)
      self.app.write(self.name + " gained 10 gold!")
      self.app.write("")      
      self.experience += 20 # Give 20 experience to the attacker
      self.gold += 10 # Attacker gains 20 gold
      self.check_player_level() # Check the attackers level
      time.sleep(1)
      return True

    else: # If the target is not dead.
      self.app.write(target.name + " has " + str(target.health) + " hit points left")
      self.app.write("")
      time.sleep(1)
      return False

  def cast_shield(self):
    """ Casts the shield spell. """
    self.mana -= 20 # Subtracts mana
    self.app.write(self.name + " casts Shield!")
    time.sleep(1)
    if self.shield <= self.max_shield: # If the player does not have a full shield
      self.shield = self.max_shield # Makes the players shield it's max
    self.app.write(self.name + " is shielded from the next " + str(self.shield) + " damage.")
    self.app.write("")
    time.sleep(1)

  def cast_mana_drain(self, target):
    """ Casts the mana drain spell. """
    self.app.write(self.name + " casts Mana Drain on " + target.name + "!")
    time.sleep(1)

    if target.mana >= 20: # if the target has atleast 20 mana
      drain = 20 # Set drain to the max drain - 20
      
    else: # If the target has less than 20 mana
      drain = target.mana # Sets drain to the targets mana

    self.app.write(self.name + " drains " + str(drain) + " mana from "+ target.name + ".")
    time.sleep(1)
      
    target.mana -= drain # Drain the targets mana
    self.mana += drain # Add the drain to the users mana
    if target.mana <= 0:
      target.mana = 0 # Sets the targets mana to 0 if the target has 0 or less mana left
      self.app.write(target.name + "'s mana has been exhausted!")

    else: # If the targets mana has not been exhausted
      self.app.write(target.name + " has " + str(target.mana) + " mana left")
    self.app.write("")

#### Character Item Actions ####


  def valid_item(self, choice):
    """
    Checks to see if the item being used is valid, returns True if the item is valid,
    and false if it's not.
    """
    valid = False

    # Determine this character's race
    # This is a built-in property we can use to work out the
    # class name of the object (i.e. their race)
    race = self.__class__.__name__

    # Checks if the player race has a given item, and if so, returns that the choice is valid.
    if choice == 1 and self.health_potions > 0:
      if race != 'Orc':
        valid = True
    if choice == 2:
      if race != 'Orc' and self.mana_potions > 0:
        if race != 'Goblin':
          valid = True
    if choice == 3:
      if race != 'Hobbit' and self.strength_potions > 0:
        if race != 'Wizard':
          valid = True
    if choice == 4:
      if race == 'Orc':
        valid = True
      if race == 'Uruk' and self.level > 1:
        valid == True
    if choice == 0:
      valid = True
        
    return valid
  def use_health_potion(self):
    """
    Uses a health potion and returns True. Before using this statement,
    make sure that the user has a health potion.
    """
    self.health_potions -= 1 # Subtract a health potion
    self.health += 250 # Add 250 to the characters health
    if self.health > self.max_health: # If the character has more health than their max, reduce it to their max.
      self.health = self.max_health
    self.app.write(self.name + " uses a health potion!")
    time.sleep(1)
    self.app.write(self.name + " has " + str(self.health) + " hit points.")
    self.app.write("")
    time.sleep(1)
    return True # Returns true after a health potion is used

  def use_mana_potion(self):
    """
    Uses a mana potion and returns True. Before using this statement,
    make sure that the user has a mana potion.
    """
    self.mana_potions -= 1 # Subtracts a mana potion
    self.mana += 50 # Adds 50 mana to the character
    if self.mana > self.max_mana: # If the character has more mana than their max, reduce it to their max.
      self.mana = self.max_mana
    self.app.write(self.name + " uses a mana potion!")
    time.sleep(1)
    self.app.write(self.name + " has " + str(self.mana) + " mana points.")
    self.app.write("")
    time.sleep(1)
    return True # Returns true after a mana potion is used


  def use_strength_potion(self):
    """
    Uses a strength potion and returns True. Before using this statement,
    make sure that the user has a strength potion.
    """
    self.strength_potions -= 1 # Subtracts a strength potion
    self.strength_potion_mod += 3 # Adds 3 to the strength potion modifier
    self.app.write(self.name + " uses a strength potion!")
    time.sleep(1)
    self.app.write(self.name + " will do triple damage next turn!")
    self.app.write("")
    time.sleep(1)
    return True # Returns true after a strength potion is used.

  def use_battle_axe(self, target, powerup_modifier):
    """
    Uses the battle axe if it's durability is above 0. Returns true if has durability,
    false if doesn't
    """
    # Creates a variable for the player race
    player_race = self.__class__.__name__
    
    if self.axe_durability > 0: # If the battle axe has durability left
      self.axe_durability -= 1 # Removes one axe durability
      self.app.write(self.name + " hits " + target.name + " with battle axe!")
      time.sleep(1)

      if player_race == 'Orc': # If the player race is an Orc, make a higher attack roll, and lower defense roll
        roll = random.randint(5, 10)
        defense_roll = random.randint(1, 5)
      if player_race == 'Uruk': # If the character is an Uruk, make a lower attack roll. and higher defense roll
        roll = random.randint(3, 5)
        defense_roll = random.randint(3, 4)
      damage = int(roll * (self.level + powerup_modifier + self.axe_heads + self.attack_mod + self.strength_potion_mod) * self.attack) - int(defense_roll * target.resistance) # Roll for damage (includes axe heads attack modifier) minus defense roll.
      if damage < 0:
        damage = 0
      if player_race == 'Orc': # If the player race is an orc, increase the damage by half.
        damage += int(damage / 2)
      if target.shield > 0: # If the target has a shield, deal damage to the shield not the target.
        if damage <= target.shield: # If targets shield is more than the damage
          self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
          time.sleep(1)
          target.shield = target.shield - damage # Subtract the damage from the targets shield
          damage = 0
        elif damage != 0: # If the targets shield gets destroyed, and damage is not 0
          self.app.write(target.name + "'s shield absorbs " + str(target.shield) + " damage.")
          time.sleep(1)
          damage = damage - target.shield # The targets shield is subtracted from damage
          target.shield = 0 # The targets shield is destroyed

      self.app.write(target.name + " takes " + str(damage) + " damage.")
      self.app.write("")
      time.sleep(1)
      target.health = target.health - damage # Subtract the damage from the targets health
      self.app.write(target.name  + " has " + str(target.health) + " hit points left")
      time.sleep(1)
      
      if target.health <= 0: # If the target is killed
        target.health = 0
        self.axe_heads += 1 # Add an axe head (plus one modifier)
        self.app.write(target.name + " is dead!")
        self.app.write(self.name + " gained a head!")
        time.sleep(0.5)
        self.app.write(self.name + " gained 20 experience!")
        time.sleep(0.5)
        self.app.write(self.name + " gained 10 gold!")
        self.app.write("")      
        self.experience += 20 # The attacker gains 20 experience
        self.gold += 10 # The attacker gains 10 gold
        self.check_player_level() # The attackers level is checked
        time.sleep(1)
        return True
      else: # If the target is not killed
        return False


#### Miscellaneous Character Actions ####
  def check_player_level(self):
    ''' Checks and adjusts the player level '''
    if self.experience >= 100: # If player has 100 or more experience.
      self.level += 1 # Add a level to the player
      self.app.write(self.name + " gained a level!")
      self.experience -= 100 # Subtract 100 experience from the player
      return True # Returns true if the player has leveled up
    else:
      return False # Returns false if the player has not leveled up

  def reset(self):
    ''' Resets all character values to their initial state '''
    race = self.__class__.__name__
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.health_potions = self.starting_health_potions;
    self.mana_potions = self.starting_mana_potions;
    self.strength_potions = self.starting_strength_potions;
    if race == 'Orc' or race == 'Uruk': # If the character has a battle axe
      self.axe_durability = self.starting_axe_durability;
    self.level = 0;
    self.experience = 0;
    self.shield = 0
    
  def print_status(self):
    ''' Prints the current status of the character '''

    player_race = self.__class__.__name__
    
    self.app.write(self.name + "'s Status:")
    time.sleep(0.5)

    self.app.write("Gold: " + str(self.gold)) # Always prints the gold counter
    time.sleep(0.5)
    
    health_bar = "Health: " # Always prints the health bar
    health_bar += "|"
    i = 0
    while i <= self.max_health:
      if i <= self.health:
        health_bar += "#"
      else:
        health_bar += " "
      i += 25
    health_bar += "| " + str(self.health) + " hp (" + str(int(self.health*100/self.max_health)) +"%)"
    self.app.write(health_bar)
    time.sleep(0.5)
        
    if self.max_mana > 0: # Prints the mana bar if the player has mana
      mana_bar = "Mana: "
      mana_bar += "|"
      i = 0
      while i <= self.max_mana:
        if i <= self.mana:
          mana_bar += "*"
        else:
          mana_bar += " "
        i += 10
      mana_bar += "| " + str(self.mana) + " mp (" + str(int(self.mana*100/self.max_mana)) +"%)"
      self.app.write(mana_bar)
      time.sleep(0.5)
   
    if self.shield > 0: # Prints the shield bar if the player has shield
      shield_bar = "Shield: "
      shield_bar += "|"
      i = 0
      while i <= 100:
        if i <= self.shield:
          shield_bar += "o"
        else:
          shield_bar += " "
        i += 10
      shield_bar += "| " + str(self.shield) + " sp (" + str(int(self.shield*100/self.max_shield)) +"%)"
      self.app.write(shield_bar)
      time.sleep(0.5)   
    
    if self.experience > 0: # Prints the experience bar if the player has experience
      experience_bar = 'Experience: '
      experience_bar += "|"
      i = 0
      while i <= 100:
        if i <= self.experience:
          experience_bar += "*"
        else:
          experience_bar += " "
        i += 10
      experience_bar += "| " + str(self.experience) + "/100 exp (" + str(self.experience) + "%)"
      self.app.write("Level: " + str(self.level + 1)) # Prints the player level + 1 (level 0 becomes level 1)
      time.sleep(0.5)
      self.app.write(experience_bar)
      time.sleep(0.5)
    
    if player_race == 'Orc': # If the character is an Orc, print the axe durability bar with 5 durability
      durability_bar = 'Battle Axe Durability: '
      durability_bar += "|"
      i = 0
      while i <= 5:
        if i <= self.axe_durability:
          durability_bar += "*"
        else:
          durability_bar += " "
        i += 1
      durability_bar += "| " + str(self.axe_durability) + " db (" + str(int(self.axe_durability*100/5)) +"%)"
      self.app.write("Axe heads: " + str(self.axe_heads)) # Prints the number of axe heads
      time.sleep(0.5)
      self.app.write(durability_bar)
      time.sleep(0.5)
    
    if player_race == 'Uruk' and self.level > 1: # If the character is an Uruk and is level 2.
      durability_bar = 'Battle Axe Durability: '
      durability_bar += "|"
      i = 0
      while i <= 3:
        if i <= self.axe_durability:
          durability_bar += "*"
        else:
          durability_bar += " "
        i += 1
      durability_bar += "| " + str(self.axe_durability) + " db (" + str(int(self.axe_durability*100/3)) +"%)"
      self.app.write("Axe heads: " + str(self.axe_heads)) # Prints the number of axe heads
      time.sleep(0.5)
      self.app.write(durability_bar)
      time.sleep(0.5)

    if self.starting_health_potions > 0: # If the player has health potions, the number of health potions will print.
      self.app.write("Health potions remaining: " + str(self.health_potions))
      if self.starting_mana_potions == 0 or self.starting_strength_potions == 0: # Checks to see if this is the last status printed
        self.app.write("")
      time.sleep(0.5)
        

    if self.starting_mana_potions > 0: # If the player has mana potions, the number of mana potions will print
      self.app.write("Mana potions remaining: " + str(self.mana_potions))
      if self.starting_strength_potions == 0: # Checks to see if this is the last status printed
        self.app.write("")
      time.sleep(0.5)

    if self.starting_strength_potions > 0: # If the player has strength potions, the number of strenght potions will print.
      self.app.write("Strength potions remaining: " + str(self.strength_potions))
      time.sleep(0.5)
      self.app.write("")
    

    
    


######
### Define the attributes specific to each of the Character Subclasses.
### This identifies the differences between each race.
######

class Dwarf(Character):
  '''Defines the attributes of a Dwarf in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Dwarf class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app) # Applies parent player values
    # Sets all player values
    self.max_health = 300;
    self.max_mana = 30;
    self.starting_health_potions = 1;
    self.starting_mana_potions = 1;
    self.starting_strength_potions = 2;
    self.attack = 9;
    self.defense = 6;
    self.magic = 4;
    self.resistance = 5;
    self.experience = 0;
    self.level = 0;
    self.gold = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.health_potions = self.starting_health_potions;
    self.mana_potions = self.starting_mana_potions;
    self.strength_potions = self.starting_strength_potions;

  def move(self, player):
    """ Defines the AI for the Dwarf class """
    move_complete = Character.move(self, player) # Completes the generalised AI actions
    if not move_complete: # If the general AI does not peform an action:
      self.set_stance('a')
      return self.attack_enemy(player, 0) # Dwarves always attack the enemy with an aggressive stance
    return False
    
class Elf(Character):
  '''Defines the attributes of an Elf in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Elf class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app) # Applies parent player values
    # Sets all player values
    self.max_health = 300;
    self.max_mana = 60;
    self.starting_health_potions = 2;
    self.starting_mana_potions = 2;
    self.starting_strength_potions = 1;
    self.attack = 6;
    self.defense = 8;
    self.magic = 8;
    self.resistance = 8;
    self.experience = 0;
    self.level = 0;
    self.gold = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.health_potions = self.starting_health_potions;
    self.mana_potions = self.starting_mana_potions;
    self.strength_potions = self.starting_strength_potions;

  def move(self, player):
    """ Defines the AI for the Elf class """
    move_complete = Character.move(self, player) # Completes the generalised AI actions
    if not move_complete: # If the general AI does not peform an action:
      self.set_stance('d')
      if self.shield == 0 and self.mana >= 20: # Elves use the shield spell if they dont have one, and if they are capable.
        self.cast_spell(2)
      else:
        return self.attack_enemy(player, 0)
    return False

class Goblin(Character):
  '''Defines the attributes of a Goblin in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Goblin class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app) # Applies parent player values
    # Sets all player values
    self.max_health = 200;
    self.max_mana = 30;
    self.starting_health_potions = 1;
    self.starting_mana_potions = 1;
    self.starting_strength_potions = 1;
    self.attack = 5;
    self.defense = 9;
    self.magic = 0;
    self.resistance = 10;
    self.experience = 0;
    self.level = 0;
    self.gold = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.health_potions = self.starting_health_potions;
    self.mana_potions = self.starting_mana_potions;
    self.strength_potions = self.starting_strength_potions;

  def move(self, player):
    """ Defines the AI for the Goblin class """
    move_complete = Character.move(self, player) # Completes the generalised AI actions
    if not move_complete: # If the general AI does not peform an action:
      self.set_stance('d')
      return self.attack_enemy(player, 0) # Goblins attack the player with the defensive stance.
    return False

class Hobbit(Character):
  '''Defines the attributes of a Hobbit in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Hobbit class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app) # Applies parent player values
    # Sets all player values
    self.max_health = 250;
    self.max_mana = 40;
    self.starting_health_potions = 2;
    self.starting_mana_potions = 1;
    self.starting_strength_potions = 0;
    self.attack = 3;
    self.defense = 9;
    self.magic = 6;
    self.resistance = 10;
    self.experience = 0;
    self.level = 0;
    self.gold = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.health_potions = self.starting_health_potions;
    self.mana_potions = self.starting_mana_potions;
    self.strength_potions = self.starting_strength_potions;

  def move(self, player):
    """ Defines the AI for the Hobbit class """
    move_complete = Character.move(self, player) # Completes the generalised AI actions
    if not move_complete: # If the general AI does not peform an action:
      self.set_stance('d')
      # Hobbits cast shield if they don't have one and are capable of doing so.
      if self.shield == 0 and self.mana >= 20: 
        self.cast_spell(2)
      else:
        return self.attack_enemy(player, 0)
    return False

class Human(Character):
  '''Defines the attributes of a Human in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Human class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app) # Applies parent player values
    # Sets all player values
    self.max_health = 250;
    self.max_mana = 40;
    self.starting_health_potions = 2;
    self.starting_mana_potions = 1;
    self.starting_strength_potions = 1;
    self.attack = 7;
    self.defense = 8;
    self.magic = 5;
    self.resistance = 4;
    self.experience = 0;
    self.level = 0;
    self.gold = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.health_potions = self.starting_health_potions;
    self.mana_potions = self.starting_mana_potions;
    self.strength_potions = self.starting_strength_potions;

  def move(self, player):
    """ Defines the AI for the Human class """
    move_complete = Character.move(self, player) # Completes the generalised AI actions
    if not move_complete: # If the general AI does not peform an action:
      # Sets the stance differently based on health level.
      if self.health*100 / self.max_health > 75:
        self.set_stance('a')
      elif self.health*100 / self.max_health > 30:
        self.set_stance('b')
      else:
        self.set_stance('d')
      if self.shield == 0 and self.mana >= 20: # If the human does not have a shield and can cast one, cast shield.
        self.cast_spell(2)
      else: # If the human has a shield or no mana, attack the enemy.
        return self.attack_enemy(player, 0) 
    return False

class Orc(Character):
  '''Defines the attributes of an Orc in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Orc class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app) # Applies parent player values
    # Sets all player values
    self.max_health = 250;
    self.max_mana = 0;
    self.starting_health_potions = 0;
    self.starting_mana_potions = 0;
    self.starting_strength_potions = 2;
    self.starting_axe_durability = 5;
    self.axe_heads = 0;
    self.attack = 7;
    self.defense = 7;
    self.magic = 2;
    self.resistance = 4;
    self.experience = 0;
    self.level = 0;
    self.gold = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.health_potions = self.starting_health_potions;
    self.mana_potions = self.starting_mana_potions;
    self.strength_potions = self.starting_strength_potions;
    self.axe_durability = self.starting_axe_durability;

  def move(self, player):
    """ Defines the AI for the Orc class """
    move_complete = Character.move(self, player) # Completes the generalised AI actions
    if not move_complete: # If the general AI does not peform an action:
      self.set_stance('b')
      return self.attack_enemy(player, 0) # Attacks if the generalised actions fail.
    return False

class Uruk(Character):
  '''Defines the attributes of an Uruk in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Uruk class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app) # Applies parent player values
    # Sets all player values
    self.max_health = 400;
    self.max_mana = 20;
    self.starting_health_potions = 1;
    self.starting_mana_potions = 1;
    self.starting_strength_potions = 3;
    self.starting_axe_durability = 3;
    self.axe_heads = 0;
    self.attack = 9;
    self.defense = 7;
    self.magic = 4;
    self.resistance = 6;
    self.experience = 0;
    self.level = 0;
    self.gold = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.health_potions = self.starting_health_potions;
    self.mana_potions = self.starting_mana_potions;
    self.strength_potions = self.starting_strength_potions;
    self.axe_durability = self.starting_axe_durability;

  def move(self, player):
    """ Defines the AI for the Uruk class """
    move_complete = Character.move(self, player) # Completes the generalised AI actions
    if not move_complete: # If the general AI does not peform an action:
      self.set_stance('a')
      return self.attack_enemy(player, 0) # Always attacks the enemy, if the generalised actions fail.
    return False

class Wizard(Character):
  '''Defines the attributes of a Wizard in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Wizard class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app) # Applies parent player values
    # Sets all player values
    self.max_health = 150;
    self.max_mana = 100;
    self.starting_health_potions = 2;
    self.starting_mana_potions = 2;
    self.starting_strength_potions = 0;
    self.attack = 5;
    self.defense = 6;
    self.magic = 10;
    self.resistance = 10;
    self.experience = 0;
    self.level = 0;
    self.gold = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.health_potions = self.starting_health_potions;
    self.mana_potions = self.starting_mana_potions;
    self.strength_potions = self.starting_strength_potions;

  def move(self, player):
    """ Defines the AI for the Wizard class """
    move_complete = Character.move(self, player) # Completes the generalised AI actions
    if not move_complete: # If the general AI does not peform an action:
      self.set_stance('d')
      if self.mana < 10 and player.mana > 0: # If the wizard has less than 10 mana and is capable of draining mana, cast drain mana.
        self.cast_spell(3, player)
      elif self.shield == 0 and self.mana >= 20: # If the wizard does not have a shield, and has enough mana to cast it, cast shield.
        self.cast_spell(2)
      elif self.mana >= 10: # If the wizard has more than 10 mana, cast fireball
        return self.cast_spell(1, player)
      else: # If all else fails, attack the enemy.
        return self.attack_enemy(player, 0)
    return False

class Scout(Character):
  '''Defines the attributes of an Scout in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Scout class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app) # Applies parent player values
    # Sets all player values
    self.max_health = 75;
    self.max_mana = 35;
    self.starting_health_potions = 3;
    self.starting_mana_potions = 2;
    self.starting_strength_potions = 1;
    self.attack = 6;
    self.defense = 4;
    self.magic = 10;
    self.resistance = 6;
    self.experience = 0;
    self.level = 0;
    self.gold = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.health_potions = self.starting_health_potions;
    self.mana_potions = self.starting_mana_potions;
    self.strength_potions = self.starting_strength_potions;

  def move(self, player):
    """ Defines the AI for the Scout class """
    move_complete = Character.move(self, player) # Completes the generalised AI actions
    if not move_complete: # If the general AI does not peform an action:
      self.set_stance('a')
      if self.shield == 0 and self.mana >= 20: # If the scout is does not have a shield, and can cast one, a cast it.
        self.cast_spell(2)
      elif self.mana >= 5: # Else, if the scout is capable of fireing the scattergun,
        return self.cast_spell(1, player)
      else:
        return self.attack_enemy(player, 0) # If all else fails, attack.
    return False