# Fantasy-Land
This is a turn based, text based, rpg battle engine implemented using Object Oriented Programming using Python. It is themed around generic fantasy.
You should run the rpg.py file to start the game.

Edited By Morgan Potter

Commented 'rpg.py'

Added the 'Scout' class. The class has extremely low health (75), but extremely high attack (Like in tf2). This makes him somewhat of a glass cannon, dying to strong characters, but easily taking out tank characters.

Added the 'Scattergun' spell to the 'Scout' class. The scattergun functions extremely similarly to the fireball spell, only the damage is consistently higher. The scouts normal attack is very inconsistent, so adding a more consistent form of damage balances the class.

Added a flee function, which varies in difficulty depending on the class choice.

Added Map feature, with non-moving, randomly generated enemies.

Added powerups to the map. This powerup is given to the player and not the enemy, as currently it is significantly harder to win than lose. The game needs to be easier for the player to win to keep the player interested. Not many people enjoy games they cannot win, at the very least they need a glimmer of hope.

Added an inventory and mana potion. The inventory gives another UI element, making it easier for the user to navigate. The mana potion gives a much needed, stable way to restore player mana. This is balanced so the characters with more mana get more mana potions. This give characters more chances to use spells, deepening the gameplay through more gameplay decisions. 

Players and enemies can no longer have a damage calc of 0. Damage can still equal zero if the defense roll is higher than the attack roll, but this just means there is less of a chance to deal / take 0 damage.

Added the strength potion. Strength potions are divied out to characters who would need them, and who would seem like they would carry them. Dwarves, uruks, orcs and the scout all carry strength potions.

Added the experience system. Currently, this system directly effects player attack, depending on experience level. This adds a level of strategy to the game, as if the player uses their map powerups well, they can get consistent high attack modifiers.

Added new difficulty 'impossible'. This takes the most over powered characters, and adds 4 of them. This is for players who are tired of the joys of life and can only be beaten if the player gets incredibly lucky.

Added a chance for a counter attack, using the same attack damage as the player enflicted, and rerolling defence for the attacker. This punishes the player for using all their powerups at once, and adds a layer of risk to using a strength potion, as the player may die. This does not punish the player for leveling up, as leveling up also increases defence by the same amount. Enhibiting the player from hording powerups, means that the player has to be more strategic when using powerups, and makes the game more intersesting to the player, even though it may be frustrating at first.

Added the leveling system (using the experience system), which currently boosts attack and defense. The level count displays level 1, but is actually level one. This makes things slightly easier to visualize - if the player has gained two levels, then their level is level 2 as opposed to level 3. This replaces the experience attack modifier. This is mainly to make the attack boosting system more slow, and means that the player has to beat atleast one battle without any experience modifier - adding an additional layer of player skill, whilst keeping the player improvement system. Enemies also gain experience, but only from winning a battle or killing you, so they can never use this benefit. This is good for balancing as it makes the game easier for the player.

Added the battle axe. Is an item wielded by orcs and urukai. Orcs wield the weapon better, and can wield the weapon at level one/zero as apposed to level 2/3. Orcs get 1.5 times boosted attack, and get a higher and more consistent damage and defence roll when using the weapon. This balances the Orc class, as they are significantly weaker than almost all the other classes, and the Orc Battle axe is a very powerful item.

Added a item pickup system. After every turn, the player has a chance to pick up one or two of a random item (they have to start with the item to pick it up). In terms of story, it would make more sence to have a chance to pick up an item after every battle (when the player is travelling), however in terms of game balance, every battle is extremely long and players typically need more than the starting amount of items. To correct the story, a roaming wizard grants the player items.

Commented map.py

Commented battle.py

Added mana potions and strength potions to the enemy AI. If the enemy has full health and a strength potion, it uses a strength potion. If a enemy has used a strength potion the previous turn, it will always attack. If a enemy has no mana and a mana potion, it uses a mana potion.

Commented character.py

</b>
Balancing:
</b>

I am taking a direct approach to balancing the game. The good side and evil side should have an equivalent character. IF there is not enough characters to have an equivalent character, one character should be stronger than the rest. The evil side has less characters than the good side due to the added scout class. To counteract this i have made the Uruk class stronger. They the same damage as a dwarf, have the highest health, and the highest defence. They have access to the shield spell, health potions, strength potions, and the Uruk battle axe at level 2/3. Despite Uruks being more powerful, they most closely resemble dwarves, high hit points, high damage, above average defense. 

Goblins were the weakest character in the game, but I have balanced them closely to hobbits, making their mana and health slightly less but their attack slightly more. Hobbits and Goblins are meant to be the weakest characters in the game (hence being used under the easy category), so making them equal, makes the evil and good sides more equal.

I have balanced the orc class against the human class, making their attack the same, and the orcs defense lower, with no health potions, but giving the orc 2 strength potions. I have given the orc a battle axe that does more damage for it, and has a consistantly high damage roll. This further balances the two sides, as the good side has an additional elf class.

Both the evil and good wizards are the same, so there is no balancing needed there.

In each difficulty setting there is a mixed number of good classes and bad classes, the good classes becoming more prominent as the list goes up. With this new balancing of sides, I have had to balance the difficulty settings accordingly. Uruks are the best evil class, so they are only available to fight in legendary and impossible mode. Wizards are the second best, so they are also only seen in legendary and impossible difficulties. Player controlled orcs can be one of the best classes, but the orc AI does not live up to this, so they are only seen in hard and medium difficulties. Goblins are the weakest so they are only seen in  medium/easy difficulty, and there is one in hard difficulty. These are now very similar in difficulty to good mode, which only required a few changes. Elves and dwarves are stronger than humans, so they moved up the ranks into legendary difficulty. Dwarves are better than elves, so one elf and two humans are seen in hard difficulty. 

Added the gold system and the merchant trader. Decreased the chance of obtaining a random item from a wizard (1/10 to 1/15), as the player can now easily buy items after a battle. Players can also buy an additional attack powerup.

Removed the AI strength potion usage, as even the easiest levels became too difficult. 

Made the enemies move in a random direction on the map. They cannot move onto a occupied space, meaning they cannot attack the enemy. They also cannot travel outside of the map. 
